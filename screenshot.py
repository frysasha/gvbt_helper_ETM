import vlc
import time
#import os
import cv2
import numpy as np
import numpy as np
import cv2
import os
#Below code will capture the video frames and will sve it a folder (in current working directory)

dirname = 'C:\\python\\ASK screen\\'
#video path
cap = cv2.VideoCapture('rtsp://admin@172.29.120.19:554/tcp/av0_0')
count = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        print('break')
        break

    else:
        cv2.imshow('frame', frame)
        #The received "frame" will be saved. Or you can manipulate "frame" as per your needs.
        name = "rec_frame"+str(count)+".jpg"
        cv2.imwrite(os.path.join(dirname,name), frame)
        count += 1
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
#os.add_dll_directory(r'C:\Program Files (x86)\VideoLAN\VLC')
from vlc import *
#media_player = vlc.MediaPlayer()

#player = vlc.MediaPlayer('rtsp://admin@172.29.120.20:554/tcp/av0_0')
#player.play()
#video = cv2.VideoCapture('rtsp://admin@172.29.120.20:554/tcp/av0_0')
#while 1:
#    time.sleep(5)
#    try:
#        player.video_take_snapshot(0, 'C:\\python\\ASK screen\\snapshot.tmp.png', 0, 0)
#    except:
#        print(xz)


#media = vlc.MediaPlayer('rtsp://admin:xcdfscxc@172.29.120.19:554/tcp/av0_0')
#media_player.set_media(media)
#media_player.video_set_scale(0.6)

# start playing video
#media_player.play()

# wait so the video can be played for 5 seconds
# irrespective for length of video
#time.sleep(5)

# taking screen shot
#media_player.video_take_snapshot(0, "F://test", 400, 300)
#player.play()
#player.video_take_snapshot(0, '.snapshot.tmp.png', 0, 0)




#import cv2
#cap = cv2.VideoCapture('rtsp://admin:xcdfscxc@172.29.120.19:554/tcp/av0_0')

#cv2.imshow('shot', cap)

#path = ('C:\Users\shlyakhov_ai\PycharmProjects\gvbt helper ETM\screen')
#shot = cv2.VideoCapture('rtsp://admin:xcdfscxc@172.29.120.19:554/tcp/av0_0')
#cv2.imshow('123', shot)
#saveshot = cv2.imwrite('123.png', img=123)
