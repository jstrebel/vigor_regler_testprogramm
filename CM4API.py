import CAN_Wrapper

reg_fieldname = 0x60
reg_speed = 0x61
reg_gps = 0x62
reg_req_cm4 = 0x98

fieldname = "asdf"
speed = "0 km/h"
gps = "GPS: fault"

def get_fieldname():
    global fieldname
    msg = CAN_Wrapper.read_can_str(reg_fieldname, reg_req_cm4)
    if msg is not None:
        fieldname = msg
    return fieldname

def get_speed():
    global speed
    msg = CAN_Wrapper.read_can_str(reg_speed, reg_req_cm4)
    if msg is not None:
        speed = msg
    return speed + " km/h"

def get_gps():
    global gps
    msg = CAN_Wrapper.read_can_str(reg_gps, reg_req_cm4)
    if msg is not None:
        gps = msg
    return "GPS: " + gps
