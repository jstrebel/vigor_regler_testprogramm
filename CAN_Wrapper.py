import can 

def read_can_str(reg_addr, req_addr):
    with can.Bus(interface='socketcan', channel='can0', bitrate=125000) as bus:
        try:
            bus.send(can.Message(arbitration_id=req_addr, data=[reg_addr, 0], is_extended_id=False))
            for msg in bus:
                if msg.arbitration_id == reg_addr:
                    data = []
                    for part in msg.data:
                        data.append(part)
                    return str(data)
        except Exception as e:
            print("Fehler beim Lesen")
            print(e)
            return 0
        
def read_can_2byte(reg_addr, req_addr):
    with can.Bus(interface='socketcan', channel='can0', bitrate=125000) as bus:
        try:
            bus.send(can.Message(arbitration_id=req_addr, data=[reg_addr, 0], is_extended_id=False))
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