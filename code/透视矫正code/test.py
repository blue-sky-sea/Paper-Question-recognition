# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 17:43:22 2019
对图像进行预处理
@author: 陈帆
"""
import cv2
import discorr as preA1
import discorr2 as preA2
import hasCorner


ori = cv2.imread("D:/7.jpg")
shapeOri = ori.shape
length = shapeOri[1]
width = shapeOri[0]
maxL = length
if length < width:
    maxL = width
k = 1000.0/maxL

resize = cv2.resize(ori, None, fx=k, fy=k)
cv2.imshow("ori", resize)
hasCorner.judge(resize)
correct1 = preA2.perspective_transformation(resize)
cv2.imshow("correct1", correct1)
retval = cv2.waitKey(0)
cv2.destroyAllWindows()
