# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 17:24:33 2019
该文件包含图像畸变矫正的函数：透视矫正、倾斜矫正
@author: 陈帆
"""
import numpy as np
import argparse
import imutils
import cv2
from imutils.perspective import four_point_transform
from imutils import contours


# 透视矫正
def perspective_transformation(img):
    # 读取图像，做灰度化、高斯模糊、膨胀、Canny边缘检测
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    #尝试二值化
    """ret,binary = cv2.threshold(blurred,100,255,cv2.THRESH_BINARY)
    cv2.imshow("binary",binary)"""
    
    
    dilate = cv2.dilate(blurred, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
    
    #尝试开运算
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(dilate,cv2.MORPH_OPEN,kernel)
    #尝试图像膨胀
    dst = cv2.dilate(opening,kernel,iterations=1)
    
    
    edged = cv2.Canny(dst, 5, 20, 3)
 
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[1]
    
    #测试1
    """test1 = cv2.drawContours(img,cnts,-1,(0,0,255),8)
    print(len(cnts))
    for i in range(len(cnts)):
        str1 = "describe" + str(i)
        cv2.imshow( str1, cv2.drawContours(img,cnts,i,(0,0,255),4) )"""
    print(len(cnts))
    
    docCnt = None
 
    # 确保至少找到一个轮廓
    if len(cnts) > 0:
        # 按轮廓大小降序排列
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            # 近似轮廓
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            # 如果我们的近似轮廓有四个点，则确定找到了纸
            if len(approx) == 4:
                docCnt = approx
                break
 
    # 对原始图像应用四点透视变换，以获得纸张的俯视图
    paper = False
    #if docCnt != None:
    paper = four_point_transform(img, docCnt.reshape(4, 2))
    print(docCnt.reshape(4,2))
    print(type(docCnt.reshape(4,2)))
    print(type(docCnt.reshape(4,2)[0]))
    
    cv2.imshow("blurred",blurred)
    cv2.imshow("dilate",dilate)
    cv2.imshow("opening", opening)
    cv2.imshow("extend", dst)
    cv2.imshow("edged",edged)
    
    return paper


'''
# 透视矫正
def perspective_transformation(img):
    # 读取图像，做灰度化、高斯模糊、膨胀、Canny边缘检测
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    dilate = cv2.dilate(blurred, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
    # edged = cv2.Canny(dilate, 75, 200)
    edged = cv2.Canny(dilate, 30, 120, 3)
 
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]  # 判断是OpenCV2还是OpenCV3
    docCnt = None
 
    # 确保至少找到一个轮廓
    if len(cnts) > 0:
        # 按轮廓大小降序排列
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            # 近似轮廓
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            # 如果我们的近似轮廓有四个点，则确定找到了纸
            if len(approx) == 4:
                docCnt = approx
                break
 
    # 对原始图像应用四点透视变换，以获得纸张的俯视图
    paper = four_point_transform(img, docCnt.reshape(4, 2))
    return paper

'''