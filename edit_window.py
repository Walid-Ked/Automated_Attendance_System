import sqlite3
from PyQt5 import QtWidgets, QtGui, QtCore

conn = sqlite3.connect('Attendance System.db')
c = conn.cursor()


class EditWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.py_date = None
        self.st_num = None
        super(EditWindow, self).__init__()
        self.setGeometry(300, 50, 800, 600)
        self.setWindowTitle("Edit Attendance")
        self.setWindowIcon(QtGui.QIcon('other_images/logo.png'))
        self.selected_subject = None

        # Heading
        h = QtWidgets.QLabel(self)
        h.setAlignment(QtCore.Qt.AlignCenter)
        h.setGeometry(QtCore.QRect(100, 20, 600, 50))
        h.setStyleSheet("QLabel { background-color : blue;color :white ; }")
        font = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        h.setFont(font)
        h.setText("Edit Attendance")

        # Result
        self.l_message = QtWidgets.QLabel(self)
        self.l_message.setAlignment(QtCore.Qt.AlignCenter)
        self.l_message.setGeometry(30, 90, 400, 30)
        self.l_message.setStyleSheet("QLabel { color:green ; }")
        self.l_message.setFont(QtGui.QFont('Times', 13))
        self.l_message.setText("Student: 12  ISM101  Date: 01/12/1962 (Absent)")

        # Checkbox
        self.attendance_checkbox = QtWidgets.QCheckBox('Attendance', self)
        self.attendance_checkbox.setChecked(True)
        self.attendance_checkbox.setGeometry(550, 90, 90, 30)
        self.attendance_checkbox.stateChanged.connect(self.checked_attendance)

        # Checkbox
        self.execuse_checkbox = QtWidgets.QCheckBox('Execuse', self)
        self.execuse_checkbox.setChecked(True)
        self.execuse_checkbox.move(650, 90)
        self.execuse_checkbox.stateChanged.connect(self.checked_execuse)

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
        self.comboBox.activated.connect(self.handleActivated)
        self.selected_subject = self.comboBox.currentText()

        # Taking Student's id
        l_student_id = QtWidgets.QLabel(self)
        l_student_id.setAlignment(QtCore.Qt.AlignCenter)
        l_student_id.setGeometry(QtCore.QRect(150, 210, 130, 30))
        l_student_id.setStyleSheet("QLabel { background-color : gray;color :black ; }")
        l_student_id.setFont(font)
        l_student_id.setText("Student")

        self.e_student_id = QtWidgets.QLineEdit(self)
        self.e_student_id.setGeometry(290, 210, 300, 30)
        self.e_student_id.setAlignment(QtCore.Qt.AlignCenter)
        self.e_student_id.setFont(font1)

        # Button for Search
        button_search = QtWidgets.QPushButton(self)
        button_search.setText("SEARCH")
        button_search.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        button_search.setGeometry(600, 210, 100, 30)
        button_search.setStyleSheet("QPushButton { background-color : orange ;color : white ; }")
        self.entries = [self.e_student_id]
        button_search.clicked.connect(self.search)

        # Taking date
        l_calendar = QtWidgets.QLabel(self)
        l_calendar.setAlignment(QtCore.Qt.AlignCenter)
        l_calendar.setGeometry(QtCore.QRect(150, 270, 130, 30))
        l_calendar.setStyleSheet("QLabel { background-color : gray;color :black ; }")
        l_calendar.setFont(font)
        l_calendar.setText("Date")

        # Choose Date
        self.calendar = QtWidgets.QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.setGeometry(290, 260, 300, 160)
        self.calendar.clicked[QtCore.QDate].connect(self.showDate)

        # Button for clearing fields
        button_reset = QtWidgets.QPushButton(self)
        button_reset.setText("RESET")
        button_reset.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        button_reset.setGeometry(480, 450, 100, 30)
        button_reset.setStyleSheet("QPushButton { background-color : red ;color : white ; }")
        self.entries = [self.e_student_id]
        button_reset.clicked.connect(self.erase)

        # Button for submission of data and storing in database
        button_submit = QtWidgets.QPushButton(self)
        button_submit.setText("SUBMIT")
        button_submit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        button_submit.setGeometry(350, 450, 100, 30)
        button_submit.setStyleSheet("QPushButton { background-color : green;color : white ; }")
        button_submit.clicked.connect(self.submit)

        self.erase()

    def handleActivated(self):
        self.selected_subject = self.comboBox.currentText()

    def erase(self):
        self.l_message.setText("")
        self.attendance_checkbox.setChecked(False)
        self.execuse_checkbox.setChecked(False)
        for entry in self.entries:
            entry.clear()

    def showDate(self, d):
        print(d.toString())
        self.py_date = str(d.toPyDate())
        print(self.py_date)

    def checked_attendance(self):
        pass

    def checked_execuse(self):
        pass

    def search(self):
        try:
            print(self.py_date)
            print(self.selected_subject)
            self.st_num = int(self.e_student_id.text())
            print(self.st_num)
            c.execute(' select * from attendance where student_id=%d and subject="%s" and date= "%s"' % (
                self.st_num, self.selected_subject, self.py_date))
            result = c.fetchone()
            presence = result[3]
            presence_text = "Present" if presence == 1 else "Absent"
            execuse = result[4]
            self.attendance_checkbox.setChecked(True) if presence == 1 else self.attendance_checkbox.setChecked(False)
            self.execuse_checkbox.setChecked(True) if execuse == 1 else self.execuse_checkbox.setChecked(False)
            self.l_message.setText(
                '%d   |  %s  |  %s  |  (%s)' % (self.st_num, self.selected_subject, self.py_date, presence_text))
            print(result)
        except:
            print("error")

    def submit(self):
        if self.selected_subject is None or self.py_date is None or self.st_num is None:
            self.l_message.setText("Error !!! ")
        else:
            try:
                int_presence = 1 if self.attendance_checkbox.isChecked() else 0
                int_excuse = 1 if self.execuse_checkbox.isChecked() else 0
                print(int_presence)
                print(int_excuse)
                c.execute('REPLACE INTO ATTENDANCE (date,student_id,subject,present,excused) VALUES(?,?,?,?,?)',
                          (self.py_date, self.st_num, self.selected_subject, int_presence, int_excuse))
                conn.commit()
                self.l_message.setText('Submited Succefully')
            except:
                print("Error occured while editing")


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = EditWindow()
    gui.show()
    app.exec_()
