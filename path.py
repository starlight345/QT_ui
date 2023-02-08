import os
import cv2

def cam_path():

    path_dir = "/dev/v4l/by-id"
    file_list = os.listdir(path_dir)

    n_list= list()
    for i in range(len(file_list)//2) :
        n_list.append(path_dir + "/"+ file_list[2*i][:-1]+"0")
    
    real_list = list()
    for name in n_list:
        real_list.append(os.path.realpath(name))
    
    return n_list
    