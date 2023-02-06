
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject
import sys

import cv2

class ShowVideo(QObject):


    flag = 0
    
    camera = cv2.VideoCapture("/dev/v4l/by-id/usb-WITHROBOT_Inc._oCam-5CRO-U-M_SN_33594014-video-index0")
    #url = cv2.VideoCapture("./videos/")
    ret, image = camera.read()
    height, width = image.shape[:2]

    VideoSignal1 = QtCore.pyqtSignal(QtGui.QImage)
    VideoSignal2 = QtCore.pyqtSignal(QtGui.QImage)

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
            self.VideoSignal1.emit(qt_image1)


            if self.flag:
                img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                img_canny = cv2.Canny(img_gray, 50, 100)

                qt_image2 = QtGui.QImage(img_canny.data,
                                         self.width,
                                         self.height,
                                         img_canny.strides[0],
                                         QtGui.QImage.Format_Grayscale8)

                self.VideoSignal2.emit(qt_image2)


            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(25, loop.quit) #25 ms
            loop.exec_()

    @QtCore.pyqtSlot()
    def canny(self):
        self.flag = 1 - self.flag


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
    vid1 = ShowVideo(serial_number = 'SN_33594229')
    vid1.moveToThread(thread)
    vid2 = ShowVideo(serial_number = 'SN_33594014')
    vid2.moveToThread(thread)

    image_viewer1 = ImageViewer()
    image_viewer2 = ImageViewer()

    vid1.VideoSignal1.connect(image_viewer1.setImage)
    vid2.VideoSignal2.connect(image_viewer2.setImage)

    push_button1 = QtWidgets.QPushButton('Start1')
    push_button2 = QtWidgets.QPushButton('Start2')
    push_button1.clicked.connect(vid1.startVideo)
    push_button2.clicked.connect(vid2.startVideo)

    vertical_layout = QtWidgets.QVBoxLayout()
    horizontal_layout = QtWidgets.QHBoxLayout()
    horizontal_layout.addWidget(image_viewer1)
    horizontal_layout.addWidget(image_viewer2)
    vertical_layout.addLayout(horizontal_layout)
    vertical_layout.addWidget(push_button1)
    #vertical_layout.addWidget(push_button2)

    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(vertical_layout)

    main_window = QtWidgets.QMainWindow()
    main_window.setCentralWidget(layout_widget)
    main_window.show()
    sys.exit(app.exec_())