import CAN_Wrapper

reg_fieldname = 0x60
reg_speed = 0x61
reg_gps = 0x62
reg_req_cm4 = 0x98

def get_fieldname():
    fieldname = CAN_Wrapper.read_can_str(reg_fieldname, reg_req_cm4)
    return fieldname

def get_speed():
    speed = CAN_Wrapper.read_can_str(reg_speed, reg_req_cm4)
    return speed + " km/h"

def get_gps():
    gps = CAN_Wrapper.read_can_str(reg_gps, reg_req_cm4)
    return gps
