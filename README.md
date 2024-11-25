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
dtoverlay=spi1-1cs
dtoverlay=mcp2515,spi1-0,oscillator=16000000,interrupt=25
```
