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


## Aufsetzen 
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
