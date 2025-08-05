import can 

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

def get_status():
    return read_can(reg_status)

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

def get_inversion(status=None):
    if status is None:
        status = get_status()
    inversion = [bool(status & 0b1000000000000), bool(status & 0b10000000000000)]
    return inversion

def get_pos():
    pos_l = read_can(reg_pos_l)
    pos_r = read_can(reg_pos_r)
    return [pos_l, pos_r]

def get_eeprom_state():
    mem_cnt = read_can(reg_mem_cnt)
    mem_off = read_can(reg_mem_off)
    return [mem_cnt, mem_off]

def set_vend(vend_l, vend_r):
    write_can(reg_vend_l, vend_l)
    write_can(reg_vend_r, vend_r)
    write_can(reg_cmd, 0x01)
    return

def get_vend():
    vend_l = read_can(reg_vend_l)
    vend_r = read_can(reg_vend_r)
    return [vend_l, vend_r]

def set_ref(ref_l, ref_r):
    write_can(reg_ref_l, ref_l)
    write_can(reg_ref_r, ref_r)
    return

def reset_errors():
    write_can(reg_cmd, 0x02)
    return

def reset_state():
    write_can(reg_cmd, 0x04)
    write_can(reg_hb_in, 0x04)
    return

def send_heartbeat(value=1000):
    write_can(reg_heart, value)
    write_can(reg_heart_hb, value)
    return

def read_can(reg_addr):
    with can.Bus(interface='socketcan', channel='can0', bitrate=125000) as bus:
        try:
            bus.send(can.Message(arbitration_id=0x99, data=[reg_addr, 0], is_extended_id=False))
            for msg in bus:
                if msg.arbitration_id == reg_addr:
                    if len(msg.data) == 2:
                        return msg.data[0] + msg.data[1]*256
        except Exception as e:
            print("Fehler beim Lesen")
            print(e)
            return 0

def write_can(reg_addr, val):
     with can.Bus(interface='socketcan', channel='can0', bitrate=125000) as bus:
        msg = can.Message(arbitration_id=reg_addr, data=[val%256, (val//256)%256], is_extended_id=False)
        try:
            bus.send(msg)
        except:
            print("Fehler beim Schreiben")
            return 0