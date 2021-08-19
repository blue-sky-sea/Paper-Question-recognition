# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 13:06:39 2019

@author: Administrator
"""
import math
import numpy as np
import argparse
import imutils
import cv2
from imutils.perspective import four_point_transform
from imutils import contours


# 计算欧式距离
def cal_distance(point1, point2):
    dis = np.sqrt(np.sum(np.square(point1[0]-point2[0])+np.square(point1[1]-point2[1])))
    return dis
# 封装点
def Point(x,y):
    return [x,y]

# 基于海伦公式计算不规则四边形的面积,coord是[x1,y1,x2,y2,x3,y3,x4,y4]
'''
def helen_formula(coord):
    coord = np.array(coord).reshape((4,2))
    # 计算各边的欧式距离
    dis_01 = cal_distance(coord[0], coord[1])
    dis_12 = cal_distance(coord[1], coord[2])
    dis_23 = cal_distance(coord[2], coord[3])
    dis_31 = cal_distance(coord[3], coord[1])
    dis_13 = cal_distance(coord[0], coord[3])
    p1 = (dis_01+dis_12+dis_13)*0.5
    p2 = (dis_23+dis_31+dis_13)*0.5
    # 计算两个三角形的面积
    area1 = np.sqrt(p1*(p1-dis_01)*(p1-dis_12)*(p1-dis_13))
    area2 = np.sqrt(p2*(p2-dis_23)*(p2-dis_31)*(p2-dis_13))
    return area1+area2
'''
def helen_formula(coord):
    coord = np.array(coord).reshape((4,2))
    # 计算各边的欧式距离
    dis_01 = cal_distance(coord[0], coord[1])
    dis_12 = cal_distance(coord[1], coord[2])
    dis_23 = cal_distance(coord[2], coord[3])
    dis_31 = cal_distance(coord[3], coord[1])
    dis_13 = cal_distance(coord[1], coord[3])
    dis_02 = cal_distance(coord[0], coord[2])
    dis_03 = cal_distance(coord[0], coord[3])
    p1 = (dis_01+dis_12+dis_02)*0.5
    p2 = (dis_23+dis_03+dis_02)*0.5
    # 计算两个三角形的面积
    area1 = np.sqrt(p1*(p1-dis_01)*(p1-dis_12)*(p1-dis_02))
    area2 = np.sqrt(p2*(p2-dis_23)*(p2-dis_03)*(p2-dis_02))
    return area1+area2
'''
def calcArea(m1,m2,n1,n2,j1,j2,k1,k2): 
    q1 = Point(m1,m2) 
    q2 = Point(n1,n2) 
    q3 = Point(j1,j2) 
    q4 = Point(k1,k2) 
    d12 = calcDistance(q1, q2) 
    d23 = calcDistance(q2, q3) 
    d34 = calcDistance(q3, q4) 
    d41 = calcDistance(q4, q1) 
    d24 = calcDistance(q2, q4) 
    k1 = (d12+d41+d24)/2 
    k2 = (d23+d34+d24)/2 
    s1 = (k1*(k1-d12)(k1-d41)(k1-d24))**0.5 
    s2 = (k2*(k2-d23)(k2-d34)(k2-d24))**0.5 
    s = s1+s2 
    return s 
'''


# 筛选直线
def getlines(lines):
    templines = []
    temprow = []
    tempcol = []
    for i in range(len(lines)):
        for rho, theta in lines[i]:
            """
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(round(x0 + 1000 * (-b)))
            y1 = int(round(y0 + 1000 * a))
            x2 = int(round(x0 - 1000 * (-b)))
            y2 = int(round(y0 - 1000 * a))
            """
            th = int(DegreeTrans(theta))# theta的取值范围为[0,pi),rho可正可负
            #print("第"+str(i+1)+"个    "+"角度："+str(th)+";"+"到原点的距离："+str(rho))
            #print("角"+str(i)+"："+str(th))
            
            if  th < 80 and th > 10:
                continue
            elif th > 110 and th < 170:
                continue
            elif (th>=0 and th<=10) or (th>=170 and th<=180):
                temprow += [[rho, theta]]
            elif (th>=80 and th<=110):
                tempcol += [[rho, theta]]
                
                
    temprow = sorted(temprow,key=lambda x: abs(x[0]))
    tempcol = sorted(tempcol,key=lambda x: abs(x[0]))
    print("排好序的所有纵向的线："+str(tempcol))
    print("排好序的所有横向的线："+str(temprow))
    
    
    if len(temprow) >= 6:
        l = len(temprow)
        templines = templines + [ temprow[:3] + temprow[l-3:] ]
    else:
        templines = templines + [ temprow ]
        
    
    if len(tempcol) >= 6:
        l = len(tempcol)
        templines = templines + [ tempcol[:3] + tempcol[l-3:] ]
    else:
        templines = templines + [ tempcol ]
    
    
    return templines

# 度数转换
def DegreeTrans(theta):
    res = theta / np.pi * 180
    return res

# 求两条直线的交点坐标,!!!注意还没有设置两条直线平行的特殊情况,直线刚好水平的情况
def point(x0,y0,x1,y1,x2,y2,x3,y3): 
    a = y1-y0 
    b = x1*y0-x0*y1 
    c = x1-x0 
    d = y3-y2 
    e = x3*y2-x2*y3 
    f = x3-x2 
    
    print("%d,%d,%d,%d,%d,%d,%d,%d"%(x0,y0,x1,y1,x2,y2,x3,y3))
    print("a*f-c*d")
    print(a*f-c*d)
    
    if a*f-c*d == 0:
        return False
    
    
    y = float(a*e-b*d)/(a*f-c*d) 
    x = float(y*c-b)/a 
    return [int(x),int(y)]

def cross_point(line1,line2):#计算交点函数
    x1=line1[0]#取四点坐标
    y1=line1[1]
    x2=line1[2]
    y2=line1[3]   
    
    x3=line2[0]
    y3=line2[1]
    x4=line2[2]
    y4=line2[3]
    
    
    if (x1-x2)==0 and (x3-x4)==0:
        return False
    if (y1-y2)==0 and (y3-y4)==0:
        return False
    if (x1-x2)==0 and (y3-y4)==0:
        return [x1,y3]
    if (y1-y2)==0 and (x3-x4)==0:
        return [x3,y1]
    
    #当x1=x2，即第一条线与x轴平行时，交互两个参数从新做一次运算
    if (x1-x2) == 0:
        return cross_point(line2,line1)
    
    k1=(y2-y1)*1.0/(x2-x1)#计算k1,由于点均为整数，需要进行浮点数转化
    b1=y1*1.0-x1*k1*1.0#整型转浮点型是关键
    if (x4-x3)==0:#L2直线斜率不存在操作
        k2=None
        b2=0
    else:
        k2=(y4-y3)*1.0/(x4-x3)#斜率存在操作
        b2=y3*1.0-x3*k2*1.0
    if k2==None:
        x=x3
    else:
        #当两条直线平行时，返回False
        if (k1-k2) == 0:
            return False
        x=(b2-b1)*1.0/(k1-k2)
    y=k1*x*1.0+b1*1.0
    
    #将x,y值取整
    x = int(x)
    y = int(y)
    
    return [x,y]

#给出两点计算它们组成的线段的长度的平方
def slen(x0,y0,x1,y1):
    return math.pow(x0-x1,2)+math.pow(y0-y1,2)
    

# 遍历直线数组，得到交点坐标集合
def getcrosspoint(rowlines, collines):
    rowxylines = []
    for i in range(len(rowlines)):
        rho = rowlines[i][0]
        theta = rowlines[i][1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(round(x0 + 1000 * (-b)))
        y1 = int(round(y0 + 1000 * a))
        x2 = int(round(x0 - 1000 * (-b)))
        y2 = int(round(y0 - 1000 * a))
        # 打包
        rowxylines += [[x1,y1,x2,y2]]
    
    colxylines = []
    for i in range(len(collines)):
        rho = collines[i][0]
        theta = collines[i][1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(round(x0 + 1000 * (-b)))
        y1 = int(round(y0 + 1000 * a))
        x2 = int(round(x0 - 1000 * (-b)))
        y2 = int(round(y0 - 1000 * a))
        # 打包
        colxylines += [[x1,y1,x2,y2]]
        
        
    result = [] 
    
    '''
    for  i in range(len(xyline)-1):#这里去掉了判断数组最后一项
        x0,y0,x1,y1 = xyline[i]
        for k in range(len(xyline) - (i+1) ):
            x2,y2,x3,y3 = xyline[i + 1 + k]
            temp = cross_point([x0,y0,x1,y1],[x2,y2,x3,y3])
            if temp != False:
                result += [temp] 
                
    '''
    for i in range(len(rowlines)):
        x0,y0,x1,y1 = rowxylines[i]
        for k in range(len(collines)):
            x2,y2,x3,y3 = colxylines[k]
            temp = cross_point([x0,y0,x1,y1],[x2,y2,x3,y3])
            if temp != False:
                result += [temp]
            
    print("所有交点的集合：" + str(result))
    
    return result

# 遍历所有坐标点，找到四个目标点（待完善）
def gettargetpoint(pointset,img):
    #lt根据图像左上角点和目标点组成的线段的长度的平方大小,取最小值，得到左上角点
    #rt根据图像右上角点和目标点组成的线段的长度的平方大小,取最小值，得到右上角点
    #lb根据图像左下角点和目标点组成的线段的长度的平方大小,取最小值，得到左下角点
    #rb根据图像右下角点和目标点组成的线段的长度的平方大小,取最小值，得到右下角点
    
    #设置一个最大长度，超过该长度则认为这个交点没有意义
    height = img.shape[0]
    length = img.shape[1]
    maxsize = slen(0,0,length,height)
    
    olt = [0,0]
    ort = [length,0]
    olb = [0,height]
    orb = [length,height]
    
    lt = []
    rt = []
    lb = []
    rb = []
    l2lt = maxsize
    l2rt = maxsize
    l2lb = maxsize
    l2rb = maxsize
    
    for i in range(len(pointset)):
        p = pointset[i]
        
        #判断该交点是否在图像内
        if p[0]<0 or p[0]>length or p[1]<0 or p[1]>height:
            continue
        
        p_l2lt = slen(olt[0],olt[1],p[0],p[1])
        p_l2rt = slen(ort[0],ort[1],p[0],p[1])
        p_l2lb = slen(olb[0],olb[1],p[0],p[1])
        p_l2rb = slen(orb[0],orb[1],p[0],p[1])
        
        if p_l2lt <= l2lt:
            l2lt = p_l2lt
            lt = p
        if p_l2rt <= l2rt:
            l2rt = p_l2rt
            rt = p
        if p_l2lb <= l2lb:
            l2lb = p_l2lb
            lb = p
        if p_l2rb <= l2rb:
            l2rb = p_l2rb
            rb = p
        
            
    #在图像上画点，测试用
    dstimg = img.copy()
    cc = cv2.circle(dstimg,(lt[0],lt[1]), 5, (0,255,0), -1)
    cc = cv2.circle(cc,(rt[0],rt[1]), 5, (0,255,0), -1)
    cc = cv2.circle(cc,(rb[0],rb[1]), 5, (0,255,0), -1)
    cc = cv2.circle(cc,(lb[0],lb[1]), 5, (0,255,0), -1)
    cv2.imshow("four_point",cc)
    
    
    return [lt,rt,lb,rb]


# 透视矫正
def perspective_transformation(img):
    # 读取图像，做灰度化、高斯模糊、膨胀、Canny边缘检测
    imgshape = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    dstImage = cv2.Canny(gray, 100, 150, 3)
    print("目标的shape：" + str(dstImage.shape))
    cv2.imshow("Canny",dstImage)
    
    

    rowlinesimage = img.copy()
    collinesimage = img.copy()
    linesimage = img.copy()

 
    # 通过霍夫变换检测直线
    # 第4个参数就是阈值，阈值越大，检测精度越高
    #参数1：要检测的二值图（一般是阈值分割或边缘检测后的图）
    #参数2：距离r的精度，值越大，考虑越多的线
    #参数3：角度θ的精度，值越小，考虑越多的线
    #参数4：累加数阈值，值越小，考虑越多的线
    p = 1
    z = 130
    lines = cv2.HoughLines(dstImage, p, np.pi/180, z)
    print(lines is None)
    if lines is None:
        return img
    
    # 由于图像不同，阈值不好设定，因为阈值设定过高导致无法检测直线，阈值过低直线太多，速度很慢
    '''
    while lines==None or len(lines) <= 8:
        p = 0.1 + p
        z -= 5
        lines = cv2.HoughLines(dstImage, p, np.pi/180, z)
    '''
    while lines is None:
        p = 0.1 + p
        z -= 5
        lines = cv2.HoughLines(dstImage, p, np.pi/180, z)
        print(lines is None)
    print(len(lines))
    
    print(type(lines))
    print(type(lines[0]))


    # 依次画出每条横线段
    for i in range(len(lines)):
        for rho, theta in lines[i]:
            th = int(DegreeTrans(theta))
            
            # print("theta:", theta, " rho:", rho)
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(round(x0 + 1000 * (-b)))
            y1 = int(round(y0 + 1000 * a))
            x2 = int(round(x0 - 1000 * (-b)))
            y2 = int(round(y0 - 1000 * a))
            # 只选角度最小的作为旋转角度
    
            cv2.line(linesimage, (x1, y1), (x2, y2), (0, 0, 255), 1, cv2.LINE_AA)
            cv2.imshow("lines", linesimage)





    templines = getlines(lines)
    rowlines = templines[0]
    collines = templines[1]

    print("横线条数：" + str(len(rowlines)) + "  -->\n" + str(rowlines))
    print("竖线条数：" + str(len(collines)) + "  -->\n" + str(collines))
    
    
    
    # 依次画出每条横线段
    for i in range(len(rowlines)):
        rho = rowlines[i][0]
        theta = rowlines[i][1]
        th = int(DegreeTrans(theta))
        print("修正线"+str(i)+"    角度："+str(th)+"  ; 长度："+str(rho))
        # print("theta:", theta, " rho:", rho)
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(round(x0 + 1000 * (-b)))
        y1 = int(round(y0 + 1000 * a))
        x2 = int(round(x0 - 1000 * (-b)))
        y2 = int(round(y0 - 1000 * a))
        # 只选角度最小的作为旋转角度

        cv2.line(rowlinesimage, (x1, y1), (x2, y2), (0, 0, 255), 1, cv2.LINE_AA)
        cv2.imshow("rowlines", rowlinesimage)
        
    # 依次画出每条竖线段
    for i in range(len(collines)):
        rho = collines[i][0]
        theta = collines[i][1]
        th = int(DegreeTrans(theta))
        print("修正线"+str(i)+"    角度："+str(th)+"  ; 长度："+str(rho))
        # print("theta:", theta, " rho:", rho)
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(round(x0 + 1000 * (-b)))
        y1 = int(round(y0 + 1000 * a))
        x2 = int(round(x0 - 1000 * (-b)))
        y2 = int(round(y0 - 1000 * a))
        # 只选角度最小的作为旋转角度

        cv2.line(collinesimage, (x1, y1), (x2, y2), (0, 0, 255), 1, cv2.LINE_AA)
        cv2.imshow("collines", collinesimage)

   
    paper = False
    
    #计算得到交点集合并找到其中4个目标点
    pointset = getcrosspoint(rowlines, collines)       
    fourpoint = gettargetpoint(pointset,img)
    print(fourpoint)
    
    print("图像的长宽：" + str(img.shape))
    print("最终确定的四个点：" + str(fourpoint))
    #计算面积并与原图比较
    f = fourpoint.copy()
    cuttingArea = helen_formula([f[0][0],f[0][1],f[1][0],f[1][1],f[2][0],f[2][1],f[3][0],f[3][1]])
    print("裁剪区域的面积是："+str(cuttingArea))
    areaRatio = cuttingArea/(imgshape[0]*imgshape[1])
    print("源图像宽："+str(imgshape[0]) +"; 长："+str(imgshape[1]) +"面积：" +str(imgshape[0]*imgshape[1]))
    print("面积比是："+str(areaRatio))
    print(helen_formula([0,0,0,1,1,0,1,1]))
    if areaRatio <= 0.7:
        return img
   
   #four_point_transform的第二个参数是[[左上点],[右上点],[右下点],[左下点]](tl, tr, br, bl) = rect
    paper = four_point_transform(img, np.array(fourpoint))
    
    

    return paper