
import cv2
import sys
from path import *

from PyQt5.QtCore import QObject, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap


global image_num
image_num = 1

global index
index = 0

cam_list = cam_path()
print(cam_list)

class ShowVideo(QObject):
    VideoSignal = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self):
        super(ShowVideo, self).__init__()

        global index

        print(index, "This is index!!!!")
        print(cam_list[index], "---This is cam_list[index]")

        self.camera = cv2.VideoCapture(str(cam_list[index]))

        ret, image = self.camera.read()
        self.height, self.width = image.shape[:2]

        index += 1
    

    @QtCore.pyqtSlot()
    def startVideo(self):

        while True:
            ret, image = self.camera.read()
            color_swapped_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            qt_image1 = QtGui.QImage(color_swapped_image.data,
                                    self.width,
                                    self.height,
                                    color_swapped_image.strides[0],
                                    QtGui.QImage.Format_RGB888)
            self.VideoSignal.emit(qt_image1)

            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(25, loop.quit) #25 ms
            loop.exec_()

class ImageViewer(QtWidgets.QWidget):
    def __init__(self):
        super(ImageViewer, self).__init__()
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def initUI(self):
        self.setWindowTitle('Test')

    @QtCore.pyqtSlot(QtGui.QImage)


    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()


#################################


class image(QWidget):
    def __init__(self):
        super().__init__()

        global image_num
    
        self.initUI()
        image_num += 1

    def initUI(self):

        global image_num

        image_path = "./image/apple"+str(image_num)+".jpeg"
        print(image_path, "->This is image_path")
        pixmap = QPixmap(image_path)

        label = QLabel()
        label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    img1 = image()
    img2 = image()
    img3 = image()


    push_button = QtWidgets.QPushButton('Start')
    vertical_layout = QtWidgets.QVBoxLayout()
    horizontal_layout1 = QtWidgets.QHBoxLayout()
    horizontal_layout2 = QtWidgets.QHBoxLayout()
    vertical_layout.addLayout(horizontal_layout1)
    
    vertical_layout.addLayout(horizontal_layout2)
    vertical_layout.addWidget(push_button)

    horizontal_layout2.addWidget(img1)
    horizontal_layout2.addWidget(img2)
    horizontal_layout2.addWidget(img3)

    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(vertical_layout)

    main_window = QtWidgets.QMainWindow()
    main_window.setCentralWidget(layout_widget)
    
    # video 1
    index = 0
    thread = QtCore.QThread()
    thread.start()
    vid = ShowVideo()
    vid.moveToThread(thread)
    image_viewer1 = ImageViewer()
    vid.VideoSignal.connect(image_viewer1.setImage)
    push_button.clicked.connect(vid.startVideo)
    horizontal_layout1.addWidget(image_viewer1)
    

    # video 2
    if len(cam_list) > 1: 
        index = 1
        thread2 = QtCore.QThread()
        thread2.start()
        vid2 = ShowVideo()
        vid2.moveToThread(thread2)
        image_viewer2 = ImageViewer()
        vid2.VideoSignal.connect(image_viewer2.setImage)
        push_button.clicked.connect(vid2.startVideo)
        horizontal_layout1.addWidget(image_viewer2)
    # video 3
    if len(cam_list) > 2: 
        index = 2
        thread3 = QtCore.QThread()
        thread3.start()
        vid3 = ShowVideo()
        vid3.moveToThread(thread3)
        image_viewer3 = ImageViewer()
        vid3.VideoSignal.connect(image_viewer3.setImage)
        push_button.clicked.connect(vid3.startVideo)
        horizontal_layout1.addWidget(image_viewer3)
    
    

    main_window.show()
    sys.exit(app.exec_())
