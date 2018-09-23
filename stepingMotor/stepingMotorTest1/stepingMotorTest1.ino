#include <SPI.h> //SPI通信の読み込み
#define PIN_SPI_MOSI 11
#define PIN_SPI_MISO 12
#define PIN_SPI_SCK 13
#define PIN_SPI_SS 10
#define PIN_BUSY 9
void setup() {
  delay(1000);
  Serial.begin(115200);
  
  //ステッピングモータ用のピンの準備
  pinMode(PIN_SPI_MOSI, OUTPUT);
  pinMode(PIN_SPI_MISO, INPUT);
  pinMode(PIN_SPI_SCK, OUTPUT);
  pinMode(PIN_SPI_SS, OUTPUT);
  digitalWrite(PIN_SPI_SS, HIGH);
  pinMode(PIN_BUSY, INPUT);

   //SPI通信の開始宣言
   SPI.begin();
   SPI.setDataMode(SPI_MODE3); //SCKの立ち上がりでデータを送受信、アイドル時はpinをHIGHに設定
   SPI.setBitOrder(MSBFIRST); //MSBから送信
   //L6470の利用設定
   L6470_setup();
}

//SPI通信するための関数

void L6470_send(unsigned char value){
  while(!digitalRead(PIN_BUSY)){}
  //BUSYが解除されるまで待機

  digitalWrite(PIN_SPI_SS, LOW);
  SPI.transfer(0); //制御信号をSPI通信で送る
  SPI.transfer(value); //制御信号をSPI通信で送る
  digitalWrite(PIN_SPI_SS, HIGH);
}

//L6470のセットアップ

void L6470_setup(){
  //デバイス設定
  L6470_send(0x00);
  L6470_send(0x00);
  L6470_send(0x00);
  L6470_send(0x00);
  L6470_send(0xc0);

  //加速係数設定
  L6470_send(0x05);
  L6470_send(0x00);
  L6470_send(0x41);
  //減速係数設定
  L6470_send(0x06); //レジスタアドレス
  L6470_send(0x00);
  L6470_send(0x41); //値(10bit)、デフォルト0x41
  //最大回転速度設定
  L6470_send(0x07);
  L6470_send(0x00);
  L6470_send(0x41);
  //最低回転速度設定
  L6470_send(0x08);
  L6470_send(0x00);
  L6470_send(0x01);
  //モータ停止中の電圧設定
  L6470_send(0x09); //レジスタアドレス
  L6470_send(0x20); //値(8bit),デフォルト0x29
  //フルステップ駆動
  L6470_send(0x15);
  L6470_send(0x00);
  L6470_send(0x3ff); //値(10bit),デフォルト0x41

  //モータ定速回転時の電圧設定
  L6470_send(0x0A);
  L6470_send(0x20); //値(8bit),デフォルト0x29
  //加速中の電圧設定
  L6470_send(0x0B);
  L6470_send(0x20); //値(8bit),デフォルト0x29
  //減速中の電圧設定
  L6470_send(0x0C);
  L6470_send(0x20); //値(8bit),デフォルト0x29
  //フルステップ、ハーフステップ、1/4,1/8,・・・,1/128ステップの設定
  L6470_send(0x16);
  L6470_send(0x03); ////値(8bit)
}

//メイン処理-loop()
void loop() {
  //360°回転させる
  L6470_send(0x51); //Run(DIR, SPD),0x51:正転,0x50:逆転
  L6470_send(0x00);
  L6470_send(0x20); //回転スピードの設定
  L6470_send(0x00);
delay(1604);
  L6470_send(0xB8);
  
}
