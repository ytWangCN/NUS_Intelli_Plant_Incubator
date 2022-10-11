'''
描述：病虫害检测的端的代码
1、getImage从云端获取实时图片
2、sendPrediction将预测结果上传到云端
'''
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
    img.save(jpg_name)
    print('成功保存图片为',jpg_name)

# 将预测结果发送给cloudserver
def sendPrediction(userId,password,prediction):

    # 增加用户名和密码
    headers = {"Content-type": "application/json"}
    data = {"userid": userId, "password": password,'disease':prediction}
    req = requests.post(url + "/sendPrediction", headers=headers, data=json.dumps(data))
    print(req)

if __name__ == '__main__':
    # 首先需要重新设定url
    userId = '111'
    password = '123456'
    addUser(userId,password)

    # getImage(userId,password,'sentPhoto.jpg')
    # sendPrediction(userId,password,'rust')











