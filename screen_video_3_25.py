import time,threading
from datetime import datetime
from PIL import ImageGrab
from cv2 import *
import cv2
import tkinter as tk
import csv
import numpy as np
from pynput import keyboard
face_classifier =cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

window = tk.Tk()
face0Data=[]
face1Data=[]


def saveHeadMovementData(face0Data :list, face1Data :list):
  print("in saveHeadMovementData")
  print("len(face0Data):",len(face0Data))
  print("len(face1Data):",len(face1Data))

  timeStamp=int(time.time())
  fileHeader = ["timestamp","X", "Y","W","H"]

  face0DataWriter = csv.writer(open("face0Data_"+str(timeStamp)+".csv", "w",newline='\n', encoding='utf-8'))
  face0DataWriter.writerow(fileHeader)
  face0DataWriter.writerows(face0Data)

  face1DataWriter = csv.writer(open("face1Data_" + str(timeStamp) + ".csv", "w",newline='\n', encoding='utf-8'))
  face1DataWriter.writerow(fileHeader)
  face1DataWriter.writerows(face1Data)



def video_record():   # 录入视频
  global name
  name = datetime.now().strftime('%Y-%m-%d %H-%M-%S') # 当前的时间（当文件名）
  screen = ImageGrab.grab() # 获取当前屏幕
  width, high = screen.size # 获取当前屏幕的大小
  #fourcc = VideoWriter_fourcc('X', 'V', 'I', 'D') # MPEG-4编码,文件后缀可为.avi .asf .mov等
  #video = VideoWriter('%s.avi' % name, fourcc, 15, (width, high)) # （文件名，编码器，帧率，视频宽高）
  #print('3秒后开始录制----')  # 可选
  #time.sleep(3)
  print('开始录制!')
  global start_time
  start_time = time.time()
  i = 0
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
    if faces is ():
      print('No faces detected!')

    timeStamp = time.time()
    width, height = 1920,1080

    if len(faces)==0:
        face0Data.append([timeStamp,0,0,0,0])
        face1Data.append([timeStamp,0,0,0,0])

    elif len(faces)==1:
      face=faces[0]
      (x, y, w, h)=face
      if (x + (w / 2)) < width / 2: #face 0
        face0Data.append([timeStamp,x, y, w, h])
        face1Data.append([timeStamp,0,0,0,0])

      else: #face 1
        face0Data.append([timeStamp, 0, 0, 0, 0])
        face1Data.append([timeStamp,x, y, w, h])



    else:  # 2 faces_found
      for (x, y, w, h) in faces:
        #if x < 1000 and y < 1000:
        if (x + (w / 2)) < width / 2:
          faceid = 0
          # draw_rectangle_around_face
          face0Data.append([timeStamp,x, y, w, h])
          cv2.rectangle(image, (x, y), (x + w, y + h), (127, 0, 255), 2)
          #     cv2.imshow('faces',image)
          #     cv2.waitKey(0)
          print("face coord",str(i),",faceid:",str(faceid),":",x,y,x + w,y + h)
          #faceid = faceid + 1
          # cropping_face_only
          roi_color = image[y:y + h, x:x + w]
          roi_gray = gray[y:y + h, x:x + w]
          # cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,255,0),2)
        else:
          faceid = 1
          # draw_rectangle_around_face
          face1Data.append([timeStamp,x, y, w, h])

          cv2.rectangle(image, (x, y), (x + w, y + h), (127, 0, 255), 2)
          #     cv2.imshow('faces',image)
          #     cv2.waitKey(0)
          print("face coord", str(i), ",faceid:", str(faceid), ":", x, y, x + w, y + h)
          #faceid = faceid + 1
          # cropping_face_only
          roi_color = image[y:y + h, x:x + w]
          roi_gray = gray[y:y + h, x:x + w]
          # cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,255,0),2)

    i = i + 1
    #imm = cvtColor(np.array(im), COLOR_RGB2BGR) # 转为opencv的BGR模式
    #video.write(imm)  #写入
    # time.sleep(0.2) # 等待5秒再次循环
    # m1.save('test_image.png')

# GUI
# window.wm_attributes('-topmost',1)
def on_press(key):   # 监听按键
  global flag
  if key == keyboard.Key.home:
    flag = True # 改变
    return False # 返回False，键盘监听结束！
def video_info():   # 视频信息
  video = VideoCapture('%s.avi' % name)  # 记得文件名加格式不要错！
  fps = video.get(CAP_PROP_FPS)
  Count = video.get(CAP_PROP_FRAME_COUNT)
  size = (int(video.get(CAP_PROP_FRAME_WIDTH)), int(video.get(CAP_PROP_FRAME_HEIGHT)))
  print('帧率=%.1f'%fps)
  print('帧数=%.1f'%Count)
  print('分辨率',size)
  print('视频时间=%.3f秒'%(int(Count)/fps))
  print('录制时间=%.3f秒'%(final_time-start_time))
  print('推荐帧率=%.2f'%(fps*((int(Count)/fps)/(final_time-start_time))))
if __name__ == '__main__':
  flag = False
  th = threading.Thread(target=video_record)
  th.start()
  with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
  time.sleep(1)  # 等待视频释放过后
  # video_info()


