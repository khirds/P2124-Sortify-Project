const int RELAY_PIN = 2;    // Relay ki pin
const int TRIGGER_PIN = 3;  // sensor ya button ki pin

const int Pot = A0;

const uint8_t ENA_PIN = 6;  // PWM to L298 ENA
const uint8_t IN1_PIN = 7;  // L298 ki IN1 deni
const uint8_t IN2_PIN = 8;  // L298 KI IN2 deni


int RUN_SPEED = 255;        //speed kam ziyada
const bool RUN_FWD = true;  //forward ya reverse krne k liye

int PotValue = 0;

int Pwm = 0;

char Data;

bool SignalFromPi = false;


void setup() {
  Serial.begin(115200);

  pinMode(ENA_PIN, OUTPUT);
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(TRIGGER_PIN, INPUT);
  digitalWrite(RELAY_PIN, LOW);
  digitalWrite(ENA_PIN, LOW);
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
}

void loop() {


  ///////////////For Serial

  while (Serial.available() > 0) {
    Data = Serial.read();
    Serial.println(Data);



    PotValue = analogRead(Pot);
    Pwm = map(PotValue, 0, 1024, 0, 255);

    analogWrite(ENA_PIN, Pwm);
    digitalWrite(IN1_PIN, HIGH);
    digitalWrite(IN2_PIN, LOW);
    if (Data == '0') {

      SignalFromPi = false;
      digitalWrite(RELAY_PIN, LOW);

    } else {
    }
    if (Data == '1') {

      SignalFromPi = true;

    } else {
    }
  }

  if (SignalFromPi == true) {
    if (digitalRead(TRIGGER_PIN) == LOW) {

      digitalWrite(RELAY_PIN, HIGH);
      delay(3000);

      digitalWrite(RELAY_PIN, LOW);

      SignalFromPi = false;
    }
  }
  else{

  }

  ///////// Motor Control

  PotValue = analogRead(Pot);
  Pwm = map(PotValue, 0, 1024, 0, 255);

  analogWrite(ENA_PIN, Pwm);
  digitalWrite(IN1_PIN, HIGH);
  digitalWrite(IN2_PIN, LOW);

  //Serial.println(Pwm);
}