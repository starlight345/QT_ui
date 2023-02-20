import sys
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QLabel
from PyQt5.QtCore import Qt, QTimer
import time
global grade
grade = 1

class WebcamWindow(QMainWindow):
    global grade
    def __init__(self):
        print("asdas")
        super().__init__()
        self.setWindowTitle("Multiple Webcams and Images")
        self.setGeometry(100, 100, 900, 900)
        self.graphics_views = [QGraphicsView(self) for _ in range(2)]
        self.graphics_scenes = [QGraphicsScene() for _ in range(2)]
        self.image_labels = [QLabel(self) for _ in range(2)]
        self.caps = [cv2.VideoCapture(0),cv2.VideoCapture(2)]
        for i in range(2):
            self.graphics_views[i].setScene(self.graphics_scenes[i])
            self.graphics_views[i].setAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.graphics_views[i].setGeometry(i * 300, 0, 300, 300)
            self.image_labels[i].setGeometry(i * 300, 300, 300, 300)
            label = QLabel(self)
            label.setGeometry(i * 300, 600, 300, 50)
            label.setText("Upperview")


        
        label = QLabel(self)
        label.setGeometry(300, 650, 300, 50)
        label.setText("Grade : "+ str(grade))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frames)
        self.timer.start(30)
        
    def update_frames(self):
        global grade
        for i in range(2):
            ret, frame = self.caps[i].read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pix = QPixmap.fromImage(q_img)
            self.graphics_scenes[i].clear()
            self.graphics_scenes[i].addPixmap(pix)
            self.image_labels[i].setPixmap(QPixmap("image/apple{}.jpeg".format(i + 1)))
            

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    window = WebcamWindow()
    window.show()
    sys.exit(app.exec_())

        

