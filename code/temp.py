# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#import cv2
from aip import AipOcr

""" 你的 APPID AK SK """

'''
APP_ID = '16014492'
API_KEY = 'LCg6tBRLl08bq7GBXedTw2Ft'
SECRET_KEY = 'kGdGzrXhCFaYGDwjGIoXm7OCaMob22gW'


APP_ID = '15776520'
API_KEY = 'O8xYdXlWnIkHn5DzVXc1l1Ey'
SECRET_KEY = 'fIAyoLQTzXowpvmDrcHKMGiK55AhsQaQ'

'''
APP_ID = '15899380'
API_KEY = '1QKo2wth8n6iUNBXmTIwA8rr'
SECRET_KEY = 'Ax9SNpQdAqq7XR52PELiNI88i8M92UpC'
'''
APP_ID = '16228251'
API_KEY = 'ZY9MufeEF66oOZooSdsUMgMK'
SECRET_KEY = 'B4HeWjCUVzOCmkzfXlk6ruf67rSDZdba'
'''

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

#image = get_file_content('/Users/tt/Desktop/timg.jpg')


""" 如果有可选参数 """
options = {}
options["language_type"] = "CHN_ENG"
options["detect_direction"] = "true"


""" 带参数调用通用文字识别, 图片参数为本地图片 """
'''results =client.basicGeneral(image, options)
for result in results['words_result']:
    print(result['words'])'''
""" 带参数调用高精度文字识别, 图片参数为本地图片 """


'''
    调用百度API的高精度文字识别的函数
    return ：识别出的文字、文字的位置的字典的集合
    author ：tt
'''
def accurate_ocr(filepath):
    image = get_file_content(filepath)
    results=client.accurate(image);
    #print(results)
    #print(len(results['words_result']))
    #for result in results['words_result']:
        #print(result['words'])
        #print(result['location'])
    return results


'''
    调用百度API的普通精度文字识别的函数
    return ：识别出的文字、文字的位置的字典的集合
    author ：tt
'''
def general_ocr(filepath):
    image = get_file_content(filepath)
    results=client.general(image);
    return results
#accurate_ocr('/Users/tt/Desktop/timg.jpg')
    

