import CAN_Wrapper

reg_heart = 0x01
reg_heart_hb = 0x02
reg_status = 0x05
reg_ref_l = 0x10
reg_pos_l = 0x11
reg_vend_l = 0x12
reg_geo_l = 0x13
reg_ref_r = 0x20
reg_pos_r = 0x21
reg_vend_r = 0x22
reg_geo_r = 0x23
reg_hb_in = 0x70
reg_mem_cnt = 0x80
reg_mem_off = 0x81
reg_cmd = 0x90
reg_req_nano = 0x99

def get_status():
    return CAN_Wrapper.read_can_2byte(reg_status, reg_req_nano)

def get_state(numbers=False, status=None):
    if status is None:
        status = get_status()
    state = (status & 0x00F0)>>4
    if state > 4:
        state = 4
    if numbers:
        return state
    else:
        if state == 1:
            return "Semiautomatik"
        elif state == 2:
            return "Automatik"
        elif state == 3:
            return "Manuell"
        else: 
            return "Fehler"

def get_endstops(status=None):
    if status is None:
        status = get_status()
    endstops = [bool(status & 0b10), bool(status & 0b1), bool(status & 0b1000), bool(status & 0b100)]
    return endstops

def get_watchdogs(status=None):
    if status is None:
        status = get_status()
    watchdogs = [bool(status & 0b100000000000), bool(status & 0b10000000000), bool(status & 0b1000000000), bool(status & 0b100000000)]
    return watchdogs

def get_timeout(status=None):
    if status is None:
        status = get_status()
    timeout = bool(status & 0b100000000000000) or bool(status & 0b1000000000000000)
    return timeout

def get_inversion(status=None):
    if status is None:
        status = get_status()
    inversion = [bool(status & 0b1000000000000), bool(status & 0b10000000000000)]
    return inversion

def get_pos():
    pos_l = CAN_Wrapper.read_can_2byte(reg_pos_l, reg_req_nano)
    pos_r = CAN_Wrapper.read_can_2byte(reg_pos_r, reg_req_nano)
    return [pos_l, pos_r]

def get_eeprom_state():
    mem_cnt = CAN_Wrapper.read_can_2byte(reg_mem_cnt, reg_req_nano)
    mem_off = CAN_Wrapper.read_can_2byte(reg_mem_off, reg_req_nano)
    return [mem_cnt, mem_off]

def set_vend(vend_l, vend_r):
    CAN_Wrapper.write_can(reg_vend_l, vend_l)
    CAN_Wrapper.write_can(reg_vend_r, vend_r)
    CAN_Wrapper.write_can(reg_cmd, 0x01)
    return

def get_vend():
    vend_l = CAN_Wrapper.read_can_2byte(reg_vend_l, reg_req_nano)
    vend_r = CAN_Wrapper.read_can_2byte(reg_vend_r, reg_req_nano)
    return [vend_l, vend_r]

def get_geo():
    geo_l = CAN_Wrapper.read_can_2byte(reg_geo_l, reg_req_nano)
    geo_r = CAN_Wrapper.read_can_2byte(reg_geo_r, reg_req_nano)
    return [geo_l, geo_r]

def set_ref(ref_l, ref_r):
    CAN_Wrapper.write_can(reg_ref_l, ref_l)
    CAN_Wrapper.write_can(reg_ref_r, ref_r)
    return

def reset_errors():
    CAN_Wrapper.write_can(reg_cmd, 0x02)
    return

def reset_state():
    CAN_Wrapper.write_can(reg_cmd, 0x04)
    CAN_Wrapper.write_can(reg_hb_in, 0x04)
    return

def send_heartbeat(value=1000):
    CAN_Wrapper.write_can(reg_heart, value)
    CAN_Wrapper.write_can(reg_heart_hb, value)
    return
