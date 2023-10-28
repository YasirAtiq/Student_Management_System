## Importing...
from PyQt6.QtWidgets import (QApplication, QLayout, QWidget, QGridLayout,
                             QLabel, QLineEdit, QPushButton)
from datetime import datetime
import sys


class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()

        # Making the title of the window 'Age Calculator'.
        self.setWindowTitle("Age Calculator")

        # Make a grid to add widgets
        grid = QGridLayout()

        # Making the name label and the textbox
        name_label = QLabel("Name:")
        self.name_line_label = QLineEdit()

        # Making the DOB label and the textbox
        dob_label = QLabel("DOB in MM/DD/YYYY:")
        self.dob_line_label = QLineEdit()

        # Adding the button to calculate age and the label as output.
        calc_button = QPushButton("Calculate Age")
        self.output = QLabel("")

        # Calling on the get_age() func when button is pressed.
        calc_button.clicked.connect(self.get_age)

        # Adding these widgets to the grid.
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_label, 0, 1)
        grid.addWidget(dob_label, 1, 0)
        grid.addWidget(self.dob_line_label, 1, 1)
        grid.addWidget(calc_button, 2, 0, 1, 2)
        grid.addWidget(self.output, 3, 0, 1, 2)

        # Adding the grid to the window.
        self.setLayout(grid)

    def get_age(self):
        current = datetime.now().year
        year = self.dob_line_label.text()[6:10]
        try:
            if not len(year) <= 3:
                yob = int(year)
                age = str(current - yob)
                self.output.setText(
                    f"{self.name_line_label.text()} is {age} years old.")
            else:
                self.output.setText(f"Incorrect value given for the DOB.")

        except ValueError:
            self.output.setText(f"Incorrect value given for the DOB.")


app = QApplication(sys.argv)
age_calculator = AgeCalculator()
age_calculator.show()
sys.exit(app.exec())
