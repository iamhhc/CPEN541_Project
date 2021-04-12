from copy import deepcopy
import sq_queue
import time,threading
from datetime import datetime
from PIL import ImageGrab
from cv2 import *
import cv2
import tkinter as tk
import csv
import numpy as np
from pynput import keyboard
from numpy import *

from MyQueue import MyQueue
from energy_bar import EnergyBar

face_classifier =cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

window = tk.Tk()
face0Data=[]
face1Data=[]
faceData0_5s=[]
faceData1_5s=[]
# res = sq_queue.SqQueue(15)
q_face0 = MyQueue(10)
q_face1 = MyQueue(10)
width, height = 1920,1080

def saveHeadMovementData(face0Data :list, face1Data :list):

  timeStamp=int(time.time())
  fileHeader = ["timestamp","X", "Y","W","H","var"]

  face0DataWriter = csv.writer(open("face0Data_"+str(timeStamp)+".csv", "w",newline='\n', encoding='utf-8'))
  face0DataWriter.writerow(fileHeader)
  face0DataWriter.writerows(face0Data)

  face1DataWriter = csv.writer(open("face1Data_" + str(timeStamp) + ".csv", "w",newline='\n', encoding='utf-8'))
  face1DataWriter.writerow(fileHeader)
  face1DataWriter.writerows(face1Data)


def test_sync(inputqueue:MyQueue):
  # for i in range(15):
  #   faceData0_5s[i] = inputqueue[i]
  # avg = np.mean(inputqueue)

  return np.var(inputqueue.getQueue())


def video_record(energyBar:EnergyBar):   # 录入视频

  global name
  name = datetime.now().strftime('%Y-%m-%d %H-%M-%S') # 当前的时间（当文件名）
  screen = ImageGrab.grab() # 获取当前屏幕
  width, high = screen.size # 获取当前屏幕的大小
  #fourcc = VideoWriter_fourcc('X', 'V', 'I', 'D') # MPEG-4编码,文件后缀可为.avi .asf .mov等
  #video = VideoWriter('%s.avi' % name, fourcc, 15, (width, high)) # （文件名，编码器，帧率，视频宽高）
  #time.sleep(3)
  print('开始录制!')
  global start_time
  start_time = time.time()
  i = 0
  lastFace0=(-1,0,0,0,0)
  lastFace1=(-1,0,0,0,0)

  while True:
    if flag:
      print("录制结束！")
      saveHeadMovementData(face0Data,face1Data)
      global final_time
      final_time = time.time()
      #video.release() #释放
      break
    im = ImageGrab.grab()  # 图片为RGB模式
    name="image.png"
    im.save(name)
    image = cv2.imread(name)
    # image = cv2.imread('test_image'+str(i)+'.png')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # detecting_faces
    faces = face_classifier.detectMultiScale(gray, 1.5, 5)

    timeStamp = time.time()



    face0 = lastFace0
    face1 = lastFace1
    if len(faces)==0:
        print('No faces detected!')


    elif len(faces)==1:
      print('1 face detected!')

      (x, y, w, h)=faces[0]

      if (x + (w / 2)) < width / 2: #face 0
        face0=(timeStamp,x, y , w, h)

      else: #face 1

        face1=(timeStamp,x, y, w, h)

    elif len(faces)==2 :  # 2 faces_found
      for (x, y, w, h) in faces:
        print('2 faces detected!')

        if (x + (w / 2)) < width / 2: #屏幕左半边的脸识别为  faceid = 0
          faceid = 0
          face0=(timeStamp,x, y, w, h)
          # print("timeStamp",str(timeStamp),"faceid:",str(faceid),":",x,y,x + w,y + h)

        else: #屏幕右半边的脸识别为  faceid = 1
          faceid = 1
          face1=(timeStamp,x, y, w, h)
          # print("timeStamp",str(timeStamp), ",faceid:", str(faceid), ":", x, y, x + w, y + h)


    q_face0.EnQueue(face0[2])
    q_face1.EnQueue(face1[2])
    sync_res0 = test_sync(q_face0)
    sync_res1 = test_sync(q_face1)


    face0=face0+(sync_res0,)
    face1=face1+(sync_res1,)
    res0=np.sqrt(sync_res0) * 4
    res1=np.sqrt(sync_res1) * 4
    energyBar.changeBar0Progress(res0)
    energyBar.changeBar1Progress(res1)
    energyBar.changeBarSumProgress((res0+res1)/2)

    face0Data.append(face0)
    face1Data.append(face1)


    if face0[0]==-1:
      face0=(-1,0,0,0,0,0)
    if face1[0] == -1:
      face1 = (-1, 0, 0, 0, 0, 0)

    lastFace0= face0
    lastFace1=face1

    i = i + 1



def on_press_to_stop(event=None):
  global flag
  print("event-----",event.char)
  flag = True # 改变

if __name__ == '__main__':
  flag = False
  energyBar = EnergyBar()
  t = threading.Thread(target=video_record, args=(energyBar,))
  t.setDaemon(True)
  t.start()

  energyBar.start(on_press_to_stop)

  # with keyboard.Listener(on_press=on_press) as listener:
  #   listener.join()



