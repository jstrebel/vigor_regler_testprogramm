import IOs

# ACHTUNG ALLE K9 sind auf K8 gesetzt und K8 auf K7

state = "INIT"
soll_vend = 0

def get_state():
    global state

    if state == "INIT":
        if IOs.get_button(0):
            pass
        elif IOs.get_button(1):
            pass
        elif IOs.get_button(2):
            pass
        elif IOs.get_button(3):
            pass
        elif IOs.get_button(4):
            pass
        elif IOs.get_button(5):
            pass
        elif IOs.get_button(6):
            state = "MANUAL_L"
        elif IOs.get_button(7):
            state = "CALIB"

    elif state == "CALIB":
        if IOs.get_button(0):
            state = "AUTO"
        elif IOs.get_button(1):
            state = "SEMI"
        elif IOs.get_button(2):
            state = "MANUAL_L"
        elif IOs.get_button(3):
            state = "EDGE_L"
        elif IOs.get_button(4):
            pass
        elif IOs.get_button(5):
            pass
        elif IOs.get_button(6):
            pass
        elif IOs.get_button(7):
            pass
        

    elif state == "MANUAL_L":
        if IOs.get_button(0):
            state = "AUTO"
        elif IOs.get_button(1):
            state = "SEMI"
        elif IOs.get_button(2):
            state = "MANUAL_L"
        elif IOs.get_button(3):
            state = "EDGE_L"
        elif IOs.get_button(4):
            state = "CALIB"
        elif IOs.get_button(5):
            pass
        elif IOs.get_button(6):
            pass
        elif IOs.get_button(7):
            pass

    elif state == "ERROR":
        if IOs.get_button(0):
            state = "AUTO"
        elif IOs.get_button(1):
            state = "SEMI"
        elif IOs.get_button(2):
            state = "MANUAL_L"
        elif IOs.get_button(3):
            state = "EDGE_L"
        elif IOs.get_button(4):
            state = "CALIB"
        elif IOs.get_button(5):
            pass
        elif IOs.get_button(6):
            pass
        elif IOs.get_button(7):
            pass

    elif state == "SEMI":
        if IOs.get_button(0):
            state = "AUTO"
        elif IOs.get_button(1):
            state = "SEMI"
        elif IOs.get_button(2):
            state = "MANUAL_L"
        elif IOs.get_button(3):
            state = "EDGE_L"
        elif IOs.get_button(4):
            state = "CALIB"
        elif IOs.get_button(5):
            pass
        elif IOs.get_button(6):
            pass
        elif IOs.get_button(7):
            pass

    elif state == "AUTO":
        if IOs.get_button(0):
            state = "AUTO"
        elif IOs.get_button(1):
            state = "SEMI"
        elif IOs.get_button(2):
            state = "MANUAL_L"
        elif IOs.get_button(3):
            state = "EDGE_L"
        elif IOs.get_button(4):
            state = "CALIB"
        elif IOs.get_button(5):
            pass
        elif IOs.get_button(6):
            pass
        elif IOs.get_button(7):
            pass

    elif state == "EDGE_L":
        if IOs.get_button(0):
            state = "AUTO"
        elif IOs.get_button(1):
            state = "SEMI"
        elif IOs.get_button(2):
            state = "MANUAL_L"
        elif IOs.get_button(3):
            state = "EDGE_L"
        elif IOs.get_button(4):
            state = "CALIB"
        elif IOs.get_button(5):
            pass
        elif IOs.get_button(6):
            pass
        elif IOs.get_button(7):
            pass

    return state