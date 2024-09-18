from smbus2 import SMBus

addr = 22

reg_heart = 0x01
reg_status = 0x05
reg_ref_l = 0x10
reg_pos_l = 0x11
reg_vend_l = 0x12
reg_ref_r = 0x20
reg_pos_r = 0x21
reg_vend_r = 0x22
reg_mem_cnt = 0x80
reg_mem_off = 0x81
reg_cmd = 0x90

bus = SMBus(1)

def get_status():
    return read_i2c(addr, reg_status)

def get_state(numbers=False):
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

def get_endstops():
    status = get_status()
    endstops = [bool(status & 0b10), bool(status & 0b1), bool(status & 0b1000), bool(status & 0b100)]
    return endstops

def get_watchdogs():
    status = get_status()
    watchdogs = [bool(status & 0b100000000000), bool(status & 0b10000000000), bool(status & 0b1000000000), bool(status & 0b100000000)]
    return watchdogs

def get_inversion():
    status = get_status()
    inversion = [bool(status & 0b1000000000000), bool(status & 0b10000000000000)]
    return inversion

def get_pos():
    pos_l = read_i2c(addr, reg_pos_l)
    pos_r = read_i2c(addr, reg_pos_r)
    return [pos_l, pos_r]

def get_eeprom_state():
    mem_cnt = read_i2c(addr, reg_mem_cnt)
    mem_off = read_i2c(addr, reg_mem_off)
    return [mem_cnt, mem_off]

def set_vend(vend_l, vend_r):
    write_i2c(addr, reg_vend_l, vend_l)
    write_i2c(addr, reg_vend_r, vend_r)
    write_i2c(addr, reg_cmd, 0x01)
    return

def get_vend():
    vend_l = read_i2c(addr, reg_vend_l)
    vend_r = read_i2c(addr, reg_vend_r)
    status = read_i2c(addr, reg_status)    
    if status & 0x2000:
        print("manuelle kalibration erfolgt und quittiert")
        status &= 0xDFFF
        status |= 0x4000
        write_i2c(addr, reg_status, status)
    return [vend_l, vend_r]

def set_ref(ref_l, ref_r):
    write_i2c(addr, reg_ref_l, ref_l)
    write_i2c(addr, reg_ref_r, ref_r)
    return

def reset_errors():
    write_i2c(addr, reg_cmd, 0x02)
    return

def reset_state():
    write_i2c(addr, reg_cmd, 0x04)

def send_heartbeat(value=1000):
    write_i2c(addr, reg_heart, value)
    return

def read_i2c(addr, reg_addr):
    try:
        return bus.read_word_data(addr, reg_addr)
    except IOError:
        print("Fehler beim Lesen")
        return 0

def write_i2c(addr, reg_addr, val):
    try:
        bus.write_word_data(addr, reg_addr, val)
    except IOError:
        print("Fehler beim Schreiben")