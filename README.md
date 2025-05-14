# vigor_regler_testprogramm

## Nutzung
Für die Nutzung des MCP2515-Boards von joy-it sind momentan folgende Kommandozeileneingaben nach dem Start nötig:
```
sudo ip link set can0 up type can bitrate 125000
```
Dies kann weiter automatisiert werden, ist aber vorerst vernachlässigt worden.
Anschliessend kann mit der folgenden Eingabe die CAN-Verbindung geprüft werden, sofern die Werkzeuge mit ```sudo apt-get install can-utils installiert``` sind:
```
candump can0
```


## Aufsetzen SPI
Damit das MCP2515-Board am SPI1 betrieben werden kann sind folgende Änderungen in */boot/firmware/config.txt* nötig:
```
dtparam=spi=on
dtoverlay=spi1-1cs,cs0_pin=16
dtoverlay=mcp2515,spi1-0,oscillator=16000000,interrupt=26
```

### Pinbelegung
| **Board-Bezeichnung** | **Raspi-Pin** | **Raspi-Bezeichnung** | **Raspi-Alternativfunktion** |
|------------------------|---------------|------------------------|-----------------------------|
| VCC                   | 1             | 3v3 Power             |                             |
| VCC1                  | 2             | 5v Power              |                             |
| GND                   | 39            | Ground                |                             |
| CS                    | 36            | GPIO16                | SPI1 CE0  (remapped from GPIO18)                 |
| SO                    | 35            | GPIO19                | SPI1 MISO                  |
| SI                    | 38            | GPIO20                | SPI1 MOSI                  |
| CLK                   | 40            | GPIO21                | SPI1 SCLK                  |
| INT                   | 37            | GPIO26                |                             |

## Python environement
Da PyQt5 auf dem Raspi Probleme bereitet, funktioniert die Standardanwendung nicht. Daher muss das venv mit den site-packages installiert werden, da PyQt5 da bereits dabei ist.
```
python -m venv --system-site-packages .venv
```
Anschliessend muss das Environement aktiviert werden und die requirements geladen werden.
```
source .venv/bin/activate
pip install -r requirements.txt
```

## Kommunikation
Die Kommunikation auf dem CAN Bus erfolgt in 5 verschiedenen Use-Cases.

### update
AA und BB sind Platzhalter für die Werte der Heartbeats
.. sind Platzhalter für die Werte der jeweiligen Register
```
ADR  LSB  MSB
0x01 0xAA 0xAA
0x02 0xBB 0xBB
0x99 0x11 0x00
-> 0x11 .. ..
0x99 0x21 0x00
-> 0x21 .. ..
0x99 0x12 0x00
-> 0x12 .. ..
0x99 0x22 0x00
-> 0x22 .. ..
0x99 0x05 0x00
-> 0x05 .. ..
0x99 0x05 0x00
-> 0x05 .. ..
0x99 0x05 0x00
-> 0x05 .. ..
0x99 0x05 0x00
-> 0x05 .. ..
0x99 0x05 0x00
-> 0x05 .. ..
0x99 0x80 0x00
-> 0x080 .. ..
0x99 0x81 0x00
-> 0x81 .. ..
```
Verbesserungspotenzial da 5x hintereinander das Statusregister abgefragt wird

### neue Anschläge
XX und YY sind Platzhalter für die Werte der neuen Anschläge
```
ADR  LSB  MSB
0x12 0xXX 0xXX
0x22 0xYY 0xYY
0x90 0x01 0x00
```

### Fehler zurücksetzen
```
ADR  LSB  MSB
0x90 0x02 0x00
```

### Controllerstate zurücksetzen
```
ADR  LSB  MSB
0x90 0x04 0x00
```

### neue Sollwerte
SS und TT sind Platzhalter für die Werte der neuen Anschläge
```
ADR  LSB  MSB
0x10 0xSS 0xSS
0x20 0xTT 0xTT
```
