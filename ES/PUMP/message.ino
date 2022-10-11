String getString() {
  if ((WiFiMulti.run() == WL_CONNECTED)) {
    WiFiClient client;
    HTTPClient http;
    Serial.print("[HTTP] begin...\n");
    //这里不能写https，要写http
    if (http.begin(client, "http://7a9a5aa.r2.cpolar.cn/getPredict")) {  // HTTP


      Serial.print("[HTTP] GET...\n");
      int httpCode = http.GET();

        Serial.printf("[HTTP] GET... code: %d\n", httpCode);

        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
           payload = http.getString();
          Serial.print("预测结果是");
          Serial.println(payload);
        }
        http.end();
      }
    } 
     delay(2000);
     Serial.print("返回前的字符串是:");
     Serial.print(payload);
     return payload;
}
void button2_callback(const String & state)
{
    BLINKER_LOG("Show state: ", state);//在com端打印   
    String s=getString();
    Serial.print("s是这个：");
    Serial.println(s);
    Blinker.println("The diagnose result is :",s);
    //tex.print("The diagnose result is :");
    //te.print(s);
}
void messageSetup(){
  Button2.attach(button2_callback);
  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP("MY HotSpot", "&2g4079S");
}
