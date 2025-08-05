import IOs
import time

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
soll_rechts = 0
vend_soll = 0
cnt_vend = 0

state = "INIT"

def get_soll():
    global soll_links, soll_rechts
    return soll_links, soll_rechts

def get_vend_soll():
    global vend_soll
    return vend_soll

def get_state():
    global state
    global soll_links, soll_rechts
    global vend_soll
    global cnt_vend
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
            state = "CALIB"
            cnt_vend += 1
            IOs.set_led(L7, True)
            time.sleep(0.1)
            if cnt_vend > 5:
                cnt_vend = 0
                state = "MANUAL_L"
        if IOs.get_button(B6):
            if vend_soll < 900:
                vend_soll += 50
        if IOs.get_button(B7):
            if vend_soll > 100:
                vend_soll -= 50
        if IOs.get_button(B8):
            soll_links = int(vend_soll / 10)
        if IOs.get_button(B9):
            soll_links = 0

        IOs.set_led(L4, True)        
        

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
            state = "CALIB"
        if IOs.get_button(B6):
            if soll_links < 100:
                soll_links += 5
        if IOs.get_button(B7):
            if soll_links > 0:
                soll_links -= 5
        if IOs.get_button(B8):
            pass
        if IOs.get_button(B9):
            state = "MANUAL_R"

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
            state = "MANUAL_L"

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
            pass

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
            pass
        if IOs.get_button(B7):
            pass
        if IOs.get_button(B8):
            pass
        if IOs.get_button(B9):
            pass

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
            pass
        if IOs.get_button(B7):
            pass
        if IOs.get_button(B8):
            pass
        if IOs.get_button(B9):
            state = "EDGE_R"

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
            pass
        if IOs.get_button(B7):
            pass
        if IOs.get_button(B8):
            pass
        if IOs.get_button(B9):
            state = "EDGE_L"

        IOs.set_led(L5, True)

        
    if state != oldstate:
        soll_links = 0
        soll_rechts = 0
        vend_soll = 0
        cnt_vend = 0
    return state