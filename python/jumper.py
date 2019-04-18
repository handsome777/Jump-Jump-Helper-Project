# DO NOT DELETE '__init__.py'
# Import modules
from PIL import Image
import numpy as np
import math
import time
import cv2
from PIL import ImageEnhance

def get_center(canny_img,loca):
    crop_h, crop_w = canny_img.shape
    center_x, center_y, center_x1= 0, 0, 0
    flag=0
    flag_y=0
    for y in range(crop_h):
    	for x in range(crop_w):
    		if canny_img[y, x] == 255:
    			center_x=x
    			flag=1
    			flag_y=y
    			break
    	if flag==1:
    		break
    		
    for x in range(crop_w,-1,-1):
    	if canny_img[flag_y, x-1] == 255:
    		center_x1=x-1
    		break

    center_x=int((center_x1+center_x)/2)

    x_before1=0
    x_before2=0
    x_before3=0
    x_before4=0
    center_y2=0
    flag=0
    x=0
    y=0
    
    for y in range (crop_h):
    	for x in range (crop_w,-1,-1):
    		if canny_img[y,x-1]==255:
    			center_y2=y;
    			if ((x_before1 >= x_before2) and (x_before1 >= x-1) and (x_before1 >= x_before3) and (x_before1 >= x_before4)):
    				flag=1
    			else:
    				x_before1=x_before2
    				x_before2=x_before3
    				x_before3=x_before4
    				x_before4=x-1
    			break;
    	if flag == 1:
    		break
    center_y2 = center_y2-3
    

    center_y=int(0*center_y+1*center_y2)
    center_y=center_y+300
    return center_x,center_y

def cut(canny_img):
    height, width = canny_img.shape
    canny_img = canny_img[300:int(height/2), 0:width]
    return canny_img

def main(canny):
    #读取截图
    new_img=Image.open('autojump.png')
    #锐度增强，锐化系数为1.5
    enh=ImageEnhance.Sharpness(new_img)
    Sharp=1.5
    img_con=enh.enhance(Sharp)
    img_con.save("autojump1.png")#把锐化后的图片保存下来

    #找小人底部中点
    img=cv2.imread('autojump1.png',0)#读取图片
    img=cv2.GaussianBlur(img,(3,3),0)#高斯滤波
    canny_img=cv2.Canny(img,30,150)#进行canny边缘检测
    res=cv2.matchTemplate(canny_img,canny,cv2.TM_CCOEFF_NORMED)#模板匹配
    min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(res)#返回匹配系数最大的坐标和相关系数
    loca=(max_loc[0]+33,max_loc[1]+210)#加上常量到小人底部坐标

    #找下一小块的中点
    canny_img=cv2.Canny(img,5,10)#再次进行边缘检测，提高精度
    #挖掉小人，防止影响
    for y in range(loca[1]-500,loca[1]):
    	for x in range(loca[0]-30,loca[0]+90):
    		canny_img[y][x]=0
    

    c_img=cut(canny_img)#截图
    x_center,y_center=get_center(c_img,loca)#找小块中点，返回值为中点坐标

    #计算距离
    distance=(loca[0]-x_center)**2+(loca[1]-y_center)**2
    distance=distance**0.5
    return int(distance)

def jumper():
    # Read screenshot at './autojump.png'
    # You can also use any file in this directory at will
    pass

    distance = 0
    pass
    canny=np.load('tmpt.npy')
    distance=main(canny)
    return distance