import sqlite3
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

conn = sqlite3.connect('Attendance System.db')
c = conn.cursor()


class ViewWindow(QtWidgets.QMainWindow):
    def __init__(self):

        super(ViewWindow, self).__init__()
        self.setGeometry(300, 50, 800, 600)
        self.setWindowTitle("Students List")
        self.setWindowIcon(QtGui.QIcon('other_images/logo.png'))
        self.selected_subject = None

        # Heading
        h = QtWidgets.QLabel(self)
        h.setAlignment(QtCore.Qt.AlignCenter)
        h.setGeometry(QtCore.QRect(100, 20, 600, 50))
        h.setStyleSheet("QLabel { background-color : blue;color :white ; }")
        font = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        h.setFont(font)
        h.setText("Students List")

        # Subject
        l_subject = QtWidgets.QLabel(self)
        l_subject.setAlignment(QtCore.Qt.AlignCenter)
        l_subject.setGeometry(QtCore.QRect(150, 150, 130, 30))
        l_subject.setStyleSheet("QLabel { background-color : gray;color :black ; }")
        font = QtGui.QFont("Times", 14, QtGui.QFont.Bold)
        l_subject.setFont(font)
        l_subject.setText("Subject")

        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(290, 150, 300, 30)
        font1 = QtGui.QFont("Arial", 14)
        self.comboBox.setFont(font1)
        c = conn.cursor()
        c.execute('select * from SUBJECTS')
        rows = c.fetchall()
        for row in rows:
            self.comboBox.addItem(row[0])

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(270, 200, 330, 200)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Student', 'Subject', 'Section'])
        self.selected_subject = self.comboBox.currentText()
        self.comboBox.activated.connect(self.handleActivated)
        self.populateTable()

        # # Button for clearing fields
        # button_reset = QtWidgets.QPushButton(self)
        # button_reset.setText("RESET")
        # button_reset.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        # button_reset.setGeometry(480, 450, 100, 30)
        # button_reset.setStyleSheet("QPushButton { background-color : red ;color : white ; }")
        # # self.entries = [self.e_section, self.e_student_id]
        # # button_reset.clicked.connect(self.erase)
        #
        # # Button for submission of data and storing in database
        # button_submit = QtWidgets.QPushButton(self)
        # button_submit.setText("SUBMIT")
        # button_submit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        # button_submit.setGeometry(350, 450, 100, 30)
        # button_submit.setStyleSheet("QPushButton { background-color : green;color : white ; }")
        # # button_submit.clicked.connect(self.submit)

        self.l_message = QtWidgets.QLabel(self)
        self.l_message.setAlignment(QtCore.Qt.AlignCenter)
        self.l_message.setStyleSheet("QLabel { color:green ; }")
        self.l_message.setFont(QtGui.QFont('Times', 13))
        self.l_message.setGeometry(QtCore.QRect(280, 500, 350, 30))

    def populateTable(self):
        self.tableWidget.setRowCount(0)
        result = c.execute('select * from sub_sec_stu where subject ="' + self.selected_subject + '"')
        for row_num, row_data in enumerate(result):
            self.tableWidget.insertRow(row_num)
            for column_num, column_data in enumerate(row_data):
                self.tableWidget.setItem(row_num, column_num, QTableWidgetItem(str(column_data)))

    def handleActivated(self):
        self.selected_subject = self.comboBox.currentText()
        self.populateTable()

    def erase(self):
        self.l_message.setText("")
        for entry in self.entries:
            entry.clear()
