from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QLayout, QWidget, QGridLayout,
                             QLabel, QLineEdit, QPushButton, QMainWindow,
                             QTableWidget, QTableWidgetItem, QDialog,
                             QVBoxLayout, QComboBox)
from PyQt6.QtGui import QAction
import sqlite3
import sys

connection = sqlite3.connect("database.db")
raw_course = list(connection.execute("SELECT * FROM Courses"))
courses = []
for i in raw_course:
    course = i[1]
    courses.append(course)
connection.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction("Register Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        search_student_action = QAction("Find Student", self)
        search_student_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_student_action)

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
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog(self.table)
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Details")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.courses_dropbox = QComboBox()
        self.courses_dropbox.addItems(courses)
        layout.addWidget(self.courses_dropbox)

        self.phone_number = QLineEdit()
        self.phone_number.setPlaceholderText("Phone no.")
        layout.addWidget(self.phone_number)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.add_student)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.courses_dropbox.itemText(
            self.courses_dropbox.currentIndex())
        phone_number = self.phone_number.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
            (name, course, phone_number))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self, table):
        super().__init__()
        self.table = table
        self.setWindowTitle("Insert Student Details")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Name of Student")
        layout.addWidget(self.search_name)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)
        layout.addWidget(search_button)

        self.setLayout(layout)

    def search(self):
        name = self.search_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?",
                                (name,))
        rows = list(result)
        items = self.table.findItems(name,
                                     Qt.MatchFlag.MatchFixedString)

        for item in items:
            self.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
