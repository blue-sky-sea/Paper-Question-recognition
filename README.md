========================================
# Paper-Question-recognition
========================================

question‘s area recognition using image processing and regular expression

![image](https://user-images.githubusercontent.com/26008298/130005551-f915e584-8acb-4dfc-a977-f8b74aeb0493.png)

bilibili宣传视频：
https://www.bilibili.com/video/av53893090


## 当前系统及库版本

Windows：win10
anaconda: Anaconda navigator 1.9.2
opencv: Opencv3 3.1.0
AipOcr: 百度ocr库最新
re: re库，自带
python：Python 3.7.0

## 系统总体思路
![image](https://user-images.githubusercontent.com/26008298/130005662-fc9aee07-1873-4b90-aa88-53dc6508f069.png)

## 预处理
![image](https://user-images.githubusercontent.com/26008298/130005705-df8fc1af-5c5d-4193-98ff-7e668488b6cb.png)
<br />  

透视矫正：目标找到纸的四个点然后矫正成右下图的样子  

![image](https://user-images.githubusercontent.com/26008298/130005746-cace47ed-3050-4ed4-a51d-f3287eedd9aa.png)

**如何找到四个点？**
**有两大方法：Canny边缘检测和霍夫直线检测**  

边缘检测效果：得到近似轮廓从而获得四个点的位置  

![image](https://user-images.githubusercontent.com/26008298/130005779-dcb86bc1-0156-4330-af93-687f94f1d5ac.png)

**双页试卷处理：**
类似这种图片，需要把试卷分成左右两份  

![image](https://user-images.githubusercontent.com/26008298/130005813-e81bbd56-fa0d-430d-bc8a-340388b2b6b5.png)  

我们的思路是：
1.选取中间部分的区域（如40%~60%）我们考虑上下也各截取了一部分，将该区域二值化<br />
2.找到连续白色区域最多，但又远大于字与字空隙的距离的区域<br />
3.计算这个区域的中心线后，这条线就是我们要找的双页试卷的切割线（橙色）<br />  

![image](https://user-images.githubusercontent.com/26008298/130005859-5541a6ac-9b6b-4717-bdda-68f54f4f0b17.png)  

这个方法甚至可以处理两页之间中间有直线的试卷。只要存在满足一定条件的空白区域就可以找到分割线。

**文字识别**
最初我们用teseeract库作识别，但是识别精度感人，jTesssBoxEditor训练字库的效果也很感人。<br />  

时间紧迫，我们就选择了百度Ocr的API接口作为文字识别的工具。缺点是，免费版低精度一天只有500次的使用次数。

**自然语言处理**

这一部分是划分题目的重中之重。
我们之前的想法是，判断识别出的某一段是否为题干，如果是题干，那么就把它和上面的部分划分开来。
但是，判断题干的效果并不好。原因在于：
1.ocr文字识别出现误差，没有识别出必要的题号等标志性词。
2.没有良好的分词。
3.正则表达式判断题干情感（比如：‘’请问…的答案是‘’、‘’以下…正确的是“ 这种一看就是题目的题干的结构）难以尽善尽美，往往需要后期debug才能补充；
简而言之，能否正确识别出题干，是我们最需要关心的。
只要识别出题干，那么上一题就被分出来了。

![image](https://user-images.githubusercontent.com/26008298/130005948-58a03361-5fef-4301-bf54-af14a388e017.png)  

另外还要考虑一下 注意事项，等无关紧要的东西不要被划分成题目。
划分出选择题的思路大致也和上面一样

**划分题目区域**

由于百度ocr接口除了文字还附带位置信息，所以我们只需要把每道题的题干+题目内容的位置信息合并就可以知道整道题的位置信息了。
ocr接口位置信息有4个变量（top，left，height，width），如下。

![image](https://user-images.githubusercontent.com/26008298/130006047-29d1bfe0-ccf2-465b-ae9a-116aa7013c9a.png)  

一道题按理来说就包括了图中的两个红框的位置信息，只要综合考虑位置信息，一定可以得到整道题的位置信息。  

![image](https://user-images.githubusercontent.com/26008298/130006072-12c5f23b-0c62-4be0-b66b-2bb394a6f738.png)  

但是实际操作中出现了意外，一道题当最后一行压根没有识别出来怎么办。<br />
解决办法是，根据下一道题的top信息来计算上一道题的height，这样就避免了 A.北京人遗址这一行没被识别出来的尴尬。  

![image](https://user-images.githubusercontent.com/26008298/130006098-bc92103a-8217-4871-b54a-9392e5c26583.png)  

**前端**

综合考虑，我们还是使用了python的tkinter库制作前端。
很简单，很朴素。  

![image](https://user-images.githubusercontent.com/26008298/130006132-5fd1c512-b6ce-44a3-b58f-a1188749e4fc.png)  

包括了选择图片所在的文件夹，切题结果保存的文件夹，预处理，是否 人工校对，开始切题的功能。

如果开启了人工校对，切题完成后会出现校对页面。右边是原图，左边是切题结果。  

![image](https://user-images.githubusercontent.com/26008298/130006157-e2c1f293-5438-4bb5-aca2-0a4f75ef50b4.png)
