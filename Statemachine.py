import IOs

# ACHTUNG ALLE K9 sind auf K8 gesetzt und K8 auf K7

state = "INIT"
soll_vend = 0

def get_state():
    global state

    if state == "INIT":
        if IOs.get_button(6):
            state = "MANUAL_L"
        elif IOs.get_button(7):
            state = "CALIB"

    elif state == "CALIB":
        pass

    return state