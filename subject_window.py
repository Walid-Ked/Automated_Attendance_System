import sqlite3
from PyQt5 import QtWidgets, QtGui, QtCore
from view_window import ViewWindow

conn = sqlite3.connect('Attendance System.db')
c = conn.cursor()

class SubjectWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self._view_window = None
        super(SubjectWindow, self).__init__()
        self.setGeometry(300, 50, 800, 600)
        self.setWindowTitle("Subjects/Sections")
        self.setWindowIcon(QtGui.QIcon('other_images/logo.png'))
        self.selected_subject = None

        # Heading
        h = QtWidgets.QLabel(self)
        h.setAlignment(QtCore.Qt.AlignCenter)
        h.setGeometry(QtCore.QRect(100, 20, 600, 50))
        h.setStyleSheet("QLabel { background-color : blue;color :white ; }")
        font = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        h.setFont(font)
        h.setText("Add Students to Subjects and Sections")

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
        # self.comboBox.activated[str].connect(self.get_selected)

        # Section
        l_section = QtWidgets.QLabel(self)
        l_section.setAlignment(QtCore.Qt.AlignCenter)
        l_section.setGeometry(QtCore.QRect(150, 250, 130, 30))
        l_section.setStyleSheet("QLabel { background-color : gray;color :black ; }")
        font = QtGui.QFont("Times", 14, QtGui.QFont.Bold)
        l_section.setFont(font)
        l_section.setText("Section")

        self.e_section = QtWidgets.QLineEdit(self)
        self.e_section.setGeometry(290, 250, 300, 30)
        self.e_section.setAlignment(QtCore.Qt.AlignCenter)
        font1 = QtGui.QFont("Arial", 14)
        self.e_section.setFont(font1)

        # Taking Student's id
        l_student_id = QtWidgets.QLabel(self)
        l_student_id.setAlignment(QtCore.Qt.AlignCenter)
        l_student_id.setGeometry(QtCore.QRect(150, 350, 130, 30))
        l_student_id.setStyleSheet("QLabel { background-color : gray;color :black ; }")
        l_student_id.setFont(font)
        l_student_id.setText("Student ID")

        self.e_student_id = QtWidgets.QLineEdit(self)
        self.e_student_id.setGeometry(290, 350, 300, 30)
        self.e_student_id.setAlignment(QtCore.Qt.AlignCenter)
        self.e_student_id.setFont(font1)

        # Button for submission of data and storing in database
        button_submit = QtWidgets.QPushButton(self)
        button_submit.setText("SUBMIT")
        button_submit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        button_submit.setGeometry(300, 450, 100, 30)
        button_submit.setStyleSheet("QPushButton { background-color : green;color : white ; }")
        button_submit.clicked.connect(self.submit)

        # Button for clearing fields
        button_reset = QtWidgets.QPushButton(self)
        button_reset.setText("RESET")
        button_reset.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        button_reset.setGeometry(420, 450, 100, 30)
        button_reset.setStyleSheet("QPushButton { background-color : red ;color : white ; }")
        self.entries = [self.e_section, self.e_student_id]
        button_reset.clicked.connect(self.erase)

        # Button for viewing list of students
        button_submit = QtWidgets.QPushButton(self)
        button_submit.setText("VIEW")
        button_submit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        button_submit.setGeometry(540, 450, 100, 30)
        button_submit.setStyleSheet("QPushButton { background-color : blue;color : white ; }")
        button_submit.clicked.connect(self.view)

        self.l_message = QtWidgets.QLabel(self)
        self.l_message.setAlignment(QtCore.Qt.AlignCenter)
        self.l_message.setStyleSheet("QLabel { color:green ; }")
        self.l_message.setFont(QtGui.QFont('Times', 13))
        self.l_message.setGeometry(QtCore.QRect(280, 500, 350, 30))

    def erase(self):
        self.l_message.setText("")
        for entry in self.entries:
            entry.clear()

    def submit(self):
        section = self.e_section.text()
        student_id = int(self.e_student_id.text())
        subject = self.comboBox.currentText()
        c.execute('REPLACE INTO SUB_SEC_STU (student, subject, section) VALUES(?,?,?)', (student_id, subject, section))
        conn.commit()
        self.l_message.setText('Added Succefully')

    def view(self):
        self._view_window = ViewWindow()
        self._view_window.show()
        # self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = SubjectWindow()
    gui.show()
    app.exec_()
