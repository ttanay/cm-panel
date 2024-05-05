const int ledPin = 11;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(19200); 
  pinMode(ledPin, OUTPUT); 
}

void loop() {
  // put your main code here, to run repeatedly:
  int brightness; 
  if(Serial.available()) {
    brightness = Serial.parseInt(); 
    analogWrite(ledPin, brightness); 
  }
}
