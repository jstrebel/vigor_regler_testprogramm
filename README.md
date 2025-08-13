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
Zum Testen der Verbindung für ausgehende Nachrichten kann mit dem folgenden Befehl ein Datenpaket gesendet werden:
```
cansend can0 01a#1234
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

## Redis
```
sudo apt install redis-server
```
UND IN REQUIREMENTS.TXT FEHLT ES AUCH NOCH

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
0x99 0x80 0x00
-> 0x080 .. ..
0x99 0x81 0x00
-> 0x81 .. ..
```

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


## Autostart
### CAN Service
1️⃣ Systemd service to bring up CAN at boot
Create the service:
```
sudo nano /etc/systemd/system/can0.service
```
Put this inside:
```
[Unit]
Description=Setup CAN interface can0
After=network.target

[Service]
Type=oneshot
ExecStart=/sbin/ip link set can0 up type can bitrate 125000
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```
Enable and start it:
```
sudo systemctl daemon-reload
sudo systemctl enable can0.service
sudo systemctl start can0.service
```
Now can0 will be configured before your GUI starts.

### GUI
Option 1 – Keep the GUI as a desktop app
Let Raspberry Pi OS boot into the graphical desktop automatically (even if no monitor is plugged in).
Your PyQt5 GUI will always have an X server running to draw on.
If you later plug in an HDMI monitor, you’ll instantly see the window.
Startup order still works — we just make the systemd service run inside your autologged-in X session.

Create a systemd user service (not system-wide) so it runs inside X:
```
mkdir -p /home/hbraspi/.config/systemd/user
nano /home/hbraspi/.config/systemd/user/vigor_gui.service
```
Paste:

```
[Unit]
Description=Start Vigor GUI
After=can0.service
Requires=can0.service

[Service]
Type=simple
WorkingDirectory=/home/hbraspi/Desktop/vigor_regler_testprogramm
ExecStart=/bin/bash -c "source .venv/bin/activate && python TestGUI_Raspi.py"
Restart=on-failure
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/hbraspi/.Xauthority

[Install]
WantedBy=default.target
```
Enable it for your user:
```
systemctl --user daemon-reload
systemctl --user enable vigor_gui.service
```

### Bildschirm
3️⃣ Starting the Vigor make run task
Since this one seems like it’s terminal-based and not GUI, we can make it another systemd service:
```
sudo nano /etc/systemd/system/vigor.service
```

```
[Unit]
Description=Run Vigor Example
After=can0.service

[Service]
Type=simple
User=hbraspi
WorkingDirectory=/home/hbraspi/Desktop/forked_Repos/Vigor_TFT_Display/examples
ExecStart=/usr/bin/make run
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
Enable it:
```
sudo systemctl enable vigor.service
```
