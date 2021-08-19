# Ethereum-Score-Hella

## 环境准备

### 当前系统及库版本

anaconda: Anaconda navigator 1.9.2

opencv: Opencv3 3.1.0

python：Python 3.7.0

imutils：newest

### 环境安装(cmd中记得先进入环境，在conda中安装可能出现网络不通的情况（比较玄学）)
1.下载anaconda：https://www.anaconda.com
1.1anaconda安装spyder等基本开发环境

2.anaconda命令行创建虚拟环境（python建议3.7）：
conda create -n your_env_name python=X.X 

3.imutils库 conda install -c gilbertfrancois imutils 


### 代码使用指南
	安装了基本的环境后。
	discorr.py为canny边缘检测的实现代码
	discorr2.py为霍夫直线检测的实现代码
	test.py为对这两个方法进行test的代码


### 项目版本更新：

main4.2－00.00 :获得了基本的以canny边缘检测为方法的demo并成功运行

main4.14-00:00 :获得了基本的以霍夫直线检测为方法的demo并成功运行

main4.26-21:40 :实现了针对试卷图片的两个检测方法的参数调整，并test成功

main4.28-16:00 :优化canny边缘检测方法下背景和纸张颜色相近时的判定

main5.5-20:20 :优化了霍夫直线筛选条件




