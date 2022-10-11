float getSoil() {
  sensorValue = analogRead(sensorPin);
  val=256.0/131 - (float)sensorValue / 524;
  Serial.print("sensorValue:");
  Serial.println(sensorValue);
  Serial.print("val:");
  Serial.print(val);
  if(val>1)
    val=1.00;

  Serial.print("sensorValue:");
  Serial.println(sensorValue);
  Serial.print("val:");
  Serial.print(val);
   // lastTime = millis();  
  return val;
}
