import can 
import redis 
import json
import time

start_time = time.time()
loop_duration = 0.05

heartbeat = 1000
motor_status = 0
geo_l = 0
geo_r = 0
pos_l = 0
pos_r = 0
fieldname = "Testfeld"
speed = "Testgeschwindigkeit"
gps = "TestGPS"

reg_heart = 0x01
reg_motor_status = 0x05
reg_pos_l = 0x11
reg_geo_l = 0x13
reg_pos_r = 0x21
reg_geo_r = 0x23
reg_fieldname = 0x60
reg_speed = 0x61
reg_gps = 0x62
reg_req = 0x98


if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    while True:
        try:
        # Check if loop duration has passed
        if time.time() - start_time > loop_duration:
            start_time = time.time()

            # Read values from Redis
            redismsg = r.get("client_feedback")
            data = json.loads(redismsg) if redismsg else {}
            geo_l = data.get("left_rate", 0)
            geo_r = data.get("right_rate", 0)
            speed = str(data.get("speed", ""))
            gps = str(data.get("longitude", "GPS not ok"))

            fieldname = r.get("project_file")

            # Send CAN messages
            with can.Bus(interface='socketcan', channel='can0', bitrate=125000) as bus:
                try:
                    bus.send(can.Message(arbitration_id=reg_heart, data=[heartbeat % 256, (heartbeat // 256) % 256], is_extended_id=False))
                    bus.send(can.Message(arbitration_id=reg_geo_l, data=[geo_l % 256, (geo_l // 256) % 256], is_extended_id=False))
                    bus.send(can.Message(arbitration_id=reg_geo_r, data=[geo_r % 256, (geo_r // 256) % 256], is_extended_id=False))
                except Exception as e:
                    print("Fehler beim Schreiben der Geometriedaten:", e)
                try:
                    for msg in bus:
                        if msg.arbitration_id == reg_req:
                            if msg.data[0] == reg_fieldname:
                                bus.send(can.Message(arbitration_id=reg_fieldname, data=list(fieldname.encode('utf-8')), is_extended_id=False))
                            elif msg.data[0] == reg_speed:
                                bus.send(can.Message(arbitration_id=reg_speed, data=list(speed.encode('utf-8')), is_extended_id=False))
                            elif msg.data[0] == reg_gps:
                                bus.send(can.Message(arbitration_id=reg_gps, data=list(gps.encode('utf-8')), is_extended_id=False))
                        elif msg.arbitration_id == reg_pos_l:
                            pos_l = msg.data[0] + (msg.data[1] << 8)
                        elif msg.arbitration_id == reg_pos_r:
                            pos_r = msg.data[0] + (msg.data[1] << 8)
                        elif msg.arbitration_id == reg_motor_status:
                            motor_status = msg.data[0] + (msg.data[1] << 8)
                        r.set("motor_feedback", json.dumps({"motor_status": motor_status, "left_position": pos_l, "right_position": pos_r}))
                except Exception as e:
                    print("Fehler beim Verarbeiten der CAN-Nachricht:", e)