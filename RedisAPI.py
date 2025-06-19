import redis 

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def set_value(key, value):
    r.set(key, value)

def get_value(key):
    value = r.get(key)
    if value is not None:
        return value
    else:
        return "Key not found"