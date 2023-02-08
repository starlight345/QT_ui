
import cv2
import sys
from path import *

from PyQt5.QtCore import QObject
from PyQt5 import QtCore, QtGui, QtWidgets


index = 0
first_flag = 0
cam_list = cam_path()

print(cam_list)

class ShowVideo(QObject):
    global index
    print(index, "This is index")

    print(cam_list[index], "---This is cam_list[index]")
    camera = cv2.VideoCapture(str(cam_list[index]))

    ret, image = camera.read()
    height, width = image.shape[:2]

    VideoSignal = QtCore.pyqtSignal(QtGui.QImage)



    def __init__(self):
        global index
        super(ShowVideo, self).__init__()
        index += 1
    print(index, "This is index")
    

    @QtCore.pyqtSlot()

    def startVideo(self):
        global image

        run_video = True
        while run_video:
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



'''
class ShowVideo2(QObject):

    camera = cv2.VideoCapture()
    ret, image = camera.read()
    height, width = image.shape[:2]

    VideoSignal = QtCore.pyqtSignal(QtGui.QImage)


    @QtCore.pyqtSlot()
    def startVideo(self):
        global image

        run_video = True
        while run_video:
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

class ShowVideo3(QObject):

    camera = cv2.VideoCapture(cam_path("33594229"))
    ret, image = camera.read()
    height, width = image.shape[:2]

    VideoSignal = QtCore.pyqtSignal(QtGui.QImage)


    @QtCore.pyqtSlot()
    def startVideo(self):
        global image

        run_video = True
        while run_video:
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
'''
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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    




    push_button = QtWidgets.QPushButton('Start')
    vertical_layout = QtWidgets.QVBoxLayout()
    horizontal_layout = QtWidgets.QHBoxLayout()
    vertical_layout.addLayout(horizontal_layout)
    vertical_layout.addWidget(push_button)
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
    horizontal_layout.addWidget(image_viewer1)
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
        horizontal_layout.addWidget(image_viewer2)
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
        horizontal_layout.addWidget(image_viewer3)
    
    
    main_window.show()
    sys.exit(app.exec_())
