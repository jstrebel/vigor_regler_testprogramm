import redis 

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
soll_vend = 0

def set_soll_vend(value):
    global soll_vend
    soll_vend = value
    r.set("hmi_vend_soll", value)

def set_value(key, value):
    r.set(key, value)

def get_value(key):
    value = r.get(key)
    if value is not None:
        return value
    else:
        return "Key not found"