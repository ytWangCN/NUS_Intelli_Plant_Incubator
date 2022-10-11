'''
描述：ES端的代码
1、上传数据到云端的mongodb中
2、获取故障检测的预测结果
4、上传图片到云端
'''
import requests
import json
from PIL import Image # Pillow library
from base64 import b64decode, b64encode

# 我的url每一次开机重启都不一样，我每一次更新都会发的
url = r'http://127.0.0.1:3001'

# 增加用户名和密码,第一次启动需要运行，将你的用户名和密码添加到数据库，后续记住即可
def addUser(userId,password):
    headers = {"Content-type": "application/json"}
    data = {"userid": userId, "password":password}
    req = requests.post(url + "/adduser", headers=headers, data=json.dumps(data))
    print("Status code: ", req.status_code, " Details: ", req.text)

# 上传图片到云端
def sendImage(userId,password,jpg_name):

    # 增加用户名和密码
    headers = {"Content-type": "application/json"}

    # 打开图片并统一大小，同时进行转码
    image = Image.open(jpg_name)
    image = image.resize((800, 600))
    img_bytes = image.tobytes()
    img_b64 = b64encode(img_bytes).decode('utf-8')

    # 将数据保存到
    data = {"userid": userId, "password": password,'data':img_b64}
    req = requests.post(url + "/sendImage", headers=headers, data=json.dumps(data))

    return req.text, req.status_code

# 从云端拉取预测结果
def getPrediction(userId,password,prediction):

    # 增加用户名和密码
    headers = {"Content-type": "application/json"}
    data = {"userid": userId, "password": password}
    req = requests.post(url + "/getPredict", headers=headers, data=json.dumps(data))
    return req.text,req.status_code

# 上传数据到云端
def pushData(humid,temp,soidHumid,light):
    '''
    上传空气湿度、温度和土壤湿度到云端数据
    '''
    headers = {"Content-type": "application/json"}
    data = {"userid": userId, "password": password,'light':light,'humid':humid,'temp':temp,'soilHumid':soidHumid}
    req = requests.post(url + "/getPredict", headers=headers, data=json.dumps(data))
    return req.text,req.status_code

if __name__ == '__main__':
    # 首先需要重新设定url
    # 第一次运行要添加用户的id和密码，先运行addUser函数
    userId = 'yongxin'
    password = '123456'
    # addUser(userId,password)










