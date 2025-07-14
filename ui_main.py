from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt, QThread
from controller import ControllerThread

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gözle Mouse Kontrolü")
        self.setGeometry(100, 100, 300, 200)

        self.controller_thread = None

        self.label_status = QLabel("Durum: Kapalı")
        self.label_status.setAlignment(Qt.AlignCenter)

        self.btn_start = QPushButton("Başlat")
        self.btn_start.clicked.connect(self.toggle_tracking)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(10)
        self.slider.setValue(5)
        self.slider.valueChanged.connect(self.update_sensitivity)

        self.label_sens = QLabel("Hassasiyet: 5")

        layout = QVBoxLayout()
        layout.addWidget(self.label_status)
        layout.addWidget(self.btn_start)
        layout.addWidget(self.label_sens)
        layout.addWidget(self.slider)

        self.setLayout(layout)
        self.running = False

    def toggle_tracking(self):
        if self.running:
            self.controller_thread.stop()
            self.controller_thread.quit()
            self.controller_thread.wait()
            self.label_status.setText("Durum: Kapalı")
            self.btn_start.setText("Başlat")
            self.running = False
        else:
            self.controller_thread = ControllerThread(sensitivity=self.slider.value())
            self.controller_thread.start()
            self.label_status.setText("Durum: Takip Ediliyor")
            self.btn_start.setText("Durdur")
            self.running = True

    def update_sensitivity(self):
        self.label_sens.setText(f"Hassasiyet: {self.slider.value()}")
        if self.controller_thread:
            self.controller_thread.sensitivity = self.slider.value()
