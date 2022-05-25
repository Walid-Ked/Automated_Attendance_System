import sqlite3
from datetime import date

import cv2
import numpy as np
from PIL import Image
from PyQt5 import QtWidgets, QtGui, QtCore
from sklearn.preprocessing import Normalizer
from sklearn.svm import SVC
from tensorflow.keras.models import load_model

from check_attendance import CheckAttendance

conn = sqlite3.connect('Attendance System.db')
c = conn.cursor()


class AttendanceWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AttendanceWindow, self).__init__()
        print("[INFO] loading model...")
        self.model = SVC(kernel='linear', probability=True)
        self.embedding_model = load_model('facenet_keras.h5')
        print('Loaded Model')
        self.train()

        self.today_date = date.today()
        self.students_names = []
        self.students_ids = []

        self.setGeometry(300, 50, 800, 600)
        self.setWindowTitle("Attendance")
        self.setWindowIcon(QtGui.QIcon('other_images/logo.png'))

        self.selected_subject = None

        # Heading
        h = QtWidgets.QLabel(self)
        h.setAlignment(QtCore.Qt.AlignCenter)
        h.setGeometry(QtCore.QRect(200, 20, 400, 50))
        h.setStyleSheet("QLabel { background-color : blue;color :white ; }")
        font = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        h.setFont(font)
        h.setText("ATTENDANCE")

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

        # Recording Button
        b1 = QtWidgets.QPushButton(self)
        b1.setText("RECORD AND MARK")
        b1.setStyleSheet("QPushButton { background-color : gray;color : black ; }")
        b1.setFont(font)
        b1.setGeometry(250, 300, 300, 50)
        b1.clicked.connect(self.record_mark)

        # Check Attendance button to check specific subject's Attendance
        b2 = QtWidgets.QPushButton(self)
        b2.setText("CHECK ATTENDANCE")
        b2.setStyleSheet("QPushButton { background-color : gray;color : black ; }")
        b2.setFont(font)
        b2.setGeometry(250, 425, 300, 50)
        b2.clicked.connect(self.create_check_attendance)

        self.get_students_list()

    def handleActivated(self):
        self.selected_subject = self.comboBox.currentText()

    def get_students_list(self):
        q = 'select student_id, first_name from students'
        c.execute(q)
        rows = c.fetchall()
        for row in rows:
            self.students_names.append(row[1])
            self.students_ids.append(row[0])
        print(self.students_ids)
        print(self.students_names)

    def train(self):
        data = np.load('dataset-embeddings.npz')
        trainX, trainy = data['arr_0'], data['arr_1']
        self.model.fit(trainX, trainy)

    def record_mark(self):
        print("[INFO] starting video stream...")
        face_cascade = cv2.CascadeClassifier('support_files/haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(1)

        while True:
            ret, frame = cap.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                roi = frame[y:y + h, x:x + w]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 100), 2, 2)
                roi = Image.fromarray(roi)
                roi = roi.resize((160, 160))
                roi = np.asarray(roi)
                embedding = self.get_embedding(self.embedding_model, roi)
                in_encoder = Normalizer(norm='l2')
                roi = np.expand_dims(roi, axis=0)
                embedding = in_encoder.transform(np.expand_dims(embedding, axis=0))
                prediction = self.model.predict(embedding)
                # prob = self.model.predict_proba(embedding)
                class_index = int(prediction[0])
                # class_probability = prob[0, class_index] * 100
                # print(class_probability)
                print(class_index)
                try:
                    for i, id in enumerate(self.students_ids):
                        if id == class_index:
                            student_name = self.students_names[i]
                            print(student_name)
                            cv2.putText(frame, student_name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                                        (0, 0, 255), 2)
                            self.insert_attendance(id, self.selected_subject, self.today_date)
                except:
                    print("id not in the database")
            cv2.imshow("Frame", frame)
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                break
        conn.commit()
        cv2.destroyAllWindows()
        cap.release()

    def get_embedding(self, model, face_pixels):
        face_pixels = face_pixels.astype('float32')
        mean, std = face_pixels.mean(), face_pixels.std()
        face_pixels = (face_pixels - mean) / std
        samples = np.expand_dims(face_pixels, axis=0)
        yhat = model.predict(samples)
        return yhat[0]

    def insert_attendance(self, student_id, subject, date):
        print(str(date))
        c.execute('REPLACE INTO ATTENDANCE VALUES(?,?,?,?,?)', (str(date), student_id, subject, 1, 0))

    def create_check_attendance(self):
        self._check_attendance = CheckAttendance()
        self._check_attendance.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = AttendanceWindow()
    gui.show()
    app.exec_()
