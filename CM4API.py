import CAN_Wrapper

reg_fieldname = 0x60
reg_speed = 0x61
reg_gps = 0x62
reg_req_cm4 = 0x98

def get_fieldname():
    return CAN_Wrapper.read_can_str(reg_fieldname, reg_req_cm4)

def get_speed():
    return CAN_Wrapper.read_can_2byte(reg_speed, reg_req_cm4)

def get_gps():
    return CAN_Wrapper.read_can_2byte(reg_gps, reg_req_cm4)

