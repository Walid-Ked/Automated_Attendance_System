import sqlite3
import time
from os import listdir

import cv2
import numpy as np
from PIL import Image
from PyQt5 import QtGui, QtCore, QtWidgets
from numpy import asarray, savez_compressed
from sklearn.preprocessing import Normalizer
from tensorflow.keras.models import load_model


class RegistrationWindow(QtWidgets.QMainWindow):
    # Registration window for student registration

    def __init__(self):
        super(RegistrationWindow, self).__init__()
        self.model = None

        # Creating Registration Window
        self.setGeometry(200, 25, 1000, 695)
        self.setWindowTitle("Registration")
        self.setWindowIcon(QtGui.QIcon('other_images/logo.png'))

        # Heading
        h = QtWidgets.QLabel(self)
        h.setAlignment(QtCore.Qt.AlignCenter)
        h.setGeometry(QtCore.QRect(100, 30, 600, 60))
        h.setStyleSheet("QLabel { background-color : blue;color :white ; }")
        font = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        h.setFont(font)
        h.setText("REGISTRATION")

        # Pseudo photo ID to be replaced by Student's Photo
        self.pic = QtWidgets.QLabel(self)
        self.pic.setGeometry(50, 120, 320, 320)
        self.pic.setPixmap(QtGui.QPixmap("other_images/default.png"))

        # Button for opening Webcam and take photo
        b = QtWidgets.QPushButton(self)
        b.setText("CLICK")
        b.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        b.setGeometry(100, 440, 100, 30)
        b.clicked.connect(self.take_photo)

        # SET OF ENTRIES
        # Taking Student's Name
        l_name = QtWidgets.QLabel(self)
        l_name.setAlignment(QtCore.Qt.AlignCenter)
        l_name.setGeometry(QtCore.QRect(310, 150, 150, 30))
        l_name.setStyleSheet("QLabel { background-color : gray;color :black ; }")
        font = QtGui.QFont("Times", 14, QtGui.QFont.Bold)
        l_name.setFont(font)
        l_name.setText("First Name")

        self.e_name = QtWidgets.QLineEdit(self)
        self.e_name.setGeometry(470, 150, 300, 30)
        self.e_name.setAlignment(QtCore.Qt.AlignCenter)
        font1 = QtGui.QFont("Arial", 14)
        self.e_name.setFont(font1)

        # Taking Student's Last Name
        l_last_name = QtWidgets.QLabel(self)
        l_last_name.setAlignment(QtCore.Qt.AlignCenter)
        l_last_name.setGeometry(QtCore.QRect(310, 250, 150, 30))
        l_last_name.setStyleSheet("QLabel { background-color : gray;color :black ; }")
        font = QtGui.QFont("Times", 14, QtGui.QFont.Bold)
        l_last_name.setFont(font)
        l_last_name.setText("Last Name")

        self.e_last_name = QtWidgets.QLineEdit(self)
        self.e_last_name.setGeometry(470, 250, 300, 30)
        self.e_last_name.setAlignment(QtCore.Qt.AlignCenter)
        font1 = QtGui.QFont("Arial", 14)
        self.e_last_name.setFont(font1)

        # Taking Student's id
        l_student_id = QtWidgets.QLabel(self)
        l_student_id.setAlignment(QtCore.Qt.AlignCenter)
        l_student_id.setGeometry(QtCore.QRect(310, 350, 150, 30))
        l_student_id.setStyleSheet("QLabel { background-color : gray;color :black ; }")
        l_student_id.setFont(font)
        l_student_id.setText("Student ID")

        self.e_student_id = QtWidgets.QLineEdit(self)
        self.e_student_id.setGeometry(470, 350, 300, 30)
        self.e_student_id.setAlignment(QtCore.Qt.AlignCenter)
        self.e_student_id.setFont(font1)

        # Taking Student's email
        l_email = QtWidgets.QLabel(self)
        l_email.setAlignment(QtCore.Qt.AlignCenter)
        l_email.setGeometry(QtCore.QRect(310, 450, 150, 30))
        l_email.setStyleSheet("QLabel { background-color : gray;color :black ; }")
        l_email.setFont(font)
        l_email.setText("E-mail")

        self.e_email = QtWidgets.QLineEdit(self)
        self.e_email.setGeometry(470, 450, 300, 30)
        self.e_email.setAlignment(QtCore.Qt.AlignCenter)
        self.e_email.setFont(font1)

        # Taking Student's Phone Number
        l_phone_number = QtWidgets.QLabel(self)
        l_phone_number.setAlignment(QtCore.Qt.AlignCenter)
        l_phone_number.setGeometry(QtCore.QRect(310, 550, 150, 30))
        l_phone_number.setStyleSheet("QLabel { background-color : gray;color :black ; }")
        l_phone_number.setFont(font)
        l_phone_number.setText("Phone Number")

        self.e_phone_number = QtWidgets.QLineEdit(self)
        self.e_phone_number.setGeometry(470, 550, 300, 30)
        self.e_phone_number.setAlignment(QtCore.Qt.AlignCenter)
        self.e_phone_number.setFont(font1)

        # Button for clearing fields
        button_reset = QtWidgets.QPushButton(self)
        button_reset.setText("RESET")
        button_reset.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        button_reset.setGeometry(650, 650, 100, 30)
        button_reset.setStyleSheet("QPushButton { background-color : red ;color : white ; }")
        self.entries = [self.e_name, self.e_student_id, self.e_email, self.e_last_name, self.e_phone_number]
        button_reset.clicked.connect(self.erase)

        # Button for training
        button_reset = QtWidgets.QPushButton(self)
        button_reset.setText("TRAIN")
        button_reset.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        button_reset.setGeometry(780, 650, 100, 30)
        button_reset.setStyleSheet("QPushButton { background-color : orange ;color : white ; }")
        button_reset.clicked.connect(self.train)

        # Label for displaying message
        self.l_message = QtWidgets.QLabel(self)
        self.l_message.setAlignment(QtCore.Qt.AlignCenter)
        self.l_message.setStyleSheet("QLabel { color:green ; }")
        self.l_message.setFont(QtGui.QFont('Times', 13))

        # Button for submission of data and storing in database
        button_submit = QtWidgets.QPushButton(self)
        button_submit.setText("SUBMIT")
        button_submit.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        button_submit.setGeometry(520, 650, 100, 30)
        button_submit.setStyleSheet("QPushButton { background-color : green;color : white ; }")
        button_submit.clicked.connect(self.store_in_database)

    def erase(self):
        # function for clearing fields and changing to default
        for entry in self.entries:
            entry.clear()
        self.pic.setPixmap(QtGui.QPixmap("other_images/default.png"))
        self.l_message.setText("")

    def draw_border_one(self, img, point1, point2, point3, point4, line_length):

        x1, y1 = point1
        x2, y2 = point2
        x3, y3 = point3
        x4, y4 = point4

        cv2.circle(img, (x1, y1), 1, (255, 255, 255), -1)  # -- top_left
        cv2.circle(img, (x2, y2), 1, (255, 255, 255), -1)  # -- bottom-left
        cv2.circle(img, (x3, y3), 1, (255, 255, 255), -1)  # -- top-right
        cv2.circle(img, (x4, y4), 1, (255, 255, 255), -1)  # -- bottom-right

        cv2.line(img, (x1, y1), (x1, y1 + line_length), (255, 255, 255), 2)  # -- top-left
        cv2.line(img, (x1, y1), (x1 + line_length, y1), (255, 255, 255), 2)

        cv2.line(img, (x2, y2), (x2, y2 - line_length), (255, 255, 255), 2)  # -- bottom-left
        cv2.line(img, (x2, y2), (x2 + line_length, y2), (255, 255, 255), 2)

        cv2.line(img, (x3, y3), (x3 - line_length, y3), (255, 255, 255), 2)  # -- top-right
        cv2.line(img, (x3, y3), (x3, y3 + line_length), (255, 255, 255), 2)

        cv2.line(img, (x4, y4), (x4, y4 - line_length), (255, 255, 255), 2)  # -- bottom-right
        cv2.line(img, (x4, y4), (x4 - line_length, y4), (255, 255, 255), 2)

    def draw_border(self, img, pt1, pt2, color, thickness, r, d):
        x1, y1 = pt1
        x2, y2 = pt2

        # Top left
        cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
        cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
        cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)

        # Top right
        cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
        cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
        cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)

        # Bottom left
        cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
        cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
        cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)

        # Bottom right
        cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
        cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
        cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)

    def take_photo(self):
        # Function for clicking,displaying and storing photo
        check_value = self.check()
        if (check_value == 1):
            self.l_message.setGeometry(QtCore.QRect(40, 500, 250, 30))
            self.l_message.setText("Check the Name and Last Name")
        elif (check_value == 2):
            self.l_message.setGeometry(QtCore.QRect(40, 500, 250, 30))
            self.l_message.setText("Check the ID")
        elif (check_value == 3):
            self.l_message.setGeometry(QtCore.QRect(40, 500, 250, 30))
            self.l_message.setText("Check the Email Address")
        elif (check_value == 4):
            self.l_message.setGeometry(QtCore.QRect(40, 500, 250, 30))
            self.l_message.setText("Check the Phone Number")
        else:
            directory = 'registration_images'
            face_cascade = cv2.CascadeClassifier('support_files/haarcascade_frontalface_default.xml')
            cap = cv2.VideoCapture(1)
            while True:
                ret, img = cap.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                face = face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in face:
                    roi_color = img[y:y + h, x:x + w]
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 1, 1)
                    # cv2.line(img, (x-10, y + h - 5), (x - 80, y + h - 5), (255, 255, 255), 1)
                    # cv2.circle(img, (x - 82, y + h - 5), 1, (255, 255, 0), 1)
                    # cv2.putText(img, 'Walid', (x - 150, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    # cv2.line(img, (x - 10, y + h - 100), (x - 80, y + h - 150), (255, 255, 255), 1)
                    # cv2.circle(img, (x - 82, y + h - 150), 1, (255, 255, 0), 1)
                    # cv2.putText(img, '27', (x - 120, y + h - 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    self.draw_border(img, (x, y), (x + w, y + h), (255, 55, 255), 3, 10, 8)
                    self.draw_border_one(img, (x, y), (x, y + h), (x + w, y), (x + w, y + h), 15)
                    image_path = directory + '\\' + str(self.e_student_id.text() + '.png')
                    cv2.imwrite(image_path, roi_color)

                cv2.imshow('img', img)
                k = cv2.waitKey(30) & 0xff
                if k == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()
            self.pic.setPixmap(QtGui.QPixmap(str('registration_images\\' +
                                                 str(self.e_student_id.text()) + '.png')))

    def load_dataset(self):
        X, y = list(), list()
        for filename in listdir('registration_images'):
            print(filename.split(".")[0])
            y.append(filename.split('.')[0])
            image = Image.open('registration_images/' + filename)
            image = image.convert('RGB')
            image = image.resize((160, 160))
            pixels = asarray(image)
            print(pixels.shape)
            X.append(pixels)
            savez_compressed('dataset.npz', X, y)

    def train(self):
        self.l_message.setText("Training in progress .......")
        time.sleep(2)
        self.model = load_model('facenet_keras.h5')
        data = np.load('dataset.npz')
        X, y = data['arr_0'], data['arr_1']
        print('Loaded: ', X.shape, y.shape)
        newX = list()
        for face_pixels in X:
            embedding = self.get_embedding(self.model, face_pixels)
            newX.append(embedding)

        in_encoder = Normalizer(norm='l2')
        newX = asarray(newX)
        newX = in_encoder.transform(newX)
        print(newX.shape)
        savez_compressed('dataset-embeddings.npz', newX, y)
        self.l_message.setText("Training Done !!!")

    def get_embedding(self, model, face_pixels):
        face_pixels = face_pixels.astype('float32')
        mean, std = face_pixels.mean(), face_pixels.std()
        face_pixels = (face_pixels - mean) / std
        samples = np.expand_dims(face_pixels, axis=0)
        yhat = model.predict(samples)
        return yhat[0]

    def store_in_database(self):
        check_value = self.check()
        print('>>', check_value)
        if (check_value == 0):
            conn = sqlite3.connect('Attendance System.db')
            c = conn.cursor()
            first_name = self.e_name.text()
            last_name = self.e_last_name.text()
            student_id = int(self.e_student_id.text())
            email = self.e_email.text()
            phone = int(self.e_phone_number.text())

            c.execute('REPLACE INTO STUDENTS (student_id,first_name,last_name,phone,email) VALUES(?,?,?,?,?)',
                      (student_id, first_name, last_name, phone, email))
            conn.commit()
            c.close()
            conn.close()
            # Displaying message after successful submission
            self.l_message.setGeometry(QtCore.QRect(40, 500, 250, 30))
            self.erase()
            time.sleep(1)
            self.load_dataset()
            self.l_message.setText("Successfully Registered")
        elif (check_value == 1):
            self.l_message.setGeometry(QtCore.QRect(40, 500, 250, 30))
            self.l_message.setText("Invalid Name")
        elif (check_value == 2):
            self.l_message.setGeometry(QtCore.QRect(40, 500, 250, 30))
            self.l_message.setText("Check the student ID")
        elif (check_value == 3):
            self.l_message.setGeometry(QtCore.QRect(40, 500, 250, 30))
            self.l_message.setText("Check the Email Address")
        elif (check_value == 4):
            self.l_message.setGeometry(QtCore.QRect(40, 500, 250, 30))
            self.l_message.setText("Check the phone number")

    def check(self):
        name = self.e_name.text()
        if (len(name) == 0):
            return 1

        for i in range(10):
            if (str(i) in name):
                return 1

        last_name = self.e_last_name.text()
        if (len(last_name) == 0):
            return 1

        for i in range(10):
            if (str(i) in last_name):
                return 1

        try:
            student_id = int(self.e_student_id.text())
            # if (student_id < 1 or student_id > 100):
            #     return 2
        except:
            return 2

        try:
            email = self.e_email.text()
        except:
            return 3

        try:
            phone_number = int(self.e_phone_number.text())
        except:
            return 4

        try:
            img = cv2.imread('registration_images' + '\\' + str(student_id) + '.png', 0)
            face_cascade = cv2.CascadeClassifier('support_files/haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(img, 1.3, 5)
            print(len(faces), 'face(s) detected')
            if (len(faces) != 1):
                return 5
        except:
            return 5

        return 0


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = RegistrationWindow()
    gui.show()
    app.exec_()
