import time,threading
import numpy as np
from PIL import ImageGrab
from cv2 import *
import cv2
import tkinter as tk
import csv


from MyQueue import MyQueue
from energy_bar import EnergyBar

face_classifier =cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

window = tk.Tk()
face0Data=[]
face1Data=[]
q_face0 = MyQueue(10)
q_face1 = MyQueue(10)
width, height = 1920,1080
res_sync = 0
stop=False
# save the result into csv file
def saveHeadMovementData(face0Data :list, face1Data :list):

  timeStamp=int(time.time())
  fileHeader = ["timestamp","X", "Y","W","H","var"]

  face0DataWriter = csv.writer(open("face0Data_"+str(timeStamp)+".csv", "w",newline='\n', encoding='utf-8'))
  face0DataWriter.writerow(fileHeader)
  face0DataWriter.writerows(face0Data)

  face1DataWriter = csv.writer(open("face1Data_" + str(timeStamp) + ".csv", "w",newline='\n', encoding='utf-8'))
  face1DataWriter.writerow(fileHeader)
  face1DataWriter.writerows(face1Data)

# return var of queue input
def test_sync(inputqueue:MyQueue):
  return np.var(inputqueue.getQueue())

def video_record(energyBar:EnergyBar):   # 录入视频

  global stop
  screen = ImageGrab.grab() # 获取当前屏幕
  width, high = screen.size # 获取当前屏幕的大小


  print('start')
  i = 0
  lastFace0=(-1,0,0,0,0)
  lastFace1=(-1,0,0,0,0)

  while True:
    if stop:
      print("录制结束！")
      saveHeadMovementData(face0Data,face1Data)
      energyBar.root.destroy()
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
    res0=np.sqrt(sync_res0) * 2
    res1=np.sqrt(sync_res1) * 2
    energyBar.changeBar0Progress(res0)
    energyBar.changeBar1Progress(res1)
    # return the sync result to the sum
    if (res0>20.0 and res1>20.0):
      res_sync = 100
    elif res0>20.0 or res1>20.0 :
      res_sync = 50
    else:
      res_sync = 0
    energyBar.changeBarSumProgress(res_sync)

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
  global stop
  # print("event-----",event.char)
  stop = True

if __name__ == '__main__':
  energyBar = EnergyBar()
  t = threading.Thread(target=video_record, args=(energyBar,))
  t.setDaemon(True)
  t.start()

  energyBar.start(on_press_to_stop)

  # with keyboard.Listener(on_press=on_press) as listener:
  #   listener.join()



