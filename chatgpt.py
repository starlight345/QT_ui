import sys
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QLabel
from PyQt5.QtCore import Qt, QTimer
import time
class WebcamWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multiple Webcams and Images")
        self.setGeometry(100, 100, 900, 900)
        self.graphics_views = [QGraphicsView(self) for _ in range(3)]
        self.graphics_scenes = [QGraphicsScene() for _ in range(3)]
        self.image_labels = [QLabel(self) for _ in range(3)]
        self.caps = [cv2.VideoCapture(0), cv2.VideoCapture(2), cv2.VideoCapture(4)]
        self.grade = 1
        offset = 20
        for i in range(3):
            self.graphics_views[i].setScene(self.graphics_scenes[i])
            self.graphics_views[i].setAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.graphics_views[i].setGeometry(i * (300 + offset), 0, 300, 300)
            self.image_labels[i].setGeometry(i * (300 + offset), 300, 300, 300)
            label = QLabel(self)
            label.setGeometry(i * (300 + offset), 600, 300, 50)
            label.setText("Upperview")
        self.grade_label = QLabel(self)
        self.grade_label.setGeometry(300, 650, 300, 50)
        self.update_grade_label()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frames)
        self.timer.start(30)
    def update_frames(self):
        for i in range(1):
            ret, frame = self.caps[i].read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pix = QPixmap.fromImage(q_img)
            self.graphics_scenes[i].clear()
            self.graphics_scenes[i].addPixmap(pix)
            self.image_labels[i].setPixmap(QPixmap("image/apple{}.jpeg".format(i + 1)))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_grade_label)
        self.timer.start(3000)
    def update_grade_label(self):
        self.grade_label.setText("Grade : "+ str(self.grade))
        time.sleep(2)
        self.grade += 1
if __name__ == "__main__":
    for i in range(3):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print("Camera with index {} is working.".format(i))
        else:
            print("Camera with index {} is not working.".format(i))
    app = QApplication(sys.argv)
    window = WebcamWindow()
    window.show()
    sys.exit(app.exec_())