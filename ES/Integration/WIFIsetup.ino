void WIFIsetup(){
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

}
void getURL(float tem,float humid,int lightlevel,float soil){
 if (WiFi.status() == WL_CONNECTED){
    HTTPClient http;
    
    String url = piAt;
    url += "data?temp=";
    url+=tem;
    
    url+="&humid=";
    url+=humid;
    
    url+="&light=";
    url+=lightlevel;
    
    url+="&SoilHumidity=";
    url+=soil;
       
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
   
  
  delay(1000);  //30 seconds delay to satisfy the Cloud DB 's uploading rules
}
