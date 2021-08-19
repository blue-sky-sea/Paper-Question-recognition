# Ethereum-Score-Hella

## 环境准备

### 当前系统及库版本

anaconda: Anaconda navigator 1.9.2

opencv: Opencv3 3.1.0

AipOcr: Newest

re: Common

python：Python 3.7.0

### 环境安装(cmd中记得先进入环境，在conda中安装可能出现网络不通的情况（比较玄学）)
1.下载anaconda：https://www.anaconda.com
1.1anaconda安装spyder等基本开发环境

2.anaconda命令行创建虚拟环境（python建议3.7）：
conda create -n your_env_name python=X.X 

3.激活虚拟环境(your_env_name即你的环境的名字)
source activate your_env_name

4.安装opencv（opencv-python的版本号可能不同，不同版本号可能与一些系统不兼容，后面的镜像源可以更换，openc的版本号按理来说应该可以更换成最新的）
pip install opencv-python==3.4.2.16 -i https://pypi.mirrors.ustc.edu.cn/simple/
或者
anaconda里面用包管理器安装(可能是网络和墙的问题，经常安装不成功)

5.安装baidu-aip包
pip install baidu-aip

### 代码使用指南
	安装了基本的环境后。
	运行python_GUI.py可以出现GUI界面。
	运行Main.py的test（）可直接进行切题（可在test中修改图片路径）。
	temp.py可更改百度OCR api的相关配置。
	JudgeTool.py中主要是功能代码。


### 项目版本更新：
main3.29－00.00 :接通了百度api文本识别接口，实现了基本的自然语言处理（对基本题号和题目情感倾向的处理）

main3.31-18.46 :优化了自然语言处理过程（增加了对题目选项的语意识别），增加了新的工具函数

main4.2－00.00 :优化了自然语言处理效果（增加了对注意事项等无关内容的排除），实现了基本的切题功能

main4.14-00:00 :解决了自然语言处理的bug，实现了基本题型的高成功率识别，解决了图片切割范围判定逻辑的问题

main4.14-23:00 :实现了题号识别不出‘.’时，依然可以根据题号顺序规律将其划分出来。

main4.26-21:40 :实现了基本的GUI图形界面，构建了基本的批量识别图片的功能。

main4.28-13:25 :修改了题号识别不准确情况下题目的判定模块，修复了图形化界面删除图片后顺序错乱的bug

main4.28-16:00 :修复了图形化界面删除图片的bug(最后一张的情况)，修改了一些交互

main5.5-20:20 :添加了进度条显示切题的进度（采用多线程并行）

main5.6-22:00 :添加了预处理的按钮(包括其进度条)，在切题前可先进行预处理(添加了双页试卷分割处理部成两张的部分),优化了对于完型填空的识别策略

main5.9-15:10 :解决了文字未识别完全导致的题目范围不完整的错误（使用下一题的位置辅助矫正上一题的位置）；的，解决了预处理（双页试卷分割处理部分）中的bug
目前尚未完成：
1.预处理的畸变矫正和倾斜矫正部分（测试通过后整合到主程序中）
2.少数不符合规则的试卷的切题策略待优化 
3.windows端界面等的适配
4.捕捉不符合常规思路的bug＋打上注释
5.拍摄视频并剪辑
6.ppt（预处理部分，自然语言处理部分，其他部分的修改＋美化）


