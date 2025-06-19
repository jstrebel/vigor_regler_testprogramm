# KnÃ¶pfe kÃ¶nnen nur vom HC...1 eingelesen werden.
# Kalibrieren wird nicht erkannt

from gpiozero import DigitalOutputDevice
from gpiozero import DigitalInputDevice

s0 = DigitalOutputDevice(0)
s1 = DigitalOutputDevice(1)
s2 = DigitalOutputDevice(4)

s02 = DigitalOutputDevice(6)

a = DigitalInputDevice(5)
a2 = DigitalInputDevice(12)

def set_mux(i):
    if not 0 <= i <= 7:
        raise ValueError()
    # Convert i to 3-bit binary string and reverse (LSB to MSB)
    bits = [int(b) for b in f"{i:03b}"][::-1]  # s0 = LSB

    s0.value = bits[0]
    s1.value = bits[1]
    s2.value = bits[2]

def read_button(i):
    if not 0 <= i <= 8:
        raise ValueError()
    if i < 8:
        set_mux(i)
        return a.is_active
    else:
        s02.value = 0
        return a2.is_active
        
        
