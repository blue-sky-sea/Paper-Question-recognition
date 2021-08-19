import sys
sys.path.append('D:\python3.6\Lib\site-packages')


from tkinter import *
import tkinter.filedialog as filedialog
import tkinter.messagebox #这个是消息框，对话框的关键
#from tkinter.filedialog import askopenfilename
from PIL import Image,ImageTk
import PIL
import os
import os.path
import Main
import imghdr
import _thread
import threading
import time
import cv2



#import OptimizeTool as tool

source_dirpath=""
save_dirpath=""
showingimage_filepath = ""

#再次进行开始识别时需要init的全局变量
showingimage_index=0
imagefilepaths = []
save_imagefilepaths = []
save_imagenumber=0
deleted_imagenumber=0

artificialjudge="yes"
artificialjudge2="no"



imagefilepaths = []
save_imagefilepaths = []

save_imagenumber=0
deleted_imagenumber=0
all_imagenumber=0#总共有几张要处理
imagenumber=0#当前正在处理第几张

pretreat_all_imagenumber=0#总共有几张要预处理
pretreat_imagenumber=0#当前正在预处理第几张
startocr_finished=False



class mainapp:
    
    
    '''
        实现系统界面的函数
        return ：无
        author ：tt
    '''
    def __init__(self):
        root=Tk()
        root.title("自动切题系统")
        root.geometry('400x340')
        root.resizable(width=False, height=True) 
        self.v = StringVar()#绑定文本框的变量
        self.v.set("请选择文件夹...")
        ent = Entry(root, width=30,textvariable = self.v)
        ent.place(relx=0.41,rely=0.1,anchor=CENTER)
        button1 = Button(root, text='选择文件夹', command=self.choose_sourcedirpath)
        button1.place(relx=0.77,rely=0.1,anchor=CENTER)

        self.var = StringVar()#绑定listbox的列表值
        self.var.set((''))
        self.listbox = Listbox(root,width=40,listvariable = self.var).place(relx=0.5,rely=0.42,anchor=CENTER)
        self.button2=Button(root,text='开始切题',command=self.starter).place(relx=0.21,rely=0.75,anchor=CENTER)
        self.button2=Button(root,text='点我预处理',command=self.pretreater).place(relx=0.4,rely=0.75,anchor=CENTER)
        #self.consolelabel=Label(root,text = '...')
        #self.consolelabel.place(relx=0.2,rely=0.7,anchor=CENTER)
        
        
        self.checkbutton=Checkbutton(root,text='是否人工校对结果',command = self.callCheckbutton)
        self.checkbutton.place(relx=0.72,rely=0.74,anchor=CENTER)
        self.checkbutton.select()
        
        #self.checkbutton2=Checkbutton(root,text='是否处理双页试卷',command = self.callCheckbutton2)
        #self.checkbutton2.place(relx=0.4,rely=0.7,anchor=CENTER)
        #self.checkbutton.select()
        #self.lb = Label(root,text = '')
        #self.lb.place(relx=0.2,rely=0.7,anchor=CENTER)
        
        self.v2 = StringVar()#绑定文本框的变量
        self.v2.set("请选择切题结果保存文件夹...")
        ent2 = Entry(root, width=30,textvariable = self.v2)
        ent2.place(relx=0.41,rely=0.85,anchor=CENTER)
        button3 = Button(root, text='选择文件夹', command=self.choose_savedirpath)
        button3.place(relx=0.77,rely=0.85,anchor=CENTER)
        root.mainloop()
    
    
    '''
        改变Checkbutton的显示值的函数
        return ：无
        author ：tt
    '''
    def callCheckbutton(self):
        #改变v的值，即改变Checkbutton的显示值
        global artificialjudge
        if(artificialjudge=="no"):
            artificialjudge='yes'
            #print(artificialjudge)
        elif(artificialjudge=="yes"):
            artificialjudge='no'
            #print(artificialjudge)
            
            
    '''
        选择图片所在文件夹路径的函数
        return ：无
        author ：tt
    '''
    def choose_sourcedirpath(self):
        self.v.set('')#清空文本框里内容
        self.var.set((('')))
        #filename = tkinter.filedialog.askopenfilename()
        global source_dirpath 
        source_dirpath = filedialog.askdirectory()
        print(source_dirpath)
        if source_dirpath :
            self.v.set(source_dirpath)
        self.getdir(source_dirpath)
        
        
    '''
        选择要存储图片所在文件夹路径的函数
        return ：无
        author ：tt
    '''  
    def choose_savedirpath(self):
        self.v2.set('')#清空文本框里内容
        global save_dirpath 
        save_dirpath  = filedialog.askdirectory()
        #print(dir(filedialog))
        print(save_dirpath )
        if save_dirpath  :
            self.v2.set(save_dirpath)
            
            
    '''
        把文件夹中图片显示在列表框的函数
        return ：无
        author ：tt
    '''          
    def getdir(self,dirpath):
        #把目录中遍历出来的文件目录显示到列表框中
        global fp
        fp = os.listdir(dirpath)
        self.var.set(fp)
        
        
       
    def global_init1(self):
        global showingimage_index
        global imagefilepaths
        global save_imagefilepaths
        global save_imagenumber
        global deleted_imagenumber
        showingimage_index=0
        imagefilepaths = []
        save_imagefilepaths = []
        save_imagenumber=0
        deleted_imagenumber=0
        
        
    '''
        图片预处理的函数
        return ：无
        author ：tt
    '''      
    def pretreater(self):
        if(source_dirpath=="" ):
            tkinter.messagebox.showinfo('提示',"请先选择图库文件夹的路径！")
            print("请先选择图库文件夹的路径！")
            return 0
        else:
           self.global_init1()
        b=tkinter.messagebox.askyesno('确认要开始预处理吗？',"这可能需要几秒甚至几分钟！")
        if(b==True):
            global pretreat_all_imagenumber
            paths=self.get_imagefilepaths_bydirpath(source_dirpath)
            if(len(paths)<=0):
                tkinter.messagebox.showinfo('不行哦','文件夹下没有可用的图片')
                return 0
            pretreat_all_imagenumber=len(paths)  
            tbar=threading.Thread(target=pretreat_progressbar,args=())
            tbar.setDaemon(True)#设置为后台线程
            t = threading.Thread(target=self.twopages_cutTool,args=(source_dirpath,1))
            t.setDaemon(True)#设置为后台线程
            tbar.start()#开启线程
            t.start()#开启线程
            
            
    '''
        把图片进行切割的函数
        return ：无
        author ：tt
    '''        
    def starter(self):
        if(source_dirpath=="" or save_dirpath==""):
            tkinter.messagebox.showinfo('提示',"请先选择图库文件夹和保存文件夹的路径！")
            print("请先选择图库文件夹和保存文件夹的路径！")
            return 
        else:
            self.global_init1()
        if(artificialjudge=="no"):
            tkinter.messagebox.showinfo('提示',"文件夹中的图片已经开始切题！请稍后到指定文件夹中查看")
            #self.startOcr(source_dirpath,save_dirpath)
            t = threading.Thread(target=self.startOcr,args=(source_dirpath,save_dirpath))
            t.setDaemon(True)#设置为后台线程
            t.start()#开启线程
        else:   
            '''global artificialjudge2
            if(artificialjudge2=="yes"):
                tkinter.messagebox.askyesno('首先进行双页试卷的预处理',"这可能需要几秒甚至几分钟！")
                t = threading.Thread(target=tool.twopages_cutTool,args=(source_dirpath))
                
                
                imagefilepaths=self.get_imagefilepaths_bydirpath(source_dirpath)'''
            #_thread.start_new_thread(tkinter.messagebox.askokcancel,('确认开始切题吗？',"这可能需要几秒甚至几分钟！"))
            b=tkinter.messagebox.askyesno('确认要开始切题吗？',"这可能需要几秒甚至几分钟！")
            if(b==True):
                tbar=threading.Thread(target=progressbar,args=())
                tbar.setDaemon(True)#设置为后台线程
                t = threading.Thread(target=self.startOcr,args=(source_dirpath,save_dirpath))
                t.setDaemon(True)#设置为后台线程
                tbar.start()#开启线程
                t.start()#开启线程
                
                
    '''
        显示出正在切割的图片的信息的函数
        return ：无
        author ：tt
    '''            
    def startOcr(self,source_dirpath,save_dirpath):
        global imagefilepaths
        global all_imagenumber
        imagefilepaths=self.get_imagefilepaths_bydirpath(source_dirpath)
        if(len(imagefilepaths)<=0):
            print("文件夹下没有可用的图片")
            return
        else:
            all_imagenumber=len(imagefilepaths)   
        
        global imagenumber
        imagenumber=1
        for filepath in imagefilepaths:
            print("#####################################")
            print("ocr controller:start ocr for ",filepath)
            #consolemessage="正在处理第"+str(imagenumber)+"张..."
            #self.consolelabel.configure(text=consolemessage)
            Main.singleocr(filepath,save_dirpath,0)
            imagenumber=imagenumber+1
        global startocr_finished
        startocr_finished=True
        return
    
    
    
    def changeconsole(self,consolemessage):
        self.consolelabel.configure(text=consolemessage)
        
        
    '''
        判断是否是图片的函数
        return ：True/False
        author ：tt
    '''    
    def is_img(self,ext):
         ext = imghdr.what(ext)
         #print(ext)
         if ext == 'jpg':
          return True
         elif ext == 'png':
          return True
         elif ext == 'jpeg':
          return True
         elif ext == 'gif':
          return True
         else:
          return False   
      
        
    '''
        得到图片路径的函数
        return ：图片绝对路径
        author ：tt
    '''    
    def get_imagefilepaths_bydirpath(self,source_dirpath):  
        if not os.path.isdir(source_dirpath):
            #tkinter.messagebox.showinfo('提示',"这不是一个文件夹")
            print("这不是一个文件夹")
            return

        global files
        files = os.listdir(source_dirpath) 
        imagefilepaths=[]
        for index in range(len(files)):
            path = "%s/%s" %(source_dirpath,files[index])   
            if os.path.isdir(path):
                files[index] = ""#将文件夹对象设为空
            else:
                filepath=source_dirpath+"/"+files[index]
                if(self.is_img(filepath)==True):
                        filename=filepath.split('/')[-1]
                        if(filename[0]!="_"):
                            imagefilepaths.append(source_dirpath+"/"+files[index])
        return imagefilepaths 
    
    
    '''
        把一张包括两页的试卷切成两面的函数
        return ：无
        author ：tt
    '''  
    def twopages_cutTool(self,source_dirpath,e):
        global pretreat_all_imagenumber
        imagefilepaths=self.get_imagefilepaths_bydirpath(source_dirpath)
        if(len(imagefilepaths)<=0):
            print("文件夹下没有可用的图片")
            return
        else:
            pretreat_all_imagenumber=len(imagefilepaths)   
        files = os.listdir(source_dirpath)
        #print("TEST@@##$files:",files)
        global pretreat_imagenumber
        pretreat_imagenumber=1
        for index in range(len(files)):
            #print("twopahes_cutTool:index:",index)
            path = "%s/%s" %(source_dirpath,files[index])   
            if os.path.isdir(path):
                files[index] = ""#将文件夹对象设为空
            if(files[index][0]=="_"):
                print("[twopages_cutTool:]image ignored!")
                continue
            else:
                imagepath=source_dirpath+"/"+files[index]
                if(self.is_img(imagepath)==True):
                    #print("start to cut two pages for:",imagepath)
                    self.cutimage_Tool(source_dirpath,imagepath) 
            pretreat_imagenumber=pretreat_imagenumber+1  
            
            
    '''
        把一张包括两页的试卷切成两面的地址存入所有图片存储的地址的函数
        return ：无
        author ：tt
    '''        
    def crop_Tool(self,filepath,save_dirpath,cut_line_x):
        img = cv2.imread(filepath)
        imgshape = img.shape
        height = imgshape[0]
        width = imgshape[1]
        savepath1="./"
        savepath2="./"
        filename=filepath.split('/')[-1]
        filename=filename.split('.')[0]
        cropped1 = img[0:height , 0:cut_line_x]
        savepath1=save_dirpath+"/"+filename+"left.jpg" 
        print(savepath1)
        cv2.imwrite(savepath1, cropped1)
        
        cropped2 = img[0:height , cut_line_x:width]
        savepath2=save_dirpath+"/"+filename+"right.jpg" 
        print(savepath2)
        cv2.imwrite(savepath2, cropped2)
    
    
    '''
        把一张包括两页的试卷切成两面的地址存入所有图片存储的地址的函数
        return ：无
        author ：tt
    '''
    def cutimage_Tool(self,source_dirpath,imagepath):   
        #读取图片
        img = cv2.imread(imagepath)
        orishape = img.shape
        #调整图片大小
        sizek = 600/orishape[1]
        resize = cv2.resize(img, None, fx=sizek, fy=sizek)
        #灰度化
        gray = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)
        imgshape = gray.shape
        sum = 0
        for i in range(imgshape[0]):
            for k in range(imgshape[1]):
                sum =sum+ int(gray[i,k])
        result = sum / (imgshape[0]*imgshape[1])
        #print(result)
        
        #二值化
        ret,binary = cv2.threshold(gray,int(result),255,cv2.THRESH_BINARY)
        #闭运算除去白色中的黑噪声
        #kernel = np.ones((5,5),np.uint8)
        #close = cv2.morphologyEx(binary,cv2.MORPH_CLOSE,kernel)
    
        tempshape = binary.shape
        height = tempshape[0]
        width = tempshape[1]
        #midwidth = width/2
        #设置裁剪范围，获得图片中间部分的区域
        xl = 0.40
        xr = 0.60
        yt = 0.25
        yb = 0.75
        store_start = 0
        #store_end = 0
        temp_start = 0
        #temp_end = 0
        #ROI_BGR = resize[int(yt*height):int(yb*height),int(xl*width):int(xr*width)]
        #裁剪出中间部分
        ROI = binary[int(yt*height):int(yb*height),int(xl*width):int(xr*width)]
        ROIshape = ROI.shape
        #print("ROI:"+ str(ROIshape))
        ROIheight = ROIshape[0]
        ROIwidth = ROIshape[1]
        #print(ROIheight,ROIwidth)
        #获得裁剪部分每列像素点中黑色像素点所占的比例
        xRate = []
        store_series_num = 0 
        temp_series_num = 0
        for i in range(ROIwidth):
            sum = 0#每列黑点的总数
            for k in range(ROIheight):
                a=int(ROI[k,i])
                #print(a," ",end='')
                if(a == 0): 
                    sum += 1
            rate = sum/ROIheight*1.0
            #print(sum)
            #print(rate)
            xRate += [rate]#ROI区域中每列黑点的比率
        #print(xRate)
        findblackline_flag = False
        for i in range(len(xRate)):
           if xRate[i] <=0.0001:#整列都是白色
              if temp_series_num == 0:
                  temp_start = i
              temp_series_num += 1 
           elif xRate[i]>=0.9999:#整列都是黑色
               findblackline_flag = True
               store_start = i
               break
           else:
              if temp_series_num > store_series_num :
                  store_series_num = temp_series_num
                  store_start = temp_start
              temp_series_num = 0  
           '''if(store_series_num==0 and i==(len(xRate)-1)):
               store_series_num=len(xRate)
               break'''
        #print("ROIwidth:",ROIwidth)#截取区域长度
        #print("store_series_num:",store_series_num)#白色区域长度
        if(findblackline_flag==False and (store_series_num/ROIwidth)<=0.05):
            print(imagepath)
            print("no need to cut")
            return
        #linesimage = ROI_BGR.copy()         
        #cv2.line(linesimage, (store_start, 0), (store_start, ROIheight), (255, 0, 0), 1, cv2.LINE_AA)
        #cv2.line(linesimage, (store_start+store_series_num, 0), (store_start+store_series_num, ROIheight), (0, 255, 0), 1, cv2.LINE_AA)
        #cv2.imshow("line",linesimage)
        #获得要截取的位置的x坐标，为白色区域的中间
        ROIxl = store_start
        if(findblackline_flag==False):
            ROIxl = (store_start+store_series_num/2)
        cut_line_x = int((width*xl + ROIxl)/sizek)
        #print(sizek)
        #print(ROIxl)
        #print(cut_line_x)
        '''cut_img = img.copy()
        cv2.line(cut_img, (cut_line_x, 0), (cut_line_x, height), (0, 0, 255), 1, cv2.LINE_AA)
        cv2.imshow("cut_img",cut_img)'''
        self.crop_Tool(imagepath,source_dirpath,cut_line_x)
        
        #对原图像在原文件夹中进行重命名
        filename=imagepath.split('/')[-1]
        filename=filename.split('.')[0]
        newimagepath=source_dirpath+"/"+"_"+filename+".jpg"
        try:
            os.rename(imagepath,newimagepath)
        except Exception as e:
            print(e)
            print('rename dir fail\r\n')
        #cv2.imshow("close",close)
        #cv2.imshow("ori",resize)
        #cv2.imshow("ROI",ROI)
        #print(xRate)
        
        #2.imshow("binary",binary)
        print("cutImageTool: waitkey before")
        #cv2.waitKey(0)     
        print("cutImageTool: waitkeyafter")
        return
        
'''
    显示预处理进度的进度条界面，显示预处理当前的进度，进度完成后提示完成
    author ：Yuta Mizuki
'''   
class pretreat_progressbar:
    def __init__(self):
        self.r=Toplevel()
        self.r.title('预处理进度')
        self.r.geometry('630x150')
        # 设置下载进度条
        Label(self.r, text='处理进度:', ).place(x=50, y=60)
        self.c = Canvas(self.r, width=465, height=22, bg="white")
        self.c.place(x=110, y=60)
        #self.progress()
        #btn_download =Button(self.r, text='启动进度条', command=self.progress)
        #btn_download.place(x=400, y=105)
        self.progress()
        self.r.destroy()
        
        
    '''
        能够把预处理的进度通过进度条的方式呈现出来的函数
        return ：无
        author ：tt
    '''    
    def progress(self):   
        global pretreat_all_imagenumber
        global pretreat_imagenumber
        fill_line = self.c.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
        if(pretreat_all_imagenumber==0):
            print("progress:pretreat_all_image_number==0")
            return
        x = 100*pretreat_all_imagenumber  # 未知变量，可更改
        tt=465
        n = 465 / x  # tt是矩形填充满的次数,n为当前进度条的长度

        cut=465 / pretreat_all_imagenumber
        nn=1#当前正在处理第nn张图片，初始为1
       
        for i in range(x-1):
            n = n + 465 / x
            self.c.coords(fill_line, (0, 0, n, 60))
            self.r.update()
            time.sleep(0.03)
            while(n>=cut*nn):
                time.sleep(0.03)
                #print("n:",n," nn:",nn," cut*nn",cut*nn,"pretreat_imagenumber",pretreat_imagenumber)
                if(pretreat_imagenumber>nn):
                    #print("chulai")
                    break
            nn=pretreat_imagenumber
        tkinter.messagebox.askyesno('预处理成功',"现在你可以快乐地切题了")
        return
    
    
'''
    显示切题进度的进度条界面，显示切题当前的进度，进度完成后跳出showpic界面
    author ：Yuta Mizuki
'''   
class progressbar:
    
    
    
    def __init__(self):
        self.r=Toplevel()
        self.r.title('切题进度')
        self.r.geometry('630x150')
        # 设置下载进度条
        Label(self.r, text='切题进度:', ).place(x=50, y=60)
        self.c = Canvas(self.r, width=465, height=22, bg="white")
        self.c.place(x=110, y=60)
        #self.progress()
        #btn_download =Button(self.r, text='启动进度条', command=self.progress)
        #btn_download.place(x=400, y=105)
        self.progress()
        self.r.mainloop()
        
        
    '''
        能够把切题的进度通过进度条的方式呈现出来的函数
        return ：无
        author ：tt
    '''    
    def progress(self):   
        global all_imagenumber
        global imagenumber
        fill_line = self.c.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
        if(all_imagenumber==0):
            print("progress:all_image_number==0")
            return
        #print("【progress func】ALL_IMAGENUMBER:",all_imagenumber,"imagenumber:",imagenumber)
        x = 100*all_imagenumber  # 未知变量，可更改
        tt=465
        n = 465 / x  # tt是矩形填充满的次数,n为当前进度条的长度

        cut=465 / all_imagenumber
        nn=1#当前正在处理第nn张图片，初始为1
       
        for i in range(x-1):
            n = n + 465 / x
            self.c.coords(fill_line, (0, 0, n, 60))
            self.r.update()
            #print("***n=",n,"***",end="")
            time.sleep(0.03)
            while(n>=cut*nn):
                time.sleep(0.03)
                #print("【progress func】n:",n," nn:",nn," cut*nn",cut*nn,"imagenumber",imagenumber)
                if(imagenumber>nn):
                    break
            nn=imagenumber
        
        showpic()    

'''
    人工校对的界面，显示切题结果的图片并且能够作手动删除操作
    author ：Yuta Mizuki
'''
class showpic:
    def __init__(self):
        r1=Toplevel()
        r1.title('切题结果人工校对')
        r1.geometry('1600x800')

        #根据图库路径source_dirpath开始遍历识别，识别结果存储在save_dirpath文件夹
        #self.startOcr(source_dirpath,save_dirpath)
        #_thread.start_new_thread(self.startOcr,(source_dirpath,save_dirpath))
        global save_imagefilepaths
        save_imagefilepaths=self.get_imagefilepaths_bydirpath(save_dirpath)
        global showingimage_filepath
        global save_imagenumber
        save_imagenumber=len(save_imagefilepaths)
        if(save_imagenumber!=0):
            showingimage_filepath=save_imagefilepaths[0]

        self.label=Label(r1,text='图片路径：')
        self.label.place(relx=0.01,rely=0.02)
        self.pathlabel=Label(r1,text=showingimage_filepath)
        self.pathlabel.place(relx=0.06,rely=0.02)
        
        
        global imagefilepaths
        img_open=Image.open(showingimage_filepath)
        print("img_open size",img_open.size)
        
        open_width = img_open.size[0]
        open_height = img_open.size[1]
        #调整图片大小
        sizek = 500/open_width
        
        
        #img_open.thumbnail((500,500))
        img_open=img_open.resize((int(sizek*img_open.size[0]),int(sizek*img_open.size[1])))
        img=ImageTk.PhotoImage(img_open)
        
        self.l1=Label(r1,image=img)
        self.l1.place(relx=0.01,rely=0.07)
        
        
        self.l2=Label(r1,text='未切割的图片：')
        self.l2.place(relx=0.45,rely=0.02)
        
        #未切割的图片的
        '''
        global imagepath
        filename=imagepath.split('/')[-1]
        filename=filename.split('.')[0]
        newimagepath=source_dirpath+"/"+filename+".jpg"
        img_open2=Image.open(newimagepath)
        img_open2.thumbnail((700,700))
        img2=ImageTk.PhotoImage(img_open2)
        self.l3=Label(r1,image=img2)
        self.l3.place(relx=0.45,rely=0.07)
        
        '''
        #lastvar1=self.lastvar(showingimage_filepath)
        #showingimage_filepath2=source_dirpath+showingimage_filepath[lastvar1:-7]+'.jpg'
        showingimage_filepath2=self.get_source_imagepath(source_dirpath,showingimage_filepath)
        img_open2=Image.open(showingimage_filepath2)
        img_open2.thumbnail((700,700))
        img2=ImageTk.PhotoImage(img_open2)
        self.l3=Label(r1,image=img2)
        self.l3.place(relx=0.45,rely=0.07)
        
        
        
        self.button2=Button(r1,text='下一张',command=self.jumpimage)
        self.button2.place(relx=0.03,rely=0.8,anchor=CENTER)
        self.button3=Button(r1,text='删除这张',command=self.deleteimage)
        self.button3.place(relx=0.09,rely=0.8,anchor=CENTER)
        r1.mainloop()
        
    
    
    def imageisexist(self,source_dirpath,a):
        if(os.path.exists(source_dirpath+'/'+a+'.jpg')):
            return source_dirpath+'/'+a+'.jpg'
        if(os.path.exists(source_dirpath+'/'+a+'.png')):
            return source_dirpath+'/'+a+'.png'
        if(os.path.exists(source_dirpath+'/'+a+'.jpeg')):
            return source_dirpath+'/'+a+'.jpeg'
        if(os.path.exists(source_dirpath+'/'+a+'.gif')):
            return source_dirpath+'/'+a+'.gif'
    
    
    def get_source_imagepath(self,source_dirpath,showingimage_filepath):
        a=showingimage_filepath.split('/')[-1]
        a=a.split('.')[0]
        a=a[:-3]
        return self.imageisexist(source_dirpath,a)
    
    
    
    def lastvar(self,showingimage_filepath):
        for i in range(-1,-1000,-1):
            if(showingimage_filepath[i]=='/'):
                return i

    
    '''
        把正在切第几张图片输出来的函数
        return ：无
        author ：tt
    '''    
    def startOcr(self,source_dirpath,save_dirpath):
        global imagefilepaths
        imagefilepaths=self.get_imagefilepaths_bydirpath(source_dirpath)
        if(len(imagefilepaths)<=0):
            print("文件夹下没有可用的图片")
            return 
        for filepath in imagefilepaths:
            print("ocr contoller:start ocr for ",showingimage_filepath)
            Main.singleocr(filepath,save_dirpath,0)
        
        
    '''
        判断切题的是否是图片的函数
        return ：无
        author ：tt
    '''    
    def is_img(self,ext):
         ext = imghdr.what(ext)
         #print(ext)
         if ext == 'jpg':
          return True
         elif ext == 'png':
          return True
         elif ext == 'jpeg':
          return True
         elif ext == 'gif':
          return True
         else:
          return False


    '''
        得到图片路径的函数
        return ：所有图片路径的列表
        author ：tt
    '''    
    def get_imagefilepaths_bydirpath(self,source_dirpath):  
        if not os.path.isdir(source_dirpath):
            #tkinter.messagebox.showinfo('提示',"这不是一个文件夹")
            print("这不是一个文件夹")
            return
        global files
        files = os.listdir(source_dirpath) 
        imagefilepaths=[]
        for index in range(len(files)):
            path = "%s/%s" %(source_dirpath,files[index])   
            if os.path.isdir(path):
                files[index] = ""#将文件夹对象设为空
            else:
                if(self.is_img(source_dirpath+"/"+files[index])==True):
                    imagefilepaths.append(source_dirpath+"/"+files[index])
        return imagefilepaths
    
    
    
    
    '''
        将图片跳到下一张及显示出图片绝对路径的函数
        return ：无
        author ：tt
    '''
    def jumpimage(self): #跳过
        global showingimage_filepath
        global save_imagefilepaths
        global showingimage_index
        '''print("jump前")
        print("showingimage_filepath is ",showingimage_filepath)'''
        global save_imagenumber
        global deleted_imagenumber
        showingimage_index=showingimage_index+1
        if((save_imagenumber+deleted_imagenumber)<=showingimage_index):
            self.pathlabel.configure(text="已经没有下一张了")
            tkinter.messagebox.showinfo('提示',"已经遍历完结果")
            #img_open=Image.open("./111.JPG")
            #img_open.thumbnail((600,600))
            #global lastimage#定义成全局变量才显示得出来！！！！！
            #lastimage = ImageTk.PhotoImage(img_open) #需要储存为实例属性，否则会被垃圾回收
            #self.l1.configure(image=lastimage)
            self.button2.configure(state=DISABLED)
            self.button3.configure(state=DISABLED)
            return
            
        showingimage_filepath=save_imagefilepaths[showingimage_index]
        self.pathlabel.configure(text=showingimage_filepath)
        
        '''print("jump后")
        print("showingimage_filepath is ",showingimage_filepath)'''
        

        print("test board:showing ",showingimage_filepath)
        img_open=Image.open(showingimage_filepath)
        #调整图片大小
        open_width = img_open.size[0]
        open_height = img_open.size[1]
        sizek = 500/open_width
        #img_open.thumbnail((500,500))
        img_open=img_open.resize((int(sizek*img_open.size[0]),int(sizek*img_open.size[1])))
        
        '''这里有踩过的坑'''
        global newimage#定义成全局变量才显示得出来！！！！！
        newimage = ImageTk.PhotoImage(img_open) #需要储存为实例属性，否则会被垃圾回收
        self.l1.configure(image=newimage)##

        
        '''
        lastvar1=self.lastvar(showingimage_filepath)
        showingimage_filepath2=source_dirpath+showingimage_filepath[lastvar1:-7]+'.jpg'
        img_open2=Image.open(showingimage_filepath2)
        img_open2.thumbnail((700,700))
        global newimage2#定义成全局变量才显示得出来！！！！！
        newimage2 = ImageTk.PhotoImage(img_open2) #需要储存为实例属性，否则会被垃圾回收
        self.l3.configure(image=newimage2)##
        '''
        
        showingimage_filepath2=self.get_source_imagepath(source_dirpath,showingimage_filepath)
        img_open2=Image.open(showingimage_filepath2)
        img_open2.thumbnail((700,700))
        global newimage2#定义成全局变量才显示得出来！！！！！
        newimage2 = ImageTk.PhotoImage(img_open2) #需要储存为实例属性，否则会被垃圾回收
        self.l3.configure(image=newimage2)##
        
        
        
    '''
        将不要的图片进行删除的函数
        return ：无
        author ：tt
    '''
    def deleteimage(self):   #删除
        global showingimage_filepath
        delete_path=showingimage_filepath
        a=tkinter.messagebox.askyesno('提示',"确定要删除吗")
        if(a==False):
            return
        print("test board:delete*** ",showingimage_filepath)
        global save_imagenumber
        global deleted_imagenumber
        save_imagenumber=save_imagenumber-1
        deleted_imagenumber=deleted_imagenumber+1
        self.jumpimage()
        os.remove(delete_path)
        tkinter.messagebox.showinfo('提示',"删除成功")
        
        
mainapp()