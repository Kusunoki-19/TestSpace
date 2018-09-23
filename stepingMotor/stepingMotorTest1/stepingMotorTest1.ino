#include <SPI.h>//ライブラリ読み込み

//ピン番号設定
#define PIN_SDO 11
#define PIN_SDI 12
#define PIN_SCK 13
#define PIN_PORTC 10

//モーター回転速度設定
long speed = 100000;

void setup()//初期設定
{
  //ピンの入出力を決定
  pinMode(PIN_SDO, OUTPUT);
  pinMode(PIN_SDI, INPUT);
  pinMode(PIN_SCK, OUTPUT);
  pinMode(PIN_PORTC, OUTPUT);


  delay(2000);//よくわからないけどちょっと待ってみる

  digitalWrite(PIN_PORTC, HIGH); //ドライバを命令を受け付けない状態にする

  //SPI通信の初期設定
  SPI.begin();
  SPI.setDataMode(SPI_MODE3);
  SPI.setBitOrder(MSBFIRST);

}


void L6470_run(long speed) { //ドライバに命令を送るサブルーチン
  unsigned short dir;
  unsigned long spd;
  unsigned char spd_h;
  unsigned char spd_m;
  unsigned char spd_l;

  //マイナス値を入力したら回転方向を 反転する
  if (speed < 0) {
    dir = 0x50;
    spd = -1 * speed;
  }
  else {
    dir = 0x51;
    spd = speed;
  }

  //回転速度の設定をするための命令を作る
  spd_h = (unsigned char)((0x0F0000 & spd) >> 16);
  spd_m = (unsigned char)((0x000FF00 & spd) >> 8);
  spd_l = (unsigned char)(0x000FF & spd);

  //ドライバに命令を送る
  L6470_write(dir);
  L6470_write(spd_h);
  L6470_write(spd_m);
  L6470_write(spd_l);
}


void L6470_write(unsigned char command) { // ドライバに命令を送るサブルーチン
  digitalWrite(PIN_PORTC, LOW); //ドライバが命令を受け取れる状態にする
  SPI.transfer(command); //命令を送る
  digitalWrite(PIN_PORTC, HIGH); //ドライバが命令を受け取れない状態にする
}

void loop() { //本文
  L6470_run(speed);
  delay(3000);

}

