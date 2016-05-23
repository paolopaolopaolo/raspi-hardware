int photoRPin = 2;
int lightLevel;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  //auto-adjust the minimum and maximum limits in real time
  lightLevel=analogRead(photoRPin);
 
  //Send the adjusted Light level result to Serial port (processing)
  Serial.println(lightLevel);

  //slow down the transmission for effective Serial communication.
  delay(50);
}