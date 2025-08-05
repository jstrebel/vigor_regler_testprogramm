# KnÃ¶pfe kÃ¶nnen nur vom HC...1 eingelesen werden.
# Kalibrieren wird nicht erkannt

from gpiozero import DigitalOutputDevice
from gpiozero import DigitalInputDevice

ti1_s0 = DigitalOutputDevice(0) # pin 27
ti1_s1 = DigitalOutputDevice(1) # pin 28
ti1_s2 = DigitalOutputDevice(4) # pin 7
ti1_a = DigitalInputDevice(5) # pin 29

ti2_s0 = DigitalOutputDevice(6) # pin 31
ti2_s1 = DigitalOutputDevice(23) # pin 16
ti2_s2 = DigitalOutputDevice(22) # pin 15
ti2_a = DigitalInputDevice(12) # pin 32

led_s0 = DigitalOutputDevice(13) # pin 33
led_s1 = DigitalOutputDevice(17) # pin 11
led_s2 = DigitalOutputDevice(18) # pin 12
led_a = DigitalOutputDevice(27) # pin 13

def set_mux_ti1(i):
    if not 0 <= i <= 7:
        raise ValueError()
    # Convert i to 3-bit binary string and reverse (LSB to MSB)
    bits = [int(b) for b in f"{i:03b}"][::-1]  # s0 = LSB

    ti1_s0.value = bits[0]
    ti1_s1.value = bits[1]
    ti1_s2.value = bits[2]

def set_mux_ti2(i):
    if not 8 <= i <= 15:
        raise ValueError()
    # Convert i to 3-bit binary string and reverse (LSB to MSB)
    bits = [int(b) for b in f"{i:03b}"][::-1]  # s0 = LSB

    ti2_s0.value = bits[0]
    ti2_s1.value = bits[1]
    ti2_s2.value = bits[2]

def set_mux_led(i):
    if not 0 <= i <= 7:
        raise ValueError()
    # Convert i to 3-bit binary string and reverse (LSB to MSB)
    bits = [int(b) for b in f"{i:03b}"][::-1]  # s0 = LSB

    led_s0.value = bits[0]
    led_s1.value = bits[1]
    led_s2.value = bits[2]

def get_button(i):
    if not 0 <= i <= 15:
        raise ValueError()
    if i < 8:
        set_mux_ti1(i)
        return not ti1_a.is_active
    else:
        set_mux_ti2(i - 8)
        return not ti2_a.is_active

def set_led(i, state):
    if not 0 <= i <= 7:
        raise ValueError()
    set_mux_led(i)
    if state:
        led_a.on()
    else:
        led_a.off()
