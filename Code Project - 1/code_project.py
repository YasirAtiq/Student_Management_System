from PyQt6.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel,
                             QLineEdit, QPushButton, QComboBox)
import sys


class SpeedCalc(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Average Speed Calculator")

        grid = QGridLayout()

        distance_label = QLabel("Distance:")
        self.distance_line_label = QLineEdit()

        time_label = QLabel("Time (Hours):")
        self.time_line_label = QLineEdit()

        calc_button = QPushButton("Calculate")
        self.output = QLabel("")

        self.unit = QComboBox()
        self.unit.addItems(["Metric (km)", "Imperial (miles)"])

        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_line_label, 0, 1)
        grid.addWidget(self.unit, 0, 2)
        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.time_line_label, 1, 1)
        grid.addWidget(calc_button, 2, 1)
        grid.addWidget(self.output, 3, 0, 1, 2)

        calc_button.clicked.connect(self.calc_speed)

        self.setLayout(grid)

    def calc_speed(self):
        try:
            if self.unit.currentText() == "Metric (km)":
                k = 1
            else:
                k = 0.6214
            distance = float(self.distance_line_label.text()) * k
            hours = float(self.time_line_label.text())
            speed = round(distance / hours, 2)
            self.output.setText(f"Average Speed: {speed} kmh")
        except ValueError:
            self.output.setText(
                "Incorrect value for either the distance or time.")


app = QApplication(sys.argv)
speed_calculator = SpeedCalc()
speed_calculator.show()
sys.exit(app.exec())
