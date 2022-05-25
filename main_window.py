import sqlite3

from PyQt5 import QtGui, QtCore, QtWidgets

from attendance_window import AttendanceWindow
from edit_window import EditWindow
from registration_window import RegistrationWindow
from subject_window import SubjectWindow

conn = sqlite3.connect('Attendance System.db')
conn.execute("PRAGMA foreign_keys = 1")
c = conn.cursor()
insert_flag = 0

c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='SUBJECTS' ''')
if c.fetchone()[0] == 1:
    insert_flag = 1

if insert_flag == 0:
    c.execute(
        'CREATE TABLE IF NOT EXISTS STUDENTS (student_id INT PRIMARY KEY , first_name TEXT, last_name TEXT, email TEXT, phone INT)')
    c.execute('CREATE TABLE IF NOT EXISTS SUBJECTS (subject TEXT PRIMARY KEY )')
    c.execute('CREATE TABLE IF NOT EXISTS SECTIONS (section TEXT PRIMARY KEY )')
    c.execute(
        'CREATE TABLE IF NOT EXISTS SUB_SEC_STU (student INT, subject TEXT, section TEXT, PRIMARY KEY (student, subject, section),'
        'FOREIGN KEY(student) REFERENCES STUDENTS(student_id), FOREIGN KEY(subject) REFERENCES SUBJECTS(subject), FOREIGN KEY(section) REFERENCES SECTIONS(section))')
    c.execute('''CREATE TABLE IF NOT EXISTS ATTENDANCE 
                (date TEXT, student_id INT, subject TEXT, present INT, excused INT, 
                 PRIMARY KEY (date, student_id, subject),
                 FOREIGN KEY (student_id) REFERENCES STUDENTS (student_id),
                 FOREIGN KEY (subject) REFERENCES SUBJECTS (subject)       
                )''')

    subjects = [("ISM101",), ("ISM113",), ("ISM112",), ("ISM224",), ("ISM326",), ("ISM467",), ("ISM433",), ("CS312",),
                ("CS421",), ("CS212",)]
    c.executemany('REPLACE INTO SUBJECTS VALUES(?)', subjects)

    sections = [("2455",), ("2456",), ("2457",), ("303",), ("304",), ("305",)]
    c.executemany('REPLACE INTO SECTIONS VALUES(?)', sections)

conn.commit()


class MainWindow(QtWidgets.QMainWindow):
    # Main Window of Interface
    def __init__(self):
        super(MainWindow, self).__init__()
        self._registration_window = None
        self._attendance_window = None
        self._subject_window = None
        self._edit_window = None
        self.setGeometry(300, 50, 800, 600)
        self.setWindowTitle("Automated Attendance System")
        self.setWindowIcon(QtGui.QIcon('other_images/logo.png'))

        # Heading
        h = QtWidgets.QLabel(self)
        h.setAlignment(QtCore.Qt.AlignCenter)
        h.setGeometry(QtCore.QRect(100, 30, 600, 60))
        h.setStyleSheet("QLabel { background-color : blue;color :white ; }")
        font = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        h.setFont(font)
        h.setText("AUTOMATED ATTENDANCE SYSTEM")

        # Registration Button for opening registration window
        b1 = QtWidgets.QPushButton(self)
        b1.setText("REGISTRATION")
        font1 = QtGui.QFont("Times", 16, QtGui.QFont.Bold)
        b1.setFont(font1)
        b1.setGeometry(450, 170, 250, 50)
        b1.setStyleSheet("QPushButton { background-color : gray;color :black ; }")
        b1.clicked.connect(self.create_registration_window)

        # Attendance Button for opening attendance window
        b2 = QtWidgets.QPushButton(self)
        b2.setText("ATTENDANCE")
        b2.setFont(font1)
        b2.setGeometry(450, 270, 250, 50)
        b2.setStyleSheet("QPushButton { background-color : gray;color :black ; }")
        b2.clicked.connect(self.create_attendance_window)

        # Subjects and sections
        b3 = QtWidgets.QPushButton(self)
        b3.setText("SUBJECTS/SECTIONS")
        b3.setFont(font1)
        b3.setGeometry(450, 370, 250, 50)
        b3.setStyleSheet("QPushButton { background-color : gray;color :black ; }")
        b3.clicked.connect(self.create_subject_window)

        # Edit Attendance
        b3 = QtWidgets.QPushButton(self)
        b3.setText("EDIT ATTENDANCE")
        b3.setFont(font1)
        b3.setGeometry(450, 470, 250, 50)
        b3.setStyleSheet("QPushButton { background-color : gray;color :black ; }")
        b3.clicked.connect(self.create_edit_window)

        # Adding Logo of college
        pic = QtWidgets.QLabel(self)
        pic.setGeometry(80, 150, 300, 350)
        pic.setPixmap(QtGui.QPixmap("other_images/logo.png"))

    def create_registration_window(self):
        # Function for opening Registration window
        self._registration_window = RegistrationWindow()
        self._registration_window.show()
        # self.close()

    def create_attendance_window(self):
        # Function for opening Attendance window
        self._attendance_window = AttendanceWindow()
        self._attendance_window.show()
        # self.close()

    def create_subject_window(self):
        # Function for opening Attendance window
        self._subject_window = SubjectWindow()
        self._subject_window.show()
        # self.close()

    def create_edit_window(self):
        # Function for opening Attendance window
        self._edit_window = EditWindow()
        self._edit_window.show()
        # self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = MainWindow()
    gui.show()
    app.exec_()
