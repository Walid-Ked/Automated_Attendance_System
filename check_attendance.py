import sqlite3

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

conn = sqlite3.connect('Attendance System.db')
c = conn.cursor()


class CheckAttendance(QtWidgets.QMainWindow):
    def __init__(self):
        self.py_date = None

        super(CheckAttendance, self).__init__()
        self.setGeometry(300, 30, 850, 650)
        self.setWindowTitle("Check Attendance")
        self.setWindowIcon(QtGui.QIcon('other_images/logo.png'))
        self.selected_subject = None

        # Heading
        h = QtWidgets.QLabel(self)
        h.setAlignment(QtCore.Qt.AlignCenter)
        h.setGeometry(QtCore.QRect(100, 5, 600, 50))
        h.setStyleSheet("QLabel { background-color : blue;color :white ; }")
        font = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        h.setFont(font)
        h.setText("Check Attendance")

        # Subject
        l_subject = QtWidgets.QLabel(self)
        l_subject.setAlignment(QtCore.Qt.AlignCenter)
        l_subject.setGeometry(QtCore.QRect(150, 70, 130, 30))
        l_subject.setStyleSheet("QLabel { background-color : gray;color :black ; }")
        font = QtGui.QFont("Times", 14, QtGui.QFont.Bold)
        l_subject.setFont(font)
        l_subject.setText("Subject")

        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(290, 70, 300, 30)
        font1 = QtGui.QFont("Arial", 14)
        self.comboBox.setFont(font1)
        c = conn.cursor()
        c.execute('select * from SUBJECTS')
        rows = c.fetchall()
        for row in rows:
            self.comboBox.addItem(row[0])

        # Section
        l_section = QtWidgets.QLabel(self)
        l_section.setAlignment(QtCore.Qt.AlignCenter)
        l_section.setGeometry(QtCore.QRect(150, 140, 130, 30))
        l_section.setStyleSheet("QLabel { background-color : gray;color :black ; }")
        font = QtGui.QFont("Times", 14, QtGui.QFont.Bold)
        l_section.setFont(font)
        l_section.setText("Section")

        self.e_section = QtWidgets.QLineEdit(self)
        self.e_section.setGeometry(290, 140, 300, 30)
        self.e_section.setAlignment(QtCore.Qt.AlignCenter)
        font1 = QtGui.QFont("Arial", 14)
        self.e_section.setFont(font1)

        # Taking date
        l_calendar = QtWidgets.QLabel(self)
        l_calendar.setAlignment(QtCore.Qt.AlignCenter)
        l_calendar.setGeometry(QtCore.QRect(150, 210, 130, 30))
        l_calendar.setStyleSheet("QLabel { background-color : gray;color :black ; }")
        l_calendar.setFont(font)
        l_calendar.setText("Date")

        # Choose Date
        self.calendar = QtWidgets.QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.setGeometry(290, 210, 300, 160)
        self.calendar.clicked[QtCore.QDate].connect(self.showDate)

        button_search = QtWidgets.QPushButton(self)
        button_search.setText("SEARCH")
        button_search.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        button_search.setGeometry(600, 210, 100, 30)
        button_search.setStyleSheet("QPushButton { background-color : orange ;color : white ; }")
        # self.entries = [self.e_student_id]
        button_search.clicked.connect(self.search)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(270, 400, 330, 200)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Name', 'Attendance'])
        self.selected_subject = self.comboBox.currentText()
        self.comboBox.activated.connect(self.handleActivated)

        # # Button for clearing fields
        # button_reset = QtWidgets.QPushButton(self)
        # button_reset.setText("RESET")
        # button_reset.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        # button_reset.setGeometry(480, 600, 100, 30)
        # button_reset.setStyleSheet("QPushButton { background-color : red ;color : white ; }")
        # # self.entries = [self.e_section, self.e_student_id]
        # # button_reset.clicked.connect(self.erase)
        #
        # # Button for submission of data and storing in database
        # button_submit = QtWidgets.QPushButton(self)
        # button_submit.setText("SUBMIT")
        # button_submit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        # button_submit.setGeometry(350, 600, 100, 30)
        # button_submit.setStyleSheet("QPushButton { background-color : green;color : white ; }")
        # # button_submit.clicked.connect(self.submit)

        self.l_message = QtWidgets.QLabel(self)
        self.l_message.setAlignment(QtCore.Qt.AlignCenter)
        self.l_message.setStyleSheet("QLabel { color:green ; }")
        self.l_message.setFont(QtGui.QFont('Times', 13))
        self.l_message.setGeometry(QtCore.QRect(280, 500, 350, 30))

    def populateTable(self):
        self.l_message.setText("")
        self.tableWidget.setRowCount(0)
        try:
            c.execute(
                'select first_name, student_id from sub_sec_stu inner join students on sub_sec_stu.student = students.student_id where subject="%s" and section ="%s"' % (
                    self.selected_subject, self.e_section.text()))
        except:
            print("error")
        students_ids = []
        students_names = []
        rows = c.fetchall()
        for row in rows:
            print(type(row[1]), row[1])
            students_names.append(row[0])
            students_ids.append(row[1])

        c.execute('select student_id, present from attendance where subject="%s" and date ="%s"' % (
            self.selected_subject, self.py_date))
        students_present = []
        for i in c.fetchall():
            students_present.append(i[0])

        for id in students_ids:
            if id not in students_present:
                print(id, 'not in presence list')
                c.execute('REPLACE INTO ATTENDANCE (date,student_id,subject,present,excused) VALUES(?,?,?,?,?)',
                          (self.py_date, id, self.selected_subject, 0, 0))
                conn.commit()

        c.execute('select student_id, present from attendance where subject="%s" and date ="%s"' % (
            self.selected_subject, self.py_date))
        result = c.fetchall()
        for row_num, row_data in enumerate(result):
            if row_data[0] in students_ids:
                self.tableWidget.insertRow(row_num)
                index = students_ids.index(int(row_data[0]))
                name = students_names[index]
                present = "Present" if row_data[1] == 1 else "Absent"
                self.tableWidget.setItem(row_num, 0, QTableWidgetItem(str(row_data[0])))
                self.tableWidget.setItem(row_num, 1, QTableWidgetItem(name))
                self.tableWidget.setItem(row_num, 2, QTableWidgetItem(present))

    def handleActivated(self):
        self.selected_subject = self.comboBox.currentText()

    def erase(self):
        self.l_message.setText("")
        for entry in self.entries:
            entry.clear()

    def search(self):
        if self.e_section.text() == "" or self.py_date is None:
            self.l_message.setText("Please choose a Section and a Date")
        else:
            # try:
            self.populateTable()
            # except:
            #     print('Error')

    def showDate(self, d):
        print(d.toString())
        self.py_date = str(d.toPyDate())
        print(self.py_date)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = CheckAttendance()
    gui.show()
    app.exec_()
