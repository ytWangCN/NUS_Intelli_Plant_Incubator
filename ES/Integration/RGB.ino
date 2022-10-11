void setColor(int redValue, int greenValue, int blueValue) {
  analogWrite(redPin, redValue);
  analogWrite(greenPin, greenValue);
  analogWrite(bluePin, blueValue);
}
void buttonRGB_callback(const String & state)
{
    BLINKER_LOG("Show state: ", state);//在com端打印
    int sta=!digitalRead(D0);
    digitalWrite(D0, sta);
      if(counter%4==0)
        setColor(255, 0,0); // Red Color 
       
      else if(counter%4==1)
         setColor(0, 255,0); // Green Color    
      else if(counter%4==2)
         setColor(0,0,255);  //blue color
      else 
          setColor(255, 255, 255); // 不亮
     
      //Blinker.vibrate(); 
      //Blinker.print("you have received a message");
    
    counter++;
     Number1.print(counter);
}
void dataRead(const String & data)
{
    BLINKER_LOG("Blinker readString: ", data);
    counter++;
    Number1.print(counter);
}
void RGBsetup()
{    
    pinMode(redPin, OUTPUT);
    pinMode(greenPin, OUTPUT);
    pinMode(bluePin, OUTPUT);
    
//    BLINKER_DEBUG.stream(Serial);
//    BLINKER_DEBUG.debugAll();
//    
//    // 初始化有LED的IO
//    pinMode(D1, OUTPUT);
//    digitalWrite(D1, HIGH);
    // 初始化blinker
   
    Blinker.attachData(dataRead);
    ButtonRGB.attach(buttonRGB_callback);
}
