import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import *
from PIL import ImageTk, Image
import cv2
import numpy as np

def upload_file():
    global img
    global filename
    f_types = [('jpg Files', '*.jpg'),('png Files','*.png')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    print(filename)
    img = ImageTk.PhotoImage(file=filename)
    b2 =tk.Button(root1,image=img) # using Button
    canvas2.create_window(400, 500, window=b2)
 


def handGesture():
  img = cv2.imread(filename)
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  blur = cv2.GaussianBlur(gray,(5,5),0)
  ret,thresh1 = cv2.threshold(blur,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

  contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  drawing = np.zeros(img.shape,np.uint8)

  max_area=0
 
  for i in range(len(contours)):
    cnt=contours[i]
    area = cv2.contourArea(cnt)
    if (area>max_area):
      max_area=area
      ci=i
  cnt=contours[ci]
  hull = cv2.convexHull(cnt)
  moments = cv2.moments(cnt)
  if moments['m00']!=0:
    cx = int(moments['m10']/moments['m00']) # cx = M10/M00
    cy = int(moments['m01']/moments['m00']) # cy = M01/M00
           
  centr=(cx,cy)      
  cv2.circle(img,centr,5,[0,0,255],2)      
  cv2.drawContours(drawing,[cnt],0,(0,255,0),2)
  cv2.drawContours(drawing,[hull],0,(0,0,255),2)
       
  cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
  hull = cv2.convexHull(cnt,returnPoints = False)
 
  if (1):
    defects = cv2.convexityDefects(cnt,hull)
    mind=0
    maxd=0
    for i in range(defects.shape[0]):
      s,e,f,d = defects[i,0]
      start = tuple(cnt[s][0])
      end = tuple(cnt[e][0])
      far = tuple(cnt[f][0])
      dist = cv2.pointPolygonTest(cnt,centr,True)
      cv2.line(img,start,end,[0,0,255],5)
     
      cv2.circle(img,far,10,[0,0,255],-1)
      font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(img, "Number of Fingers: "+str(i), ( 10, 100), font, 0.5, (0, 0, 255), 1)

    i=0
    cv2.imshow("image",img)

#input = cv2.imread("/Users/rexcarvalho/Desktop/Screen Shot 2022-06-03 at 2.52.31 PM.png")
#output = handGesture(input)
#cv2.imshow('image',output)

def values():
  label_Prediction = tk.Label(root, text= 'Hello',bg='orange')
  canvas11.create_window(300, 230, window=label_Prediction)

def canvas11():
    global root
    global canvas1
    root= tk.Tk()
    #Make a Canvas (i.e, a screen for your project
    canvas1 = tk.Canvas(root, width = 500, height = 400)
    canvas1.pack()
    canvas1.config(bg='orange')
    #To see the GUI screen
    label1 = tk.Label(root, text='HAND GESTURE RECOGNITION APP')
    canvas1.create_window(260, 20, window=label1)
     
    button1 = tk.Button (root, text='Picture Upload',command=canvas12, bg='orange')
    # button to call the 'values' command above
    canvas1.create_window(260, 125, window=button1)
     
    #button1 = tk.Button (root, text='Take Picture',command=values, bg='orange')
    # button to call the 'values' command above
    #canvas1.create_window(260, 140, window=button1)

    button1 = tk.Button (root, text='Hand Gestures',command=help, bg='orange')
    # button to call the 'values' command above
    canvas1.create_window(260, 225, window=button1)
    root.mainloop()
 

def help():
    win = tk.Toplevel(root)
    win.geometry("500x300")
    frame = Frame(win, width=150, height=100)
    frame.pack()
    frame.place(anchor='center', relx=0.5, rely=0.5)
    img = ImageTk.PhotoImage(Image.open("/Users/rexcarvalho/Desktop/Screen Shot 2022-05-16 at 12.43.03 PM.png"))
    label = Label(frame, image = img)
    label.pack()
    win.mainloop()


def canvas12():
    global root1
    global canvas2
    root1 = tk.Toplevel(root)
    canvas2 = tk.Canvas(root1, width = 800, height = 1000)
    canvas2.pack()
    canvas2.config(bg='#0000EE')
    label1 = tk.Label(root1, text='UPLOAD PICTURE')
    canvas2.create_window(400, 20, window=label1)
    #Define this function that help you to upload image from local system
    button1 = tk.Button (root1, text='Upload Picture',command=upload_file, bg='orange')
    # button to call the 'values' command above
    canvas2.create_window(400, 80, window=button1)
    button2 = tk.Button (root1, text='Submit Picture',command=handGesture, bg='orange')
    # button to call the 'values' command above
    canvas2.create_window(400, 180, window=button2)
    root1.mainloop()
   

canvas11()
