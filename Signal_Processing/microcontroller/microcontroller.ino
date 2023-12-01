const int analogPin = A0; 

void setup() {
  Serial.begin(9600);
}

void loop() {
  int sensorValue = analogRead(analogPin);

  // if (sensorValue != 0) {
  //   Serial.print("Analog value: ");
  //   Serial.println(sensorValue);
  // }   
  Serial.println(sensorValue);  
  delay(20);
}