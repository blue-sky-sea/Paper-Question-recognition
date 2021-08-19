#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 12:00:32 2019

@author: tt
"""
import re
import cv2

class MyGlobal:
    def __init__(self):
        self.A = 0
        self.B = [0]
        self.questionnumber="0."
GL = MyGlobal()

'''
    将切好的图片进行命名及放入文件夹的函数
    return ：
    author ：404
'''

def crop_Tool(filepath,save_dirpath,location_list,areatype):
    img = cv2.imread(filepath)
    i=0
    savepath="./"
    global filename
    filename=filepath.split('/')[-1]
    filename=filename.split('.')[0]
    #print(location_list)
    #print("filename is ",filename)
    for loc in location_list:
        cropped = img[loc['top']:loc['top']+loc['height'] , loc['left']:loc['left']+loc['width']]
        picnum=""
        if(i<10):
            picnum="00"+str(i)
        if(i>=10 and i<100):
            picnum="0"+str(i)    
        
        if(areatype==1):
            savepath=save_dirpath+"/"+filename+picnum+".jpg" 
            print(savepath)
        
        if(areatype==2):
            savepath=save_dirpath+"/"+"option_"+filename+picnum+".jpg"
        i=i+1
        cv2.imwrite(savepath, cropped)
        
'''
    判断一句话是否为疑问句／命令句／是非判断句的函数
    return ：True／False
    author ：poi
'''           
#判断一句话是否为疑问句／命令句／是非判断句／题干标志的函数
def questionemotion_JudgeTool(textcontent):

    interrogtive_dict=['吗\?','(有|是)哪(些|里)','(有|要)(几|多少)(些|种|分钟|时间|千克|米|吨|本|万)','如何.*(定义|进行|处理)','(什么|何).*(问题|区别|不同|作用|原因)',
                       '(为|是|有)(什么|何|多少)','(想想看|请问).(怎么|区别是|看法是|多长时间)','怎样.*(理解|处理)','(问|检验).*(差异|差别|影响)',
                       '(what/why/where/how/when).\?']#疑问句
    imperative_dict=['请.*(辨析|解释|证明|说明)','求.*(概率|解|面积|值)','求解.*问题','阅读.*(回答|完成|解释)','简要说明.*区别',
                     '归纳.主要内容','概(述|论).*(历史意义|作用)','(综|结)合.*(体会|理解)','请你.*应该是','根据.*给',
                     '(句|文|词).*(默|填)写','的(主要内涵|基本标准)','(指出|简析|简述|分析|解释|试论).*(原因|好处|条件|程序|流程|意义|产生|应用|内容|影响|策略|方面)',
                     '(试加以说明|的一项是)']#命令句
    copulative_dict=['请.*判断.*是否','(正确|错误).*（的是|的有）','则.*为','（其中|下列|上述）.*是',]#是非判断句
    
    #flag_dict=['本题满分[0-9]+分','Section']
    key=textcontent
    for p in interrogtive_dict:
        pattern1=re.compile(p)
        res=pattern1.findall(key)
        if len(res)!=0:
            print("这里发生了什么？",p)
            
            return True,1
    for p in copulative_dict:
        pattern1=re.compile(p)
        res=pattern1.findall(key)
        if len(res)!=0:
            #print(res)
            return True,2
    for p in imperative_dict:
        pattern1=re.compile(p)
        res=pattern1.findall(key)
        if len(res)!=0:
            #print(res)
            return True,3
    '''for p in flag_dict:
        pattern1=re.compile(p)
        res=pattern1.findall(key)
        if len(res)!=0:
            #print(res)
            return True,4'''
    return False,0


'''
    判断是否有题号，以及题号的类型的函数
    return ：True／False,numberstyle(1,2,3,4,5,6,7,0),code
    author ：Yuta Mizuki
'''
def index_of_str(s1, s2):
    lt=s1.split(s2,1)
    if len(lt)==1:
        return -1
    return len(lt[0])
'''
    将识别出的文字前面的空格去掉的函数
    return ：删减后的文字内容
    author ：enhenghahouxi
'''
def removespace(textcontent):
    #print(textcontent)
    a=textcontent
    for i in range(len(a)):
        if(a[0]==' '):
            a=a[1:]
        if(a[0]!=' '):
            textcontent=a
            return textcontent

'''
    减少题号没有没识别完全导致错误的函数
    return ：True/False
    author ：tt
'''   
#减少题号没有没识别完全导致错误的情况
def questionnumber_FixedJudgeTool(textcontent):
    textcontent=removespace(textcontent)
    flag_dict=['[0-9]+[^0-9]','[0-9]+设.+(为|则)','本题满分[0-9]+分','Section','\.完型填空','Text [0-9]+','的.+(方程|结果|条件)为']
    nn=0
    for p in flag_dict:
        pattern1=re.compile(p)
        res=pattern1.findall(textcontent)
        if(len(res)==1):  
            a=index_of_str(textcontent,res[0])
            if(nn==0 and a==0):         
                a=int(re.sub("\D", "", res[0]))
                b=0
                b=int(re.sub("\D", "", GL.questionnumber))
                if(b!=0):
                    if(a==(b+1)):
                        return True
                #第一题的题号就没完全识别的情况
                if(GL.questionnumber=="0."):
                    GL.questionnumber=="1."
                    return True
            if(nn!=0):
                return True           
        else:
            #存在句子开头为数字的情况，一句话中存在多个数字的情况
            '''TODO'''
        nn=nn+1 
         
    return False

'''
    判断是否有题号，以及题号的类型的函数
    return ：True/False,题号(1,2,3,4,5,6,7,8,9),"666"/"404"
    author ：tt
''' 
#判断是否有题号，以及题号的类型的函数
def questionnumber_JudgeTool(textcontent):
    
    '''questionnumber_dict=["[一二三四五六七八九十]+、","[一二三四五六七八九十]+\.","[0-9]+\.","[0-9]+、"
                         ,"[Ee][Gg].[0-9]+","\([0-9]+\)","\([一二三四五六七八九十]+\)"]'''
    textcontent=removespace(textcontent)
    
    questionnumber_dict=["[一二三四五六七八九十]+、","[一二三四五六七八九十]+\.","[0-9]+\.","[0-9]+、"
                         ,"[Ee][Gg].[0-9]+","\([0-9]+\)","\([一二三四五六七八九十]+\)"]
    key=textcontent
    i=0
    for p in questionnumber_dict:
        pattern1 = re.compile(p)
        res=pattern1.findall(key)
        #print(res)
        i=i+1
        
        if(len(res)==0):
            continue
        elif(len(res)==1):
            a=index_of_str(key,res[0])
            #print(a)
            if(a==0): 
                #print("before:questionnumber->:",GL.questionnumber)
                GL.questionnumber=res[0]
                #print("after:questionnumber->:",GL.questionnumber)
                return True,i,"666"
            else:
                return False,i,"404"
        else:
            a=index_of_str(key,res[0])
            #print(a)
            if(a==0):
                GL.questionnumber=res[0]
                return True,i,"404"
            else:
                return False,i,"404" 
    return False,0,"505"




'''
    判断一句话是否为选择题选项的函数
    判断是否为A.,B.,C.,D.开头，并与后三句话进行匹配
        达成A，B，C，D／A,B,C/a,b,c,d/a,b,c认为是选择题的选项
    return ：True／False,ABCDstyle(0 or 1 or 2 or 3 or 4),code(标示码)
    author ：Yuta Mizuki

'''  
#判断是否为选择题的选项的函数
def option_JudgeTool(textcontent):
    option_dict=["[Aa]\.","[Bb]\.","[Cc]\.","[Dd]\."]
    key=textcontent
    i=0
    for p in option_dict:
        pattern1 = re.compile(p)
        res=pattern1.findall(key)
        #print(res)
        i=i+1
        if(len(res)==0):
            continue
        elif(len(res)==1):
            a=index_of_str(key,res[0])
            #print(a)
            if(a==0):
                return True,i,"666"
            else:
                return False,i,"404"
        else:
            a=index_of_str(key,res[0])
            #print(a)
            if(a==0):
                return True,i,"404"
            else:
                return False,i,"404" 
    return False,0,"505"

'''
    判断一句话是否为考试注意事项的函数

    return ：True／False,code(标示码)
    author ：Yuta Mizuki

'''   
def note_JudgeTool(textcontent):
    note_dict=["注意事项","本试题.*部分","(姓名|座位号|座号|准考证号).*相应位置","铅笔.*答案",
               "(签字笔|水笔).*答题卡","答题区域","(切记不要|切忌).*答题"]
    key=textcontent
    i=0
    for p in note_dict:
        pattern1 = re.compile(p)
        res=pattern1.findall(key)
        #print(res)
        i=i+1
        if(len(res)==0):
            continue
        elif(len(res)==1):
            if(i==1):
                return True
            else:
                return True
        else:
            return True
    return False

'''
    判断一句话是否为题干的函数
    主要考虑到文本语气／题号及其位置／(选项判断及其位置)
    in ：textcontent (result['words'])
    return ："YES"(确认是题干)/"NO"(不确认是题干)，numberstyle（题号的类型）,code(标示码)
    code：404:存在题号，没有问题情感，可能是注意事项之类的／也可能是判断题的陈述
          505:不存在题号，也没有问题情感，也不属于选择项
          
    author ：Yuta Mizuki
'''
def question_JudgeTool(textcontent):
    x=textcontent
    #判断是否为疑问／命令／是非判断
    isorder,c=questionemotion_JudgeTool(x)
    #判断是否有题号，以及题号的类型
    hasquestionnumber,numberstyle,code=questionnumber_JudgeTool(x)
    #print(c)
    if(isorder==True):
        '''初步认为是可能为疑问的题干。但也有可能是阅读题中的反问或者是选择题选项中的问句'''
        if(hasquestionnumber==True):
            return True,numberstyle,"11"
        else:
            #也可能是题号没有被识别出来 如 9. 的 . 没有被识别
            if(questionnumber_FixedJudgeTool(x)==True):
                return True,0,"fixed"
            
            isoption,optionstyle,optioncode=option_JudgeTool(x)
            if(isoption==True):
                return False,0,"101"
            else:
                return  False,0,"100"
    elif(isorder==False):
        '''初步认为不为疑问／命令／是非判断。但也有可能是判断题中的陈述句。'''
        if(hasquestionnumber==True):
            '''有题号，所以大致认为是一道题里面的内容'''
            if(note_JudgeTool(x)==True):
                return False,0,"011"#注意事项等
            else:
                return True,0,"010"#判断题中的陈述句
        else:
            '''既没有题干语气，又没有题号，最难判断的一类。不出意外就是需要忽略的内容'''
            #也可能是题号没有被识别出来 如 9. 的 . 没有被识别
            if(questionnumber_FixedJudgeTool(x)==True):
                return True,0,"fixed"
            
            isnote=note_JudgeTool(x)
            if(isnote==True):
                return False,0,"001"#"注意事项"
            else:
                isoption,optionstyle,optioncode=option_JudgeTool(x)
                if(isoption==True):
                    return False,0,"0001"#选择题选项
                else:
                    if(questionnumber_FixedJudgeTool(x)==True):
                        return True,0,"fixed"
                    return False,0,"0000"#毫无结果
            