'''
描述：病虫害检测的端的代码
1、getImage从云端获取实时图片
2、sendPrediction将预测结果上传到云端
'''
import csv

import requests
import json
from PIL import Image # Pillow library
from base64 import b64decode


# 我的url每一次开机重启都不一样，我每一次更新都会发的
url = r'http://127.0.0.1:3001'

# 增加用户名和密码,第一次启动需要运行，将你的用户名和密码添加到数据库，后续记住即可
def addUser(userId,password):
    headers = {"Content-type": "application/json"}
    data = {"userid": userId, "password":password}
    req = requests.post(url + "/adduser", headers=headers, data=json.dumps(data))
    print("Status code: ", req.status_code, " Details: ", req.text)

# 获取云端的数据，一次获取50组，进行最新预测
def getData(userId,password):

    # 增加用户名和密码
    headers = {"Content-type": "application/json"}
    data = {"userid": userId, "password": password}
    req = requests.post(url + "/getData", headers=headers, data=json.dumps(data))

    # 将返回的数据进行解码处理
    data = req.text
    data = data.splt('&&')
    result = []
    for i in data:
        item = json.loads(i)
        item['humid'] = int(item['humid'])
        item['temp'] = int(item['temp'])
        item['light'] = int(item['light'])
        result.append(item)

    # 将字典进行保存
    headers = ['time','humid','temp','light']
    with open('sensorData.csv','a', newline='',encoding='utf-8') as f:
        writer = csv.DictWriter(f,fieldnames=headers)
        writer.writeheader()
        writer.writerows(result)

    print('已经下载最新的50条数据,文件名为sensorData.csv')

# 将预测结果发送给cloudserver
def sendPrediction(userId,password,prediction):

    # 增加用户名和密码
    headers = {"Content-type": "application/json"}
    data = {"userid": userId, "password": password,'prediction':prediction}
    req = requests.post(url + "/sendData", headers=headers, data=json.dumps(data))
    print(req)

if __name__ == '__main__':
    # 首先需要重新设定url
    # 第一次运行要添加用户的id和密码，先运行addUser函数
    userId = 'jiawei'
    password = '123456'
    # addUser(userId,password)
    getData(userId,password)












