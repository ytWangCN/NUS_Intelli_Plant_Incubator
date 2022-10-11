//温湿度模块
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#define DHTPIN D6     
#define DHTTYPE    DHT11     // DHT 11
DHT_Unified dht(DHTPIN, DHTTYPE);
uint32_t delayMS;

//光模块
#define LDR_PIN A0 

//接受另一块板子的土壤湿度
#include <ESP8266WiFi.h>

//网络模块
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
const char* ssid = "MY HotSpot"; //Your Wifi's SSID  电脑热点
const char* password = "&2g4079S"; //Wifi Password   电脑热点
//const char* piAt = "http://566d91a0.cpolar.cn/";  
const char* piAt = "http://2ee535c2.r2.cpolar.cn/"; 
WiFiClient wifiClient;


//RGB按钮灯模块
#define BLINKER_WIFI
#include <Blinker.h>

char auth[] = "3be9c13dabe8";
char Bssid[] = "MY HotSpot";
char pswd[] = "&2g4079S";
int redPin= D5;
int greenPin = D4;
int bluePin = D3;
// 新建组件对象
BlinkerButton ButtonRGB("btn-RGB");
BlinkerButton ButtonFan("btn-fan");
BlinkerButton ButtonWindow("btn-window");
BlinkerNumber Number1("num-counter");
BlinkerNumber tempe("num-temperature");
BlinkerNumber hum("num-humidity");
BlinkerNumber lig("num-light");
//BlinkerNumber soi("soil");
int counter = 0;

//窗户模块
#include <Servo.h>
#define PIN_SERVO D1
Servo myservo;

//风扇模块
#define MotorPin D8

//温度上传时间间隔
volatile unsigned long lastTime = 0;  
volatile unsigned long timedelay = 600000; 
void setup(){
  Serial.begin(115200);
  //receiveSetup();
 // myservo.attach(D1);
  WiFi.begin(ssid, password);
  Serial.println("");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
//  
  DHTsetup();

 
  
  //WIFI模块地方改成函数连接不稳定不知道为什么

  //以下是按钮的setup
   BLINKER_DEBUG.stream(Serial);
    BLINKER_DEBUG.debugAll();
     Blinker.begin(auth, Bssid, pswd);
  RGBsetup();
  Fansetup();
  Windowsetup();
}
void loop(){
  Blinker.run();
  sensors_event_t event;
  float tem=getTemperature(event);
  float humid=getHumidity(event);
  int lightLevel=getLight();
  

  tempe.print(tem);
  hum.print(humid);
  lig.print(lightLevel);
if(millis()-lastTime>timedelay){
  if (WiFi.status() == WL_CONNECTED){
    HTTPClient http;
    
    String url = piAt;
    url += "data?temp=";
    url+=tem;
    
    url+="&humid=";
    url+=humid;
    
    url+="&light=";
    url+=lightLevel;
       
    http.begin(wifiClient,url);
    int returnCode = http.GET();   //perform a HTTP GET request
    
    if (returnCode > 0){
      String payload = http.getString();
      Serial.println(payload);
    }
    http.end();
    
  } else {
    Serial.println("WiFi disconnected");
  }

  lastTime=millis();
}
  //WindowOn();
//  Serial.println("this is servo");
//  myservo.write(180);
//  delay(2000);  //30 seconds delay to satisfy the Cloud DB 's uploading rules
//  //WindowOff();
//   myservo.write(45);
//   delay(2000);

  delay(1000);
}
