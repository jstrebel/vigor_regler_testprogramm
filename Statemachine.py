import IOs

state = "INIT"
soll_vend = 0

def get_state():
    global state

    if state == "INIT":
        if IOs.get_button(7):
            state = "MANUAL_L"
        elif IOs.get_button(8):
            state = "CALIB"

    elif state == "CALIB":
        pass

    return state