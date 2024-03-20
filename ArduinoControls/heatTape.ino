#define RELAY_PIN 8

void setup() {
  Serial.begin(9600);
  // initialize digital pin RELAY_PIN as an output.
  pinMode(RELAY_PIN, OUTPUT);
}


void loop() {
  if (Serial.available() > 0){
    String msg = Serial.readString();

    if (msg == "ON"){
      delay(5000); //delay for nitrogen
      digitalWrite(RELAY_PIN, HIGH);
      delay(10000); //allows for 1 hour of heat
      digitalWrite(RELAY_PIN, LOW);
      }
    else if (msg == "OFF"){
      digitalWrite(RELAY_PIN, LOW);
    }
    else{
      for (int i=0; i <5; i++){
        digitalWrite(RELAY_PIN, HIGH);   // turn the RELAY on 
        delay(500);                     // wait for a second
        digitalWrite(RELAY_PIN, LOW);    // turn the RELAY off
        delay(500);                     // wait for a second
      }
    }
  }
}