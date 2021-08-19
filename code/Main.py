#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 11:01:36 2019

@author: tt
"""

import sys
sys.path.append('D:\python3.6\Lib\site-packages')

import temp
import JudgeTool as tool
  


'''
    分隔及输出识别出的文字的函数
    return ：无
    author ：tt
''' 
def lookarea(examinations_area):
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    for examination in examinations_area:
        print("**************************")
        for line in examination:
            print(line['words'])
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^") 
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")   


'''
    判断出每一道题的边框的width，top，left，height的函数
    return ：[{'width':,'top':,'left':,'height':},{'width':,'top':,'left':,'height':}]
    author ：tt
''' 
def examinations_location_sort(examinations_area) :

    locations_list=[]
    locations={}
    last_locations={}
    questionnumber=len(examinations_area)
    print("examinations_area length:",questionnumber)
    n=0;
    for examination in examinations_area:
        maxwidth=0
        maxtop=0
        mintop=10086
        minleft=10086
        maxtop_height=0
        #maxleft=0
        maxleft_plus_width=0
        locations={}
        for line in examination:
            if(line['location']['width']>maxwidth):
                maxwidth=line['location']['width']
            if(line['location']['top']<mintop):
                mintop=line['location']['top']
            if(line['location']['top']>maxtop):
                maxtop=line['location']['top']
                maxtop_height=line['location']['height']
            if(line['location']['left']<minleft):
                minleft=line['location']['left']
            #if(line['location']['left']>maxleft):
             #   maxleft=line['location']['left']
            if((line['location']['left']+line['location']['width'])>maxleft_plus_width):
                maxleft_plus_width=(line['location']['left']+line['location']['width'])
        locations['width']=maxleft_plus_width-minleft
        locations['top']=mintop
        locations['left']=minleft
        locations['height']=maxtop+maxtop_height-mintop
        
        if(n==0):
            last_locations=locations
        elif(n < questionnumber):
            if(last_locations['top']<locations['top']):
                if( (last_locations['top']+last_locations['height']) < (locations['top']-1) ):
                    #强制矫正
                    last_locations['height']=locations['top']-last_locations['top']-1     
                #print("no.",n,"append last_locations into locations_list")   
                locations_list.append(last_locations)
                last_locations=locations
            else:
                locations_list.append(last_locations)
                last_locations=locations 
        n=n+1
    #print("no.",n,"append loactions into locations_list")   
    locations_list.append(locations)
    
        
    return locations_list
        
"""
    遍历全部文本为题干还是其他，划分出每段文本所属的题目的函数
    in： results
    return ： examinations_result
    author ： Yuta Mizuki
"""
def JudgeFunction(results):
    #print(len(results['words_result']))#36条数据
    tool.GL.questionnumber="0."
    #examinations_area:总的存储所有处理后数据的list,
    #存储多个（多个result集合的题目区域）single_examination_area数组
    examinations_area=[]
    examinations_options_area=[]
    #single_examination_area:存储单个（多个result集合的题目区域）题目区域的数组
    #存储多个result（属于同一题的result），result:文本信息，包括文本内容和文本位置
    single_examination_area=[]#单个题目数据（文本／位置信息）的area
    single_examination_options_area=[]#单个题目选项（文本／位置信息）的area
    #examination_number:题目的数量
    examination_number=0
    #current_numberlevel:当前题号类型层次标示
    #current_numberstyle=0;#默认为0，即还没有分层。
    current_flag=0;#默认为0，当前层是否失效
    for i in range(len(results['words_result'])):
        result=results['words_result'][i]
        #print("[i]:",i,"  ",result['words'])
        #print(result['location'])
        isquestion,numberstyle,code=tool.question_JudgeTool(result['words'])
        if(code=="11" or code=="010" or code=="fixed"):
            current_flag=1
        if(code=="011" or code=="001"):
            current_flag=0  
        if(isquestion==True):
            print(result['words'],"###Yes###",code)
            '''是题干。考虑属于上级题目的情况（如 一、单项选择题），存在上下级时，忽略。TODO'''

            
            #考虑第一道题的情况，当之前没有题目area这是第一个时，直接将location信息添加到single_examination_area
            if(examination_number==0):  
                examination_number=examination_number+1
                single_examination_area.append(result)
            #如果不是第一题，那么先提交上一题的area到examinations_area，然后清空，然后再开始添加下一题的内容到single_examination_area
            elif(examination_number>=0):   
                if(numberstyle>5): 
                    single_examination_area.append(result)
                else:
                    examination_number=examination_number+1#将题目数加一
                    examinations_area.append(single_examination_area)#将上一single题的area提交
                    if(len(single_examination_options_area)!=0):
                        examinations_options_area.append(single_examination_options_area)#将上一single题的area提交
                    #lookarea(examinations_area)
                    single_examination_area=[]#提交后清空single题的存储
                    single_examination_options_area=[]#提交后清空single题的存储
                    single_examination_area.append(result)#将下一题 (也就是本行)添加到single题的area
                
        elif(isquestion==False):
            print(result['words'],"&&&NO&&&",code)
            '''不是题干,可能是题目的一部分(选择题选项／题干的非第一行/下级题目)，
            也可能完全不属于题目(如 考出风格／非题干的一部分)，
            '''
            if(current_flag==0):
                continue;
            
            single_examination_area.append(result)#添加到当前single题的area      
            
            #为选择题选项的情况
            if(code=="0001"):
                single_examination_options_area.append(result)#添加到当前single题选项的area  
                
            #考虑最后一行的情况，此时已经没有题干行进行判断一道题的area是否结束，
            #所以当最后一行时,直接进行area提交，结束
            if(i==(len(results['words_result'])-1)):         
                examinations_area.append(single_examination_area)
                examinations_options_area.append(single_examination_options_area)
                single_examination_area=[]
            else:
                continue
                
    print(examination_number)
    return examinations_area,examinations_options_area


'''
    测试将图片切割及切割后图片是否正确的函数
    return ：无
    author ：tt
''' 
def test():
    filepath=r'F:\testphoto\0002_1.jpg'#要切割的图片路径
    #results=temp.accurate_ocr(filepath)
    results=temp.general_ocr(filepath)
    
    r,op=JudgeFunction(results)
    
    print()
    print("*results are:")
    lookarea(r)
    
    #print()
    lookarea(op)
    
    locations_list=examinations_location_sort(r)
    #option_locations_list=examinations_location_sort(op)
    print(locations_list)
    #areatype=1
    tool.crop_Tool(filepath,"F:\1",locations_list,1)#要存储的图片路径
    #print("option area cut")
    #print(option_locations_list)
    #areatype=2
    #tool.crop_Tool(filepath,"/Users/tt/Desktop/t",option_locations_list,2)
    print("finish")

'''
    调用百度API及包括框出每一道题、切好图片进行命名并放入文件夹的函数
    return ：无
    author ：tt
'''
def singleocr(filepath,save_dirpath,ocrtype):
    filename=filepath.split('/')[-1]
    if(filename[0]=="_"):
        print("[singleocr:]image ignored!")
        return 0
    #test
    ocrtype=1
    if(ocrtype==1):
        results=temp.accurate_ocr(filepath)
    elif(ocrtype!=1):
        results=temp.general_ocr(filepath)
    r,op=JudgeFunction(results)   
    locations_list=examinations_location_sort(r)
    tool.crop_Tool(filepath,save_dirpath,locations_list,1)
    
#test()