'''
描述：病虫害检测的端的代码
1、getImage从云端获取实时图片
2、sendPrediction将预测结果上传到云端
'''
import os
import time
import lstm_load
import requests
import json
from PIL import Image # Pillow library
from base64 import b64decode
import predict
import csv

# 我的url每一次开机重启都不一样，我每一次更新都会发的
url = 'http://5cf838a7.cpolar.cn/'

# 增加用户名和密码,第一次启动需要运行，将你的用户名和密码添加到数据库，后续记住即可
def addUser(userId,password):
    headers = {"Content-type": "application/json"}
    data = {"userid": userId, "password":password}
    req = requests.post(url + "/adduser", headers=headers, data=json.dumps(data))
    print("Status code: ", req.status_code, " Details: ", req.text)

# 获取云端的图片
def getImage(userId,password,jpg_name):
    # 增加用户名和密码
    headers = {"Content-type": "application/json"}
    data = {"userid": userId, "password": password}
    req = requests.post(url + "/getImage", headers=headers, data=json.dumps(data))
    # 将返回的数据进行解码处理
    img_b64 = req.text
    img_data = b64decode(img_b64)
    img = Image.frombytes("RGB", (800, 600), img_data)
    # 这个图片可以直接保存
    img.save('D:/'+jpg_name+'.jpg')
    print('成功保存图片为',jpg_name)
    return 'D:/'+jpg_name+'.jpg'

def getImage1(userId,password,jpg_name):
    # 增加用户名和密码
    headers = {"Content-type": "application/json"}
    data = {"userid": userId, "password": password}
    req = requests.post(url + "/getImage1", headers=headers, data=json.dumps(data))
    # 将返回的数据进行解码处理
    img_b64 = req.text
    img_data = b64decode(img_b64)
    img = Image.frombytes("RGB", (800, 600), img_data)
    # 这个图片可以直接保存
    img.save('D:/'+jpg_name+'.jpg')
    print('成功保存图片为',jpg_name)
    return 'D:/'+jpg_name+'.jpg'

def getData(userId,password):

    # 增加用户名和密码
    headers = {"Content-type": "application/json"}
    data = {"userid": userId, "password": password}
    req = requests.post(url + "/getData", headers=headers, data=json.dumps(data))

    # 将返回的数据进行解码处理
    data = req.text
    data = data.split('&&')
    result = []
    for i in data:
        item = json.loads(i)
        print(item['temp'])
        item['temp'] = (float(item['temp']) + 25)/70
        item['humid'] = (float(item['humid']) + 25)/70
        item['light'] = (float(item['light']) + 25)/70
        result.append(item)

    # 将字典进行保存
    headers = ['time','temp','humid','light']
    os.remove("D:/sensorData.csv")
    with open('D:/sensorData.csv','a', newline='',encoding='utf-8') as f:

        writer = csv.DictWriter(f,fieldnames=headers)
        writer.writeheader()
        writer.writerows(result)

    print('已经下载最新的50条数据,文件名为sensorData.csv')

# 将预测结果发送给cloudserver
def sendPrediction(userId,password,prediction):

    # 增加用户名和密码
    headers = {"Content-type": "application/json"}
    data = {"userid": userId, "password": password,'disease':prediction}
    req = requests.post(url + "/sendPrediction", headers=headers, data=json.dumps(data))
    print(req)

def sendPrediction1(userId,password,prediction):

    # 增加用户名和密码
    headers = {"Content-type": "application/json"}
    data = {"userid": userId, "password": password,'disease':prediction}
    req = requests.post(url + "/sendPrediction1", headers=headers, data=json.dumps(data))
    print(req)

def sendPrediction2(userId,password,prediction):

    # 增加用户名和密码
    headers = {"Content-type": "application/json"}
    data = {"userid": userId, "password": password,'prediction':prediction}
    req = requests.post(url + "/sendData", headers=headers, data=json.dumps(data))
    print(req)

if __name__ == '__main__':
    # 首先需要重新设定url

    userId = 'echoloe'
    password = '123456'
    #addUser(userId,password)
    # addUser(userId,password)
    # getImage(userId,password,'sentPhoto.jpg')
    while 1:
         # file_path=getImage(userId, password, 'plant')
         # result = predict.PredictResult(file_path)
         file_path1 = getImage1(userId, password, 'plant1')
         result1 = predict.PredictResult(file_path1)
         getData(userId,password)
         prediction=lstm_load.lstm()
         # sendPrediction(userId, password, result)
         # sendPrediction1(userId,password,result1)
         # sendPrediction2(userId, password, prediction)
         sendPrediction(userId, password, 'tomato_healthy')
         sendPrediction1(userId,password, 'orange_rust')
         sendPrediction2(userId, password, prediction)
         time.sleep(15)











