/* -----------------------------------------------------------------------------
  Author             : Osorio
  Check              : Wesley
  Version            : V1.0
  Date               : 23/05/2020
  Description        : Rollarm control via Serial entry
   ---------------------------------------------------------------------------*/

/* Include ------------------------------------------------------------------*/
// Create servo object to control a servo. 
#include <Servo.h> 

Servo servos[4];

//Starting the control variables
int readValue[4] = {0};
int controlValue[4] = {0};
//These are the min and max angle for each servo
int minMaxServoValue[4][2] = {{10,170},{10,170},{10,170},{100,180}};

int button = 3;

// Initialize the manualMode control variable
// 1 = Manual
// 0 = Serial
int manualMode = 0;
int delayTime = 0;

void setup() {
  //Start the serial.
  Serial.begin(9600);
  
  // Attach the servos on pins to the servo object
  servos[0].attach(4);
  servos[1].attach(5);
  servos[2].attach(6);
  servos[3].attach(7);

  setBaseValues();
  updateValues();
}

void loop() {

  changeMode();
  if(manualMode == 1){
    manualControl();  
  }
  else{
    serialControl();  
  }

  servosWrite();
  
  updateValues();

}

// Execute the manual control process
void manualControl(){
  potentiometerRead();
  mapValues();
}

//Read the potentiometer values
void potentiometerRead(){
  readValue[0] = analogRead(A0);
  readValue[1] = analogRead(A1);
  readValue[2] = analogRead(A2);
  readValue[3] = analogRead(A3);
}

// This is used to map the potentiometer value to the right angle
void mapValues(){
  readValue[0] = map(readValue[0], 0, 1023, minMaxServoValue[0][0], minMaxServoValue[0][1]); 
  readValue[1] = map(readValue[1], 0, 1023, minMaxServoValue[1][0], minMaxServoValue[1][1]);
  readValue[2] = map(readValue[2], 0, 1023, minMaxServoValue[2][0], minMaxServoValue[2][1]); 
  readValue[3] = map(readValue[3], 0, 1023, minMaxServoValue[3][0], minMaxServoValue[3][1]);
}

// Receive commands from the serial
void serialControl(){
  char readChar[64];
  Serial.readBytesUntil(33,readChar,64);
  String commandReceived = String(readChar);
  int commandStart = commandReceived.indexOf('#');
  if(commandStart > -1){
    int servoLimiter = commandReceived.indexOf('%');
    if(servoLimiter > -1){
      int commandEnd = commandReceived.indexOf('$');
      if(commandEnd > -1){
        // separate servo from associated data
        int selectedServo = commandReceived.substring(1,servoLimiter).toInt();
        int inputValue = commandReceived.substring(servoLimiter+1,commandEnd).toInt();
        readValue[selectedServo] = inputValue;  
      }   
    }
  }
  
}

// Updates the control values
void updateValues(){
  for (int i = 0; i < 4; i++){
    controlValue[i] = readValue[i];  
  }
}

// Check and change between manual and serial mode
void changeMode(){
  if (digitalRead(button) == 0) {
    if(manualMode == 1){
      manualMode = 0;
      Serial.println("Control mode set to SERIAL!");
    }else{
      manualMode = 1;
      Serial.println("Control mode set to MANUAL!");
    }
    delay(1000);
  }
}

// Set initial positions to the servos
void setBaseValues(){
  readValue[0] = 90;
  readValue[1] = 90;
  readValue[2] = 90;
  readValue[3] = 100;
}

// Writes the values to the servos
void servosWrite(){
    for (int i = 0; i < 4; i++){
    if( (readValue[i] - controlValue[i]) >= 0){
      for(; controlValue[i] <= readValue[i]; controlValue[i]++){
        servos[i].write(controlValue[i]);
        delay(delayTime);
      }
    }
    else
    {
      for (; controlValue[i] > readValue[i]; controlValue[i]--)
      {
        servos[i].write(controlValue[i]);
        delay(delayTime);
      }
    }
  }
}
