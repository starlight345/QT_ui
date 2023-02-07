
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject
import sys

import cv2

class ShowVideo(QObject):

    camera = cv2.VideoCapture(0)
    ret, image = camera.read()
    height, width = image.shape[:2]

    VideoSignal = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self):
        super(ShowVideo, self).__init__()

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

class ShowVideo2(QObject):

    camera = cv2.VideoCapture(2)
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

    camera = cv2.VideoCapture(4)
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


    thread = QtCore.QThread()
    thread.start()
    
    thread2 = QtCore.QThread()
    thread2.start()

    thread3 = QtCore.QThread()
    thread3.start()

    # video 1
    vid = ShowVideo()
    vid.moveToThread(thread)
    # video 2
    vid2 = ShowVideo2()
    vid2.moveToThread(thread2)
    # video 3
    vid3 = ShowVideo2()
    vid3.moveToThread(thread3)
    
    image_viewer1 = ImageViewer()
    image_viewer2 = ImageViewer()
    image_viewer3 = ImageViewer()

    vid.VideoSignal.connect(image_viewer1.setImage)
    vid2.VideoSignal.connect(image_viewer2.setImage)
    vid3.VideoSignal.connect(image_viewer3.setImage)

    push_button = QtWidgets.QPushButton('Start')
    push_button.clicked.connect(vid.startVideo)
    push_button.clicked.connect(vid2.startVideo)
    push_button.clicked.connect(vid3.startVideo)

    vertical_layout = QtWidgets.QVBoxLayout()
    horizontal_layout = QtWidgets.QHBoxLayout()

    horizontal_layout.addWidget(image_viewer1)
    horizontal_layout.addWidget(image_viewer2)
    horizontal_layout.addWidget(image_viewer3)

    vertical_layout.addLayout(horizontal_layout)
    vertical_layout.addWidget(push_button)
    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(vertical_layout)

    main_window = QtWidgets.QMainWindow()
    main_window.setCentralWidget(layout_widget)
    main_window.show()
    sys.exit(app.exec_())