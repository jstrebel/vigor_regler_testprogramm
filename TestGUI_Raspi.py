import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt5.QtCore import QTimer
import MotorAPI

class SliderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TestGUI_Raspi")
        self.setGeometry(100, 100, 800, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QHBoxLayout(self.central_widget)
        stack = QVBoxLayout()

        self.text_overall = QLabel("Gesamtübersicht:\n" + \
                                   "Status:\t0b0000000000000000\n" + \
                                    "Controllerstate:\t0" + \
                                    "Endanschlag links vorne:\tfalse" + \
                                    "Endanschlag links hinten:\tfalse" + \
                                    "Endanschlag rechts vorne:\tfalse" + \
                                    "Endanschlag rechts hinten:\tfalse")

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
                                "Sollwert:\t\t0\n" + \
                                "Istwert:\t\t0\n" + \
                                "Anschlag:\t\t0\n")
        self.text_right = QLabel("Motor rechts:\n" + \
                                "Sollwert:\t\t0\n" + \
                                "Istwert:\t\t0\n" + \
                                "Anschlag:\t\t0\n")

        stack.addWidget(self.text_overall)
        stack.addWidget(self.reset_err)
        stack.addWidget(self.reset_s)

        layout.addLayout(stack)
        layout.addWidget(self.slider_left)
        layout.addWidget(self.text_left)
        layout.addWidget(self.slider_right)
        layout.addWidget(self.text_right)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)  # Alle 100 Millisekunden

    def update_reference(self):
        MotorAPI.set_ref(self.slider_left.value(), self.slider_right.value())

    def update(self):
        MotorAPI.send_heartbeat()
        #Update Text
        p = MotorAPI.get_pos()
        s = [self.slider_left.value(), self.slider_right.value()]
        a = MotorAPI.get_vend()
        self.text_left.setText(f"Motor links:\n" + \
                               f"Sollwert:\t\t{s[0]}%\n" + \
                               f"Istwert:\t\t{p[0]}\n" + \
                               f"Anschlag:\t\t{a[0]}\n")
        self.text_right.setText(f"Motor rechts:\n" + \
                                f"Sollwert:\t\t{s[1]}%\n" + \
                                f"Istwert:\t\t{p[1]}\n" + \
                                f"Anschlag:\t\t{a[1]}\n")
        state = MotorAPI.get_state()
        status = MotorAPI.get_status()
        endstops = MotorAPI.get_endstops()
        self.text_overall.setText(f"Gesamtübersicht:\n" + \
                                  f"Status:\t{bin(status)}\n" + \
                                  f"Controllerstate:\t{state}" + \
                                  f"Endanschlag links vorne:\t{endstops[0]}" + \
                                  f"Endanschlag links hinten:\t{endstops[1]}" + \
                                  f"Endanschlag rechts vorne:\t{endstops[2]}" + \
                                  f"Endanschlag rechts hinten:\t{endstops[3]}")

    def reset_errors(self):
        MotorAPI.reset_errors()

    def reset_state(self):
        MotorAPI.set_state(2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SliderApp()
    window.show()
    sys.exit(app.exec_())
