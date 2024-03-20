#define RELAY_PIN 8

void setup() {
  Serial.begin(9600);
  // initialize digital pin RELAY_PIN as an output.
  pinMode(RELAY_PIN, OUTPUT);
}

// the loop function runs over and over again forever   
void loop() {
  if (Serial.available() > 0){
    String msg = Serial.readString();

    if (msg == "ON"){
      digitalWrite(RELAY_PIN, HIGH);
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

