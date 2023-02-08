import os
import cv2
import subprocess

# OpenCV VideoCaptureProperties Doc : https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html



class oCam_Camera:
    def __init__(self, serial_number=''):
        self.DEFAULT_CAMERA_NAME = '/dev/v4l/by-id/usb-WITHROBOT_Inc._oCam-5CRO-U-M_' + serial_number + '-video-index0'
        if os.path.exists(self.DEFAULT_CAMERA_NAME):
            device_path = os.path.realpath(self.DEFAULT_CAMERA_NAME)

        self.cam = cv2.VideoCapture(device_path)
        # self.set_default_opt()

        if not self.cam.isOpened():
            print('oCAM' + serial_number + ' : 안됨')


    def get_frame(self):
        ret_val, frame = self.cam.read()
        return frame


    def set_default_opt(self):
        # Basic option
        frame_width     = 1280
        frame_height    = 720
        frame_fps       = 30
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height) 
        self.cam.set(cv2.CAP_PROP_FPS, frame_fps) 

        ### Detailed option
        #          brightness 0x00980900 (int)    : min=-4 max=4 step=1 default=0 value=4
        #            contrast 0x00980901 (int)    : min=0 max=8 step=1 default=4 value=0
        #          saturation 0x00980902 (int)    : min=0 max=8 step=1 default=4 value=4
        #                 hue 0x00980903 (int)    : min=0 max=11 step=1 default=6 value=6
        #   exposure_absolute 0x009a0902 (int)    : min=0 max=10 step=1 default=4 value=4

        ### Create a dict of the settings of interest
        self.cam_props = {'brightness': 4, 'contrast': 0, 'saturation': 4, 'hue': 6, 'exposure_absolute': 4}
        for key in self.cam_props:
            subprocess.call(['v4l2-ctl -d {} -c {}={}'.format(self.DEFAULT_CAMERA_NAME, key, str(self.cam_props[key]))], shell=True)


    def print_key_info(self):
        for key in self.cam_props:
            subprocess.call(['v4l2-ctl -d {} -C {}'.format(self.DEFAULT_CAMERA_NAME, key)], shell=True)


    def print_all_info(self):
        print(f"CAP_PROP_POS_MSEC:{self.cam.get(cv2.CAP_PROP_POS_MSEC)}")                            # 0
        # print(f"CAP_PROP_POS_FRAMES:{self.cam.get(cv2.CAP_PROP_POS_FRAMES)}")                        # 1
        # print(f"CAP_PROP_POS_AVI_RATIO:{self.cam.get(cv2.CAP_PROP_POS_AVI_RATIO)}")                  # 2
        print(f"CAP_PROP_FRAME_WIDTH:{self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)}")                      # 3
        print(f"CAP_PROP_FRAME_HEIGHT:{self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)}")                    # 4
        print(f"CAP_PROP_FPS:{self.cam.get(cv2.CAP_PROP_FPS)}")                                      # 5
        print(f"CAP_PROP_FOURCC:{self.cam.get(cv2.CAP_PROP_FOURCC)}")                                # 6
        # print(f"CAP_PROP_FRAME_COUNT:{self.cam.get(cv2.CAP_PROP_FRAME_COUNT)}")                      # 7
        print(f"CAP_PROP_FORMAT:{self.cam.get(cv2.CAP_PROP_FORMAT)}")                                # 8
        print(f"CAP_PROP_MODE:{self.cam.get(cv2.CAP_PROP_MODE)}")                                    # 9
        print(f"CAP_PROP_BRIGHTNESS:{self.cam.get(cv2.CAP_PROP_BRIGHTNESS)}")                        # 10 / min=-4 max=4 step=1 default=0 value=4

        print(f"CAP_PROP_CONTRAST:{self.cam.get(cv2.CAP_PROP_CONTRAST)}")                            # 11 / min=0 max=8 step=1 default=4 value=0
        print(f"CAP_PROP_SATURATION:{self.cam.get(cv2.CAP_PROP_SATURATION)}")                        # 12 / min=0 max=8 step=1 default=4 value=4 
        print(f"CAP_PROP_HUE:{self.cam.get(cv2.CAP_PROP_HUE)}")                                      # 13 / min=0 max=11 step=1 default=6 value=6
        # print(f"CAP_PROP_GAIN:{self.cam.get(cv2.CAP_PROP_GAIN)}")                                    # 14
        print(f"CAP_PROP_EXPOSURE:{self.cam.get(cv2.CAP_PROP_EXPOSURE)}")                            # 15
        print(f"CAP_PROP_CONVERT_RGB:{self.cam.get(cv2.CAP_PROP_CONVERT_RGB)}")                      # 16
        # print(f"CAP_PROP_WHITE_BALANCE_BLUE_U:{self.cam.get(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U)}")    # 17
        # print(f"CAP_PROP_RECTIFICATION:{self.cam.get(cv2.CAP_PROP_RECTIFICATION)}")                  # 18
        # print(f"CAP_PROP_MONOCHROME:{self.cam.get(cv2.CAP_PROP_MONOCHROME)}")                        # 19
        # print(f"CAP_PROP_SHARPNESS:{self.cam.get(cv2.CAP_PROP_SHARPNESS)}")                          # 20

        # print(f"CAP_PROP_AUTO_EXPOSURE:{self.cam.get(cv2.CAP_PROP_AUTO_EXPOSURE)}")                  # 21
        # print(f"CAP_PROP_GAMMA:{self.cam.get(cv2.CAP_PROP_GAMMA)}")                                  # 22
        # print(f"CAP_PROP_TEMPERATURE:{self.cam.get(cv2.CAP_PROP_TEMPERATURE)}")                      # 23
        # print(f"CAP_PROP_TRIGGER:{self.cam.get(cv2.CAP_PROP_TRIGGER)}")                              # 24
        # print(f"CAP_PROP_TRIGGER_DELAY:{self.cam.get(cv2.CAP_PROP_TRIGGER_DELAY)}")                  # 25
        # print(f"CAP_PROP_WHITE_BALANCE_RED_V:{self.cam.get(cv2.CAP_PROP_WHITE_BALANCE_RED_V)}")      # 26
        # print(f"CAP_PROP_ZOOM:{self.cam.get(cv2.CAP_PROP_ZOOM)}")                                    # 27
        # print(f"CAP_PROP_FOCUS:{self.cam.get(cv2.CAP_PROP_FOCUS)}")                                  # 28
        # print(f"CAP_PROP_GUID:{self.cam.get(cv2.CAP_PROP_GUID)}")                                    # 29
        # print(f"CAP_PROP_ISO_SPEED:{self.cam.get(cv2.CAP_PROP_ISO_SPEED)}")                          # 30

        # None 31 
        # print(f"CAP_PROP_BACKLIGHT:{self.cam.get(cv2.CAP_PROP_BACKLIGHT)}")                          # 32
        # print(f"CAP_PROP_PAN:{self.cam.get(cv2.CAP_PROP_PAN)}")                                      # 33
        # print(f"CAP_PROP_TILT:{self.cam.get(cv2.CAP_PROP_TILT)}")                                    # 34
        # print(f"CAP_PROP_ROLL:{self.cam.get(cv2.CAP_PROP_ROLL)}")                                    # 35
        # print(f"CAP_PROP_IRIS:{self.cam.get(cv2.CAP_PROP_IRIS)}")                                    # 36
        # print(f"CAP_PROP_SETTINGS:{self.cam.get(cv2.CAP_PROP_SETTINGS)}")                            # 37
        print(f"CAP_PROP_BUFFERSIZE:{self.cam.get(cv2.CAP_PROP_BUFFERSIZE)}")                        # 38
        # print(f"CAP_PROP_AUTOFOCUS:{self.cam.get(cv2.CAP_PROP_AUTOFOCUS)}")                          # 39
        # print(f"CAP_PROP_SAR_NUM:{self.cam.get(cv2.CAP_PROP_SAR_NUM)}")                              # 40

        # print(f"CAP_PROP_SAR_DEN:{self.cam.get(cv2.CAP_PROP_SAR_DEN)}")                              # 41
        print(f"CAP_PROP_BACKEND:{self.cam.get(cv2.CAP_PROP_BACKEND)}")                              # 42
        # print(f"CAP_PROP_CHANNEL:{self.cam.get(cv2.CAP_PROP_CHANNEL)}")                              # 43
        # print(f"CAP_PROP_AUTO_WB:{self.cam.get(cv2.CAP_PROP_AUTO_WB)}")                              # 44
        # print(f"CAP_PROP_WB_TEMPERATURE:{self.cam.get(cv2.CAP_PROP_WB_TEMPERATURE)}")                # 45
        # print(f"CAP_PROP_CODEC_PIXEL_FORMAT:{self.cam.get(cv2.CAP_PROP_CODEC_PIXEL_FORMAT)}")        # 46
        # print(f"CAP_PROP_BITRATE:{self.cam.get(cv2.CAP_PROP_BITRATE)}")                              # 47
        # print(f"CAP_PROP_ORIENTATION_META:{self.cam.get(cv2.CAP_PROP_ORIENTATION_META)}")            # 48
        print(f"CAP_PROP_ORIENTATION_AUTO:{self.cam.get(cv2.CAP_PROP_ORIENTATION_AUTO)}")            # 49
        # None 50

        # None 51
        # None 52
        # print(f"CAP_PROP_OPEN_TIMEOUT_MSEC:{self.cam.get(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC)}")          # 53
        # print(f"CAP_PROP_READ_TIMEOUT_MSEC:{self.cam.get(cv2.CAP_PROP_READ_TIMEOUT_MSEC)}")          # 54



if __name__ == "__main__": 
    ocam1 = oCam_Camera(serial_number='SN_33594229')
    # ocam2 = oCam_Camera(serial_number='SN_33594143')
    # ocam3 = oCam_Camera(serial_number='SN_33594229')
    # ocam.print_key_info()
    while True:
        frame1 = ocam1.get_frame()
        # frame2 = ocam2.get_frame()
        # frame3 = ocam3.get_frame()
    
        # print(frame1)
        # print(frame2)
        # print(frame3)

        cv2.imshow("Cam Viewer1",frame1)
        # cv2.imshow("Cam Viewer2",frame2)
        # cv2.imshow("Cam Viewer3",frame3)
        if cv2.waitKey(1) == 27:
            break # esc to quit