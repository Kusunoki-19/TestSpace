#include <SPI.h>

// ピン定義。
#define PIN_SPI_MOSI 11
#define PIN_SPI_MISO 12
#define PIN_SPI_SCK 13
#define PIN_SPI_SS 10

#define SW1  8
#define ON   LOW
void L6470_send(unsigned char add_or_val) {
  digitalWrite(PIN_SPI_SS, LOW);
  SPI.transfer(add_or_val); // アドレスもしくはデータ送信。
  digitalWrite(PIN_SPI_SS, HIGH);
}

void L6470_setup() {
  //最大回転スピード
  L6470_send(0x07);//レジスタアドレス
  L6470_send(0x00);//値(10bit),デフォルト0x41
  L6470_send(0x30);
  //モータ停止中の電圧設定
  L6470_send(0x09);//レジスタアドレス
  L6470_send(0x20);//値(8bit),デフォルト0x29
  //モータ定速回転時の電圧設定
  L6470_send(0x0a);//レジスタアドレス
  L6470_send(0x40);//値(8bit),デフォルト0x29
  //加速中の電圧設定
  L6470_send(0x0b);//レジスタアドレス
  L6470_send(0x40);//値(8bit),デフォルト0x29
  //減速中の電圧設定
  L6470_send(0x0c);//レジスタアドレス
  L6470_send(0x40);//値(8bit),デフォルト0x29

  //フ ル ス テ ッ プ,ハ ー フ ス テ ッ プ,1/4, 1/8,…,1/128 ステップの設定
  L6470_send(0x16);//レジスタアドレス
  L6470_send(0x00);//値(8bit)
}

void setup()
{
  delay(2000);
  // ピン設定。
  pinMode(PIN_SPI_MOSI, OUTPUT);
  pinMode(PIN_SPI_MISO, INPUT);
  pinMode(PIN_SPI_SCK, OUTPUT);
  pinMode(PIN_SPI_SS, OUTPUT);
  pinMode(SW1, INPUT_PULLUP);
  Serial.begin(115200);

  digitalWrite(PIN_SPI_SS, HIGH);
  //SPI通信開始
  SPI.begin();
  SPI.setDataMode(SPI_MODE3);//SCKの立ち上がりでテータを送受信＆アイドル時はpinをHIGHに設定
  SPI.setBitOrder(MSBFIRST);//MSBから送信

  //前のコマンドの引数を消去
  L6470_send(0x00);//nop
  L6470_send(0x00);
  L6470_send(0x00);
  L6470_send(0x00);
  //デバイスリセットコマンド
  L6470_send(0xc0);//ResetRevice

  L6470_setup();//L6470を設定
}

void loop()
{
  static uint32_t ONE_ROTATE_STEP = 400;
  static float angle_float = 0;
  static uint32_t angle = 0; 
  angle = 400;
  if (digitalRead(SW1) == ON) {
    //angle_float += 400 / 24;
    //angle = (uint32_t)(angle_float);
    //angle = angle % ONE_ROTATE_STEP; //ONE_ROTATE_STEP からはみ出さないようにする

    //angle += 400;

    uint8_t bits_8 = 0;

    //L6470_send(0b01101001); //GoTo_DIR命令 (DIR = 1 ->正回転)
    //L6470_send(0b01100000); //GoTo命令
    L6470_send(0b01000001); //Move命令 (DIR = 1 ->正回転)

    bits_8 = (uint8_t)(angle >> 16);
    L6470_send(bits_8); //上位8bit書き込み

    bits_8 = (uint8_t)(angle >> 8);
    L6470_send(bits_8); //中  8bit書き込み

    bits_8 = (uint8_t)(angle);
    L6470_send(bits_8); //下位8bit書き込み
    delay(1000);

    Serial.print("angle_float :"); Serial.println(angle_float);
    Serial.print("angle       :"); Serial.println(angle);
    Serial.print("upper  8bit :"); Serial.println((uint8_t)(angle >> 16), BIN);
    Serial.print("mediam 8bit :"); Serial.println((uint8_t)(angle >> 8), BIN);
    Serial.print("downer 8bit :"); Serial.println((uint8_t)(angle), BIN);
    Serial.print("\n");
  }
}
