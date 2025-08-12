import IOs
import time
import MotorAPI
import RedisAPI

B1 = 3
B2 = 2
B3 = 1
B4 = 0
B5 = 8
B6 = 4 
B7 = 5
B8 = 6
B9 = 7

L1 = 5
L2 = 4
L3 = 3
L4 = 6
L5 = 2
L6 = 0
L7 = 1

soll_links = 0
geo_l = 0
soll_rechts = 0
geo_r = 0
vend_soll = 100
cnt_vend = 0
vend_curr = 910
inverted = False

state = "INIT"
debounce_flag = False
cal_released_flag = False
lr_released_flag = False
enable_geo = False

def get_soll():
    global soll_links, soll_rechts
    return soll_links, soll_rechts

def get_geo():
    global geo_l, geo_r
    return geo_l, geo_r

def get_vend_soll():
    global vend_soll
    return vend_soll

def set_error():
    global state
    state = "ERROR"

def set_vend_curr(vend):
    global vend_curr
    if 100 <= vend <= 910:
        vend_curr = vend
    else:
        raise ValueError("Vend must be between 100 and 910")
    
def set_inverted(invert):
    global inverted
    if isinstance(invert, bool):
        inverted = invert
    else:
        raise ValueError("Inversion must be a boolean value")

def get_state():
    global state
    global soll_links, soll_rechts
    global vend_soll
    global cnt_vend
    global debounce_flag, cal_released_flag, lr_released_flag
    global vend_curr, inverted
    global geo_l, geo_r
    global enable_geo
    oldstate = state

    if state == "INIT":
        if IOs.get_button(B1):
            pass
        if IOs.get_button(B2):
            pass
        if IOs.get_button(B3):
            pass
        if IOs.get_button(B4):
            pass
        if IOs.get_button(B5):
            pass
        if IOs.get_button(B6):
            pass
        if IOs.get_button(B7):
            pass
        if IOs.get_button(B8):
            state = "MANUAL_L"
        if IOs.get_button(B9):
            state = "CALIB"

        IOs.set_led(L7, True)


    elif state == "CALIB":
        if IOs.get_button(B1):
            state = "AUTO"
        if IOs.get_button(B2):
            state = "SEMI"
        if IOs.get_button(B3):
            state = "MANUAL_L"
        if IOs.get_button(B4):
            state = "EDGE_L"
        if IOs.get_button(B5):
            cnt_vend += 1
            if cnt_vend > 30:   # 3s at 100ms
                state = "MANUAL_L"
                cal_released_flag = False
                MotorAPI.set_vend(vend_soll, vend_soll)
                RedisAPI.set_value("hmi_vend_ist", vend_soll)
        else:
            cnt_vend = 0
        if IOs.get_button(B6):
            if inverted: 
                soll_links = round((910 - vend_soll) / (910 - vend_curr) * 100)
            else:
                soll_links = round((vend_soll - 100) / (vend_curr - 100) * 100)
        if IOs.get_button(B7):
            soll_links = 0
        if IOs.get_button(B8):
            if vend_soll < 910:
                vend_soll += 5
            cnt_vend = 0
        if IOs.get_button(B9):
            if vend_soll > 100:
                vend_soll -= 5
            cnt_vend = 0

        if cnt_vend < 10:
            IOs.set_led(L4, True)
        else:
            if cnt_vend % 2:
                IOs.set_led(L4, True)
            else:
                IOs.set_led(L7, True)


    elif state == "MANUAL_L":
        if IOs.get_button(B1):
            state = "AUTO"
        if IOs.get_button(B2):
            state = "SEMI"
        if IOs.get_button(B3):
            state = "MANUAL_L"
        if IOs.get_button(B4):
            state = "EDGE_L"
        if IOs.get_button(B5):
            if cal_released_flag:
                state = "CALIB"
        else: 
            cal_released_flag = True
        if IOs.get_button(B6):
            if soll_links < 100:
                soll_links += 5
        if IOs.get_button(B7):
            if soll_links > 0:
                soll_links -= 5
        if IOs.get_button(B8):
            pass
        if IOs.get_button(B9):
            if lr_released_flag:
                state = "MANUAL_R"
                lr_released_flag = False
        else:
            lr_released_flag = True
        IOs.set_led(L3, True)
        

    elif state == "MANUAL_R":
        if IOs.get_button(B1):
            state = "AUTO"
        if IOs.get_button(B2):
            state = "SEMI"
        if IOs.get_button(B3):
            state = "MANUAL_L"
        if IOs.get_button(B4):
            state = "EDGE_L"
        if IOs.get_button(B5):
            state = "CALIB"
        if IOs.get_button(B6):
            if soll_rechts < 100:
                soll_rechts += 5
        if IOs.get_button(B7):
            if soll_rechts > 0:
                soll_rechts -= 5
        if IOs.get_button(B8):
            pass
        if IOs.get_button(B9):
            if lr_released_flag:
                state = "MANUAL_L"
                lr_released_flag = False
        else:
            lr_released_flag = True
        IOs.set_led(L3, True)


    elif state == "ERROR":
        if IOs.get_button(B1):
            pass
        if IOs.get_button(B2):
            pass
        if IOs.get_button(B3):
            pass
        if IOs.get_button(B4):
            pass
        if IOs.get_button(B5):
            pass
        if IOs.get_button(B6):
            pass
        if IOs.get_button(B7):
            pass
        if IOs.get_button(B8):
            pass
        if IOs.get_button(B9):
            state = "MANUAL_L"
            lr_released_flag = False
            MotorAPI.reset_errors()
            MotorAPI.reset_state()

        IOs.set_led(L6, True)


    elif state == "SEMI":
        if IOs.get_button(B1):
            state = "AUTO"
        if IOs.get_button(B2):
            state = "SEMI"
        if IOs.get_button(B3):
            state = "MANUAL_L"
        if IOs.get_button(B4):
            state = "EDGE_L"
        if IOs.get_button(B5):
            state = "CALIB"
        if IOs.get_button(B6):
            soll_links = 100
            soll_rechts = 100
        if IOs.get_button(B7):
            soll_links = 0
            soll_rechts = 0
        if IOs.get_button(B8):
            pass
        if IOs.get_button(B9):
            pass

        IOs.set_led(L2, True)


    elif state == "AUTO":
        if IOs.get_button(B1):
            state = "AUTO"
        if IOs.get_button(B2):
            state = "SEMI"
        if IOs.get_button(B3):
            state = "MANUAL_L"
        if IOs.get_button(B4):
            state = "EDGE_L"
        if IOs.get_button(B5):
            state = "CALIB"
        if IOs.get_button(B6):
            enable_geo = True
        if IOs.get_button(B7):
            enable_geo = False
        if IOs.get_button(B8):
            pass
        if IOs.get_button(B9):
            pass

        geo_l, geo_r = MotorAPI.get_geo()
        if enable_geo:
            soll_links = geo_l
            soll_rechts = geo_r
        else:
            soll_links = 0
            soll_rechts = 0
        IOs.set_led(L1, True)


    elif state == "EDGE_L":
        if IOs.get_button(B1):
            state = "AUTO"
        if IOs.get_button(B2):
            state = "SEMI"
        if IOs.get_button(B3):
            state = "MANUAL_L"
        if IOs.get_button(B4):
            state = "EDGE_L"
        if IOs.get_button(B5):
            state = "CALIB"
        if IOs.get_button(B6):
            enable_geo = True
        if IOs.get_button(B7):
            enable_geo = False
        if IOs.get_button(B8):
            pass
        if IOs.get_button(B9):
            if lr_released_flag:
                state = "EDGE_R"
                lr_released_flag = False
        else:
            lr_released_flag = True

        geo_l, geo_r = MotorAPI.get_geo()
        if enable_geo:
            soll_links = geo_l
        else:
            soll_links = 0
        IOs.set_led(L5, True)


    elif state == "EDGE_R":
        if IOs.get_button(B1):
            state = "AUTO"
        if IOs.get_button(B2):
            state = "SEMI"
        if IOs.get_button(B3):
            state = "MANUAL_L"
        if IOs.get_button(B4):
            state = "EDGE_L"
        if IOs.get_button(B5):
            state = "CALIB"
        if IOs.get_button(B6):
            enable_geo = True
        if IOs.get_button(B7):
            enable_geo = False
        if IOs.get_button(B8):
            pass
        if IOs.get_button(B9):
            if lr_released_flag:
                state = "EDGE_L"
                lr_released_flag = False
        else:
            lr_released_flag = True
        geo_l, geo_r = MotorAPI.get_geo()
        if enable_geo:
            soll_rechts = geo_r
        else:
            soll_rechts = 0
        IOs.set_led(L5, True)

    if debounce_flag:
        time.sleep(0.5)  # Debounce delay
        debounce_flag = False
        
    if state != oldstate:
        soll_links = 0
        soll_rechts = 0
        debounce_flag = True
        enable_geo = False
        cnt_vend = 0
    return state