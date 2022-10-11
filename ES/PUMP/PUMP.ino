#define BLINKER_WIFI
#include <Blinker.h>
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

int sensorPin = A0;    // 设置模拟口A0为信号输入端    // 设置LED控制引脚为13
int sensorValue = 0;



ESP8266WiFiMulti WiFiMulti;
char auth[] = "a17f7c7955cf";
char ssid[] = "MY HotSpot";
char pswd[] = "&2g4079S";
// 新建组件对象
//BlinkerButton Button1("btn-pump");

BlinkerButton Button2("btn-pump");//实质是message
BlinkerNumber num("soil");
BlinkerText tex("tex-dmu");
BlinkerText te("tex-k81");
float val;

int RelayPin =D5; //定义数字接口8 
String payload;
//// 按下按键即会执行该函数
////这个是给水泵的
//void button1_callback(const String & state)
//{
//      BLINKER_LOG("Show state: ", state);//在com端打印
//      digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));  
//      digitalWrite(RelayPin,!digitalRead(RelayPin));
//}

void setup()
{
//    // 初始化串口
//    Serial.begin(115200);
//    BLINKER_DEBUG.stream(Serial);
//    BLINKER_DEBUG.debugAll();
//    
//    Blinker.begin(auth, ssid, pswd);
//
////    Button1.attach(button1_callback);
////   
//    // 初始化有LED的IO,这些都是水泵用的
    pinMode(RelayPin, OUTPUT);
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, HIGH);
    digitalWrite(RelayPin, LOW);
  
      // 初始化串口
    Serial.begin(115200);
    BLINKER_DEBUG.stream(Serial);
    BLINKER_DEBUG.debugAll();
    
    // 初始化有LED的IO
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, HIGH);
    // 初始化blinker
    Blinker.begin(auth, ssid, pswd);

    Button2.attach(button2_callback);
    
    WiFi.mode(WIFI_STA);
    WiFiMulti.addAP("MY HotSpot", "&2g4079S");
}

void loop() {
    Blinker.run();//有可能是必须先run这个，不然网络容易断，谁知道
    float v=getSoil();
   if(v<0.3){
     digitalWrite(RelayPin,HIGH);
     delay(1500);
     digitalWrite(RelayPin,LOW);
   }
    num.print(v);
    delay(1000);
}
