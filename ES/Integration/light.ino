int getLight() {
  int lightLevel;
  lightLevel = analogRead(LDR_PIN); 
  Serial.print("lightLevel=");
  Serial.println(lightLevel); 
  return lightLevel ;
}
