void setup() {
  Serial.begin(9600);  // set baud rate 9600 bps
  pinMode(13, OUTPUT); // set arduino led as output
}

void loop() {
  Serial.print("Ai reusit!");
  delay(10);          // delay 10 milliseconds
  Serial.println();   // prints another carriage return
}
