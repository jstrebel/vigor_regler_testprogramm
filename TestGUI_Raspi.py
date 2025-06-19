import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QPushButton, QSpinBox
from PyQt5.QtCore import QTimer
import MotorAPI
import RedisAPI

class SliderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TestGUI_Raspi")
        self.setGeometry(100, 100, 800, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QHBoxLayout(self.central_widget)
        stack = QVBoxLayout()
        stackm1 = QVBoxLayout()
        stackm2 = QVBoxLayout()

        self.text_overall = QLabel("Gesamtübersicht:\n" + \
                                   "Status:\t0b0000000000000000\n" + \
                                    "Controllerstate:\t0\n" + \
                                    "Endanschlag links hinten:\t\tFalse\n" + \
                                    "Endanschlag links vorne:\t\tFalse\n" + \
                                    "Endanschlag rechts hinten:\tFalse\n" + \
                                    "Endanschlag rechts vorne:\t\tFalse\n" + \
                                    "Watchdog links hinten:\tFalse\n" + \
                                    "Watchdog links vorne:\tFalse\n" + \
                                    "Watchdog rechts hinten:\tFalse\n" + \
                                    "Watchdog rechts vorne:\tFalse\n" + \
                                    "\n" + \
                                    "EEPROM Counter:\t0\n" + \
                                    "EEPROM Offset:\t\t0\n")

        self.btn_new_vend = QPushButton("neue Anschläge senden")
        self.btn_new_vend.pressed.connect(self.new_vend)

        self.reset_err = QPushButton("Fehler zurücksetzen")
        self.reset_err.pressed.connect(self.reset_errors)
        
        self.reset_s = QPushButton("Controllerstate zurücksetzen")
        self.reset_s.pressed.connect(self.reset_state)

        self.slider_left = QSlider()
        self.slider_left.setRange(0, 100)
        self.slider_left.valueChanged.connect(self.update_reference)

        self.slider_right = QSlider()
        self.slider_right.setRange(0, 100)
        self.slider_right.valueChanged.connect(self.update_reference)

        self.text_left = QLabel("Motor links:\n" + \
                                "Inverted:\t\tFalse\n" + \
                                "Sollwert:\t\t0\n" + \
                                "Istwert:\t\t0\n" + \
                                "Anschlag:\t0\n")
        self.spin_vend_left = QSpinBox()
        self.spin_vend_left.setMaximum(1000)

        self.text_right = QLabel("Motor rechts:\n" + \
                                "Inverted:\t\tFalse\n" + \
                                "Sollwert:\t\t0\n" + \
                                "Istwert:\t\t0\n" + \
                                "Anschlag:\t0\n")
        self.spin_vend_right = QSpinBox()
        self.spin_vend_right.setMaximum(1000)

        stack.addWidget(self.text_overall)
        stack.addWidget(self.btn_new_vend)
        stack.addWidget(self.reset_err)
        stack.addWidget(self.reset_s)

        stackm1.addWidget(self.text_left)
        stackm1.addWidget(self.spin_vend_left)

        stackm2.addWidget(self.text_right)
        stackm2.addWidget(self.spin_vend_right)

        layout.addLayout(stack)
        layout.addWidget(self.slider_left)
        layout.addLayout(stackm1)
        layout.addWidget(self.slider_right)
        layout.addLayout(stackm2)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(500)  # Alle 100 Millisekunden

    def update_reference(self):
        MotorAPI.set_ref(self.slider_left.value(), self.slider_right.value())

    def update(self):
        MotorAPI.send_heartbeat()
        #Update Text
        p = MotorAPI.get_pos()
        s = [self.slider_left.value(), self.slider_right.value()]
        a = MotorAPI.get_vend()
        i = MotorAPI.get_inversion()
        self.text_left.setText(f"Motor links:\n" + \
                               f"Inverted:\t\t{i[0]}\n" + \
                               f"Sollwert:\t\t{s[0]}%\n" + \
                               f"Istwert:\t\t{p[0]}\n" + \
                                f"Anschlag:\t{a[0]}\n")
        self.text_right.setText(f"Motor rechts:\n" + \
                                f"Inverted:\t\t{i[1]}\n" + \
                                f"Sollwert:\t\t{s[1]}%\n" + \
                                f"Istwert:\t\t{p[1]}\n" + \
                                f"Anschlag:\t{a[1]}\n")
        status = MotorAPI.get_status()
        state = MotorAPI.get_state(status=status)
        endstops = MotorAPI.get_endstops(status=status)
        watchdogs = MotorAPI.get_watchdogs(status=status)
        inversion = MotorAPI.get_inversion(status=status)
        e = MotorAPI.get_eeprom_state()
        self.text_overall.setText(f"Gesamtübersicht:\n" + \
                                  f"Status:\t{format(status, '#018b')}\n" + \
                                  f"Controllerstate:\t{state}\n" + \
                                  f"Endanschlag links hinten:\t\t{endstops[0]}\n" + \
                                  f"Endanschlag links vorne:\t\t{endstops[1]}\n" + \
                                  f"Endanschlag rechts hinten:\t{endstops[2]}\n" + \
                                  f"Endanschlag rechts vorne:\t\t{endstops[3]}\n" + \
                                  f"Watchdog links hinten:\t{watchdogs[0]}\n" + \
                                  f"Watchdog links vorne:\t{watchdogs[1]}\n" + \
                                  f"Watchdog rechts hinten:\t{watchdogs[2]}\n" + \
                                  f"Watchdog rechts vorne:\t{watchdogs[3]}\n" + \
                                  f"\n" + \
                                  f"EEPROM Counter:\t{e[0]}\n" + \
                                  f"EEPROM Offset:\t\t{e[1]}\n" + \
                                  f"Inversion left:\t{inversion[0]}\n" + \
                                  f"Inversion right:\t{inversion[1]}\n")
        
        RedisAPI.set_value("hmi_pos_l", str(p[0]))
        RedisAPI.set_value("hmi_pos_r", str(p[1]))

    def new_vend(self):
        MotorAPI.set_vend(self.spin_vend_left.value(), self.spin_vend_right.value())

    def reset_errors(self):
        MotorAPI.reset_errors()

    def reset_state(self):
        MotorAPI.reset_state()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SliderApp()
    window.show()
    sys.exit(app.exec_())
