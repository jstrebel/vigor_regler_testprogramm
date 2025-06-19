import IOs

# ACHTUNG ALLE K9 sind auf K8 gesetzt und K8 auf K7

B1 = 3
B2 = 2
B3 = 1
B4 = 0
B5 = 8
B6 = 4 
B7 = 5
B8 = 6
B9 = 7


state = "INIT"
soll_vend = 0

def get_state():
    global state

    if state == "INIT":
        if IOs.get_button(B1):
            pass
        elif IOs.get_button(B2):
            pass
        elif IOs.get_button(B3):
            pass
        elif IOs.get_button(B4):
            pass
        elif IOs.get_button(B5):
            pass
        elif IOs.get_button(B6):
            pass
        elif IOs.get_button(B7):
            state = "EDGE_L"
        elif IOs.get_button(B8):
            state = "MANUAL_L"
        elif IOs.get_button(B9):
            state = "CALIB"


    elif state == "CALIB":
        if IOs.get_button(B1):
            state = "AUTO"
        elif IOs.get_button(B2):
            state = "SEMI"
        elif IOs.get_button(B3):
            state = "MANUAL_L"
        elif IOs.get_button(B4):
            state = "EDGE_L"
        elif IOs.get_button(B5):
            pass
        elif IOs.get_button(B6):
            pass
        elif IOs.get_button(B7):
            pass
        elif IOs.get_button(B8):
            pass
        elif IOs.get_button(B9):
            pass
        

    elif state == "MANUAL_L":
        if IOs.get_button(B1):
            state = "AUTO"
        elif IOs.get_button(B2):
            state = "SEMI"
        elif IOs.get_button(B3):
            state = "MANUAL_L"
        elif IOs.get_button(B4):
            state = "EDGE_L"
        elif IOs.get_button(B5):
            state = "CALIB"
        elif IOs.get_button(B6):
            pass
        elif IOs.get_button(B7):
            pass
        elif IOs.get_button(B8):
            pass
        elif IOs.get_button(B9):
            pass

    elif state == "ERROR":
        if IOs.get_button(B1):
            state = "AUTO"
        elif IOs.get_button(B2):
            state = "SEMI"
        elif IOs.get_button(B3):
            state = "MANUAL_L"
        elif IOs.get_button(B4):
            state = "EDGE_L"
        elif IOs.get_button(B5):
            state = "CALIB"
        elif IOs.get_button(B6):
            pass
        elif IOs.get_button(B7):
            pass
        elif IOs.get_button(B8):
            pass
        elif IOs.get_button(B9):
            pass

    elif state == "SEMI":
        if IOs.get_button(B1):
            state = "AUTO"
        elif IOs.get_button(B2):
            state = "SEMI"
        elif IOs.get_button(B3):
            state = "MANUAL_L"
        elif IOs.get_button(B4):
            state = "EDGE_L"
        elif IOs.get_button(B5):
            state = "CALIB"
        elif IOs.get_button(B6):
            pass
        elif IOs.get_button(B7):
            pass
        elif IOs.get_button(B8):
            pass
        elif IOs.get_button(B9):
            pass

    elif state == "AUTO":
        if IOs.get_button(B1):
            state = "AUTO"
        elif IOs.get_button(B2):
            state = "SEMI"
        elif IOs.get_button(B3):
            state = "MANUAL_L"
        elif IOs.get_button(B4):
            state = "EDGE_L"
        elif IOs.get_button(B5):
            state = "CALIB"
        elif IOs.get_button(B6):
            pass
        elif IOs.get_button(B7):
            pass
        elif IOs.get_button(B8):
            pass
        elif IOs.get_button(B9):
            pass

    elif state == "EDGE_L":
        if IOs.get_button(B1):
            state = "AUTO"
        elif IOs.get_button(B2):
            state = "SEMI"
        elif IOs.get_button(B3):
            state = "MANUAL_L"
        elif IOs.get_button(B4):
            state = "EDGE_L"
        elif IOs.get_button(B5):
            state = "CALIB"
        elif IOs.get_button(B6):
            pass
        elif IOs.get_button(B7):
            pass
        elif IOs.get_button(B8):
            pass
        elif IOs.get_button(B9):
            pass
        
    print("State:", state)
    print("B1:", IOs.get_button(B1))
    print("B2:", IOs.get_button(B2))
    print("B3:", IOs.get_button(B3))
    print("B4:", IOs.get_button(B4))
    print("B5:", IOs.get_button(B5))
    print("B6:", IOs.get_button(B6))
    print("B7:", IOs.get_button(B7))
    print("B8:", IOs.get_button(B8))
    print("B9:", IOs.get_button(B9))
    return state