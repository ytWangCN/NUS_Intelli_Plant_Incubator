//
////设置土壤湿度传感器的针脚
//#define PIN_AO A0
//#define PIN_DO D0
//
///*
// * 土壤湿度传感器的setup程序
// * 注意有两种模式，一种是数字模式和模拟模式，推荐使用模拟模式
// */
//void SoilHumidSetup(){
//  pinMode(PIN_AO, INPUT);
//  pinMode(PIN_DO, INPUT);  
//}
//
///*
// * LCD的设置函数 
// * 描述：包括初始化屏幕，并打开低光
// */
//void LCDsetup(){
//  lcd.init();
//  lcd.backlight();
//  lcd.setCursor(2, 0);
//  lcd.print("Intelligent");
//  lcd.setCursor(3, 1);      
//  lcd.print("incubator");
//}
//
///*
// * 描述：返回泥土湿度的模拟量，从1到1024
// * 注意：这里只需要接三根线，对于数字信号D0并不需要接线
// */
//int getSoilHumid(){
//  return analogRead(PIN_A0);
//}
//
///* 
// * 实时显示培育箱的状态
// * 描述：显示空气温度（AT：32℃）、空气湿度（AH：21%）、土壤湿度（SH：32%）、植物健康状态（State：H/U）
// * 注意：需要进行循环调用显示
// * 参数：AirTemp（空气湿度），AirHumid（空气湿度），SoilHumid（土壤湿度），State
// * 
// * 
// */
//void LCDShow(int AirTemp,int AirHumid,int SoilHumid,int State){
//  lcd.setCursor(0,0);
//  lcd.print("AT:"+String(AirTemp)+"C   ");
//  lcd.print("AH:"+String(AirHumid)+"%");
//  lcd.setCursor(0,1);
//  if(State == 1){
//    lcd.print("State:H  ");
//  }else{
//    lcd.print("State:U  ");
//  }
//  lcd.print("SH:"+String(SoilHumid)+"%");
//}
