#define LDR_PIN A0
#define PIR_PIN 2
#define LED_PIN 9

// declaring the variables



int timeLedIsOn = 0;
int currentTime = 0;

void setup() {
  Serial.begin(9600);
  pinMode(PIR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);

}

void loop() {
  int ldrValue = analogRead(LDR_PIN);
  int pirValue = digitalRead(PIR_PIN);
  if (pirValue == 1){
    int brightness = 255 - (ldrValue/1023.0 * 255);
    analogWrite(LED_PIN, brightness);
    timeLedIsOn++;
  }
  else {
    analogWrite(LED_PIN, 0);
  }
  currentTime++;
  Serial.print(currentTime);
  Serial.print(", ");
  Serial.print(ldrValue);
  Serial.print(", ");
  Serial.print(pirValue);
  Serial.print(", ");
  Serial.println(timeLedIsOn);
  delay(1000);
}








