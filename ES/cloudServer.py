import json

from flask import Flask,request,Response,send_file
from hashlib import sha512
from pymongo import MongoClient
from PIL import Image
from base64 import b64encode, b64decode
import datetime
# 声明对应应用类别
from requests import Response

app = Flask(__name__)

# 创建mongodb客户端
client = MongoClient("mongodb://127.0.0.1:27017")
# 创建对应数据库
mydb = client['SoilSensorData']
# 指定对应集合表
users = mydb['user']
sensor_data_collection = mydb['sensorData']
sensor_data_collection1 = mydb['sensorData1']

# 用于客户验证
def finduser(userid):
    return users.find_one({"userid":userid})

# 用于密码验证
USER_OK = 0
USER_NOT_EXIST = 1
USER_BAD_PASSWORD = 2

# 安全验证的函数
def secure_check(data):
    # 检查用户名和密码
    if 'userid' not in data or 'password' not in data or 'image' not in data:
        return "Must provide userid, password and image data.", 400

    # 检查密码和账户是否存在
    res = check_pw(data['userid'], data['password'])
    if res == USER_NOT_EXIST:
        return "User does not exist.", 400
    if res == USER_BAD_PASSWORD:
        return "Incorrect password", 400

# 检查密码
def check_pw(userid, passwd):
    # 检查用户是否存在
    user_data = finduser(userid)

    if user_data is None:
        # 用户不存在
        return USER_NOT_EXIST

    # 用户存在检查密码
    pw = sha512(passwd.encode('utf-8')).hexdigest()

    if pw == user_data["password"]:
        return USER_OK
    else:
        return USER_BAD_PASSWORD

# 主页提示信息
@app.route('/',methods = ['GET','POST'])
def index():
    # Let's see if a name is provided
    name = request.args.get('name')

    # Return back a text message and a result code of 200, which means success.
    if name is not None:
        return "this is sws3009 group 2 temporary server!Hello " + name, 200
    else:
        return "this is sws3009 group 2 temporary server!Hello whoever you are.", 200

# 增加用户
@app.route("/adduser", methods=["POST"])
def newuser():
    # We can get the data POSTED to us using request.get_json()
    try:
        user_data = request.get_json()

        # 确保在useradd中制定了用户名和密码
        if "userid" not in user_data or "password" not in user_data:
            return "Must specify userid and password", 400

        # 如果用户存在，返回异常
        if finduser(user_data["userid"]) is not None:
            return "User " + user_data["userid"] + " exists.", 400
        else:
            # 不可直接将用户信息写入到数据库中，防止sql注入攻击
            pw = sha512(user_data["password"].encode('utf-8')).hexdigest()
            users.insert_one({"userid": user_data["userid"], "password": pw})

        return "OK", 200

    except Exception as e:
        return "Error inserting record: " + str(e), 500

'''
下述为ES端的访问网页，功能包括
1、getPredict获取dl的预测结果
2、sendPicture上传图片
3、sendData上传传感器数据
'''
# 获取预测结果
@app.route('/getPredict',methods = ['GET','POST'])
def send_predict():
    try:
        with open('water.txt','r') as tf:
            water = tf.read()
        with open('disease.txt','r') as tf:
            disease = tf.read()
        result = disease + ' '+ water
        return result,200
    except Exception as e:
        return "Error processing request." + str(e), 500

@app.route('/getPredict1',methods = ['GET','POST'])
def send_predict1():
    try:
        # with open('water1.txt','r') as tf:
        #     water = tf.read()
        with open('disease1.txt','r') as tf:
            disease = tf.read()
        result = disease
        return result,200
    except Exception as e:
        return "Error processing request." + str(e), 500

# 上传图片到云端
@app.route('/sendImage',methods = ['GET','POST'])
def send_image():
    try:
        # 获取数据
        data = request.get_json()
        secure_check(data)
        # 获取图片编码
        img_b64 = data['data']
        img_data = b64decode(img_b64)
        img = Image.frombytes("RGB", (800, 600), img_data)
        # 保存图片
        img.save(r'photo.jpg')
        print('成功获取图片并保存')
        return 'accept the image',200

    except Exception as e:
        return "Error processing request." + str(e), 500

@app.route('/sendImage1',methods = ['GET','POST'])
def send_image1():
    try:
        # 获取数据
        data = request.get_json()
        secure_check(data)
        # 获取图片编码
        img_b64 = data['data']
        img_data = b64decode(img_b64)
        img = Image.frombytes("RGB", (800, 600), img_data)
        # 保存图片
        img.save(r'photo1.jpg')
        print('成功获取图片并保存')
        return 'accept the image',200

    except Exception as e:
        return "Error processing request." + str(e), 500

# 上传检测数据到云端，需要调用mongodb进行保存
@app.route('/data',methods = ['GET','POST'])
def send_sensor_data():
    try:
        # 获取数据
        # data = request.get_json()
        # print(request)
        # print(data)
        # secure_check(data)
        # 获取图片编码
        time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        humid = request.args.get('humid')
        temp = request.args.get('temp')
        # soilHumid = data['soilHumid']
        light = request.args.get('light')

        sensordata = {
            'time':time,
            'humid':humid,
            'temp':temp,
            # 'soilHumid':soilHumid,
            'light':light
        }

        # 打开mongodb并将当前这条数据保存其中
        sensor_data_collection.insert_one(sensordata)
        return "  accept data",200

    except Exception as e:
        return "Error processing request." + str(e),500

@app.route('/data1',methods = ['GET','POST'])
def send_sensor_data1():
    try:
        # 获取数据
        # 获取图片编码
        time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        humid = request.args.get('humid')
        temp = request.args.get('temp')
        # soilHumid = data['soilHumid']
        # light = request.args.get('light')

        sensordata = {
            'time':time,
            'humid':humid,
            'temp':temp,
            # 'soilHumid':soilHumid,
            # 'light':light
        }
        # 温湿度控制
        # 打开mongodb并将当前这条数据保存其中
        with open("a.json", "w") as f:
            f.write(json.dumps(sensordata, ensure_ascii=False, indent=4, separators=(',', ':')))
        return 'accept data',200

    except Exception as e:
        return "Error processing request." + str(e),500

# 水培箱的控制程序
@app.route('/water',methods = ['GET','POST'])
def water1():
    # 控制浇水，根据温度和湿度进行联和控制温湿度
    # try:
        with open("a.json", "r") as f:
            load_dict = json.load(f)
        humid =load_dict['humid']
        print("获取浇水结果",humid)
        if int(humid) < 80:
            return 'Y', 200
        else:
            return 'N',200

    # except Exception as e:
    #     return "Error processing request." + str(e), 500

'''
下述为DL端访问的网页，功能包括
1、getImage：获取ES端上传的图片
2、sendPredictDisease：发送病虫害检测数据
3、getData：获取ES端上传的传感器数据
4、sendData:发送ES传感器端的数据
'''
# 获取DL的病虫害预测结果
@app.route('/sendPrediction',methods = ['GET','POST'])
def receive_predict_disease():
    try:
        # 获取数据
        data = request.get_json()
        secure_check(data)

        # 处理用户的具体需求
        diseaseStr = data['disease']
        print('record the disease ',diseaseStr)
        with open('disease.txt','w') as tf:
            tf.write(diseaseStr)

        return 'accept prediction',200

    except Exception as e:
        return "Error processing request." + str(e), 500

@app.route('/sendPrediction1',methods = ['GET','POST'])
def receive_predict_disease1():
    try:
        # 获取数据
        data = request.get_json()
        secure_check(data)

        # 处理用户的具体需求
        diseaseStr = data['disease']
        print('record the disease ',diseaseStr)
        with open('disease1.txt','w') as tf:
            tf.write(diseaseStr)

        return 'accept prediction',200

    except Exception as e:
        return "Error processing request." + str(e), 500

# 获取服务器端的图片数据,将之发送到DL的计算机
@app.route('/getImage',methods = ['GET','POST'])
def get_Image():

    try:
        # 获取数据
        data = request.get_json()
        secure_check(data)

        # 对图片进行编码
        image = Image.open(r'photo.jpg')
        image = image.resize((800,600))
        # image.show()
        img_bytes = image.tobytes()
        img_b64 = b64encode(img_bytes).decode('utf-8')

        return img_b64

    except Exception as e:
         return "Error processing request." + str(e), 500

@app.route('/getImage1',methods = ['GET','POST'])
def get_Image1():

    try:
        # 获取数据
        data = request.get_json()
        secure_check(data)

        # 对图片进行编码
        image = Image.open(r'photo1.jpg')
        image = image.resize((800,600))
        # image.show()
        img_bytes = image.tobytes()
        img_b64 = b64encode(img_bytes).decode('utf-8')

        return img_b64

    except Exception as e:
         return "Error processing request." + str(e), 500

# 获取服务器端保存的传感器的数据
@app.route('/getData',methods = ['GET','POST'])
def get_data():
    try:
        # 获取数据
        data = request.get_json()
        secure_check(data)
        data = sensor_data_collection.find().limit(50)
        result = list()
        for i in data:
                temp = {'time':i['time'],
                        'humid':i['humid'],
                        'temp':i['temp'],
                        'light':i['light']}
                result.append(json.dumps(temp))
        result = '&&'.join(result)
        print(type(result))
        return result

    except Exception as e:
         return "Error processing request." + str(e), 500

@app.route('/getData1',methods = ['GET','POST'])
def get_data1():
    try:
        # 获取数据
        data = request.get_json()
        secure_check(data)
        data = sensor_data_collection1.find().limit(50)
        result = list()
        for i in data:
                temp = {'time':i['time'],
                        'humid':i['humid'],
                        'temp':i['temp'],
                        'light':i['light']}
                result.append(json.dumps(temp))
        result = '&&'.join(result)
        print('将传感器数据保存为csv文件')
        return result

    except Exception as e:
         return "Error processing request." + str(e), 500

# 获取DL的某一项的预测结果
@app.route('/sendData',methods = ['GET','POST'])
def send_data():
    try:
        # 获取数据
        data = request.get_json()
        secure_check(data)

        # 处理用户的具体需求
        waterStr = data['prediction']
        print('record the water ', waterStr )
        with open('water.txt', 'w') as tf:
            tf.write(waterStr)

        return 'accept prediction'

    except Exception as e:
        return "Error processing request." + str(e), 500

@app.route('/sendData1',methods = ['GET','POST'])
def send_data1():
    try:
        # 获取数据
        data = request.get_json()
        secure_check(data)

        # 处理用户的具体需求
        waterStr = data['prediction']
        print('record the water ', waterStr )
        with open('water1.txt', 'w') as tf:
            tf.write(waterStr)

        return 'accept prediction'

    except Exception as e:
        return "Error processing request." + str(e), 500

if __name__ == '__main__':
    # 设置为所有ip都可以访问
    app.run(host = '0.0.0.0',port =3001,debug=True)
