# CPEN541_Project
### 2021/3/25
√ python 录屏 + 脸部识别  [python屏幕录制](https://www.jb51.net/article/181757.htm)  
√ 先跑通截屏的code，之后将脸部识别融入进去  

**problems**: 两个人的人脸数据坐标混乱。不能定向追踪某个人。  
**solution**: 屏幕一分为二，录屏的坐标固定，限制在某一坐标内的人脸就是固定的faceid  

*(TBD)* 本地拿到两组人脸数据（中心点）判断是否同步  

需要的库依赖:
```
dependency: 
pynput 
Pillow 
python-opencv
```
### 2021/4/1
the x and y to seperate coordinates of two faces.

**how to study the sync**  
*save the result to local file??*  
*or save the data into arrays and do real-time analysis??*  

GUI: two little window with energy bar and link to the sync result  
locate the precise x and y of the windows.  
[弹窗](https://zhuanlan.zhihu.com/p/81429343)  

first energy bar: x:800  y:660  w:66  h:200  
second energy bar:  x:1700  y:660  w:66  h:200

优化输出数据，如果没检测到和上一帧保持一样
判断相关性

### 2021/4/8
use a queue to save 15 frames  
calculate the standard deviation of the 15 number  
use the result as an indication whether the user has nodded

works to be done:
1. split the window (*now we have two bars in the same window*)  
2. move the window to the right place (*the information of the position is listed above*)  
3. make sure the windows are always on top  
4. *find out other ways to visualize the output (optional)*  
5. find volunteers?  
6. start the report  

### 2021/4/11
The layout is far from good, need to change the place of the window  
need to at least change the color  
or the position