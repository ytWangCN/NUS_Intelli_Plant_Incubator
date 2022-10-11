void buttonFan_callback(const String & state)
{
    BLINKER_LOG("Show state: ", state);//在com端打印
    
    int sta=!digitalRead(D8);
    digitalWrite(D8, sta); 
    if(sta==1)
         analogWrite(MotorPin,2400);
    else 
         analogWrite(MotorPin,0);
}
void Fansetup()
{
    pinMode(MotorPin,OUTPUT);; 
    // 初始化有LED的IO
    digitalWrite(MotorPin, HIGH);
  
    ButtonFan.attach(buttonFan_callback);
}
