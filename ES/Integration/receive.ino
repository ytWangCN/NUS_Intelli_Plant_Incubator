//void OnDataRecv(uint8_t * mac, uint8_t *incomingData, uint8_t len) {
//  memcpy(&myData, incomingData, sizeof(myData));
//  Serial.print("SoilHumidity received ");
//  Serial.println(myData.SoilHumidity);
//}
//void receiveSetup(){
//  WiFi.mode(WIFI_STA);
//  if (esp_now_init() != 0) {
//    Serial.println("Error initializing ESP-NOW");
//    return;
//  }
//  esp_now_set_self_role(ESP_NOW_ROLE_SLAVE);
//  esp_now_register_recv_cb(OnDataRecv);
//
//}
