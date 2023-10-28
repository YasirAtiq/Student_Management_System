from PyQt6.QtWidgets import (QApplication, QLayout, QWidget, QGridLayout,
                             QLabel, QLineEdit, QPushButton, QMainWindow,
                             QTableWidget, QTableWidgetItem, QDialog)
from PyQt6.QtGui import QAction
import sqlite3
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        add_student_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course",
                                              "Phone no."))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = list(connection.execute("SELECT * FROM students"))
        self.table.setRowCount(0)
        for index, row in enumerate(result):
            self.table.insertRow(index)
            for col_num, data in enumerate(row):
                self.table.setItem(index, col_num,
                                   QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = None


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()


app = QApplication(sys.argv)
age_calculator = MainWindow()
age_calculator.show()
age_calculator.load_data()
sys.exit(app.exec())
