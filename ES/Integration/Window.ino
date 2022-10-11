void buttonWindow_callback(const String & state)
{
    BLINKER_LOG("Show state: ", state);//在com端打印
    
    int sta=!digitalRead(D2);
    
    digitalWrite(D2, sta);  
    if(sta==1)
        myservo.write(180);
    else
        myservo.write(45);
      
      //Blinker.vibrate(); 
      //Blinker.print("you have received a message");

}

//D2是辅助信号口   D1是舵机信号源
void Windowsetup()
{   myservo.attach(D1);    
    pinMode(D2, OUTPUT);
    digitalWrite(D2, HIGH);
    ButtonWindow.attach(buttonWindow_callback);
}
