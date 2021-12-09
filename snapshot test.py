import numpy as np
import cv2
import os
from time import sleep


capblue = cv2.VideoCapture('rtsp://admin:xcdfscxc@172.29.120.19:554/tcp/av0_0')
#capblue = cv2.VideoCapture('rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov')
capyellow = cv2.VideoCapture('rtsp://admin:xcdfscxc@172.29.120.18:554/tcp/av0_0')
#cappriem = cv2.VideoCapture('rtsp://admin@172.29.120.20:554/tcp/av0_0')



def snap_blue():
    while(capblue.isOpened()):
        try:
            print('probuy')
            ret, frame = capblue.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame',gray)
            cv2.imwrite(os.path.join('C:\\python\\ASK screen\\blue.jpg'), frame)
            print('ura')
            capblue.release()
            sleep(1)
            cv2.destroyAllWindows()
        except:
            print('f')
            sleep(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('off')
            break

def snap_priem():
    while (cappriem.isOpened()):
        try:
            ret, frame = cappriem.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame', gray)
            cv2.imwrite(os.path.join('C:\\python\\ASK screen\\priem.jpg'), frame)
            print('ura')
            cappriem.release()
            sleep(1)
            cv2.destroyAllWindows()
        except:
            print('f')
            sleep(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('off')
            break


def snap_yellow():
    while (capyellow.isOpened()):
        try:
            ret, frame = capyellow.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame', gray)
            cv2.imwrite(os.path.join('C:\\python\\ASK screen\\yellow.jpg'), frame)
            print('ura')
            capyellow.release()
            sleep(1)
            cv2.destroyAllWindows()
        except:
            print('f')
            sleep(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('off')
            break


snap_blue()
snap_yellow()
#snap_priem()

#cap.release()
#cv2.destroyAllWindows()