
// Include Wire library
#include <Wire.h>

// Make sure that the arduino is in slave mode for I2C
#define SLAVE_ADDRESS 8

// Define trig and echopins

#define trigPin_sensor_1 2  
#define echoPin_sensor_1 3
#define trigPin_sensor_2 4  
#define echoPin_sensor_2 5
#define trigPin_sensor_3 6  
#define echoPin_sensor_3 7
#define trigPin_sensor_3 6  
#define echoPin_sensor_3 7
#define trigPin_sensor_4 8  
#define echoPin_sensor_4 9

// Distances which are calculated while running are saved in the designated variables
float distance_sensor_1; 
float distance_sensor_2;
float distance_sensor_3; 
float distance_sensor_4; 

// Byte which is sent to the Rasperry pi

/*

Bit at address 0 is for sensor 1
0 = No object is detected within a range of 0 and 10

Bit at address 1 is for sensor 2
Bit at address 2 is for sensor 3

*/

byte detection_data = 0x00;

float read_ultrasonic_distance(int trigPin, int echoPin){
  digitalWrite(trigPin, LOW); 
  delayMicroseconds(2);  
  digitalWrite(trigPin, HIGH);  
	delayMicroseconds(10);  
	digitalWrite(trigPin, LOW); 

  float duration = pulseIn(echoPin, HIGH);
  return (duration*.0343)/2;

}

// This function sends one byte to the Rasperry Pi which is connected through I2C
void requestEvent() {
    Wire.write(detection_data);  

}

void setup() {

  // Start serial connection
  pinMode(trigPin_sensor_1, OUTPUT);  
	pinMode(echoPin_sensor_1, INPUT);
  pinMode(trigPin_sensor_2, OUTPUT);  
	pinMode(echoPin_sensor_2, INPUT);
  pinMode(trigPin_sensor_3, OUTPUT);  
	pinMode(echoPin_sensor_3, INPUT);
  pinMode(trigPin_sensor_4, OUTPUT);  
	pinMode(echoPin_sensor_4, INPUT);
  Serial.begin(9600); 

  // Join I2C bus as follower
  Wire.begin(SLAVE_ADDRESS);

  Wire.onRequest(requestEvent);

}


void loop() {

   
  //Get the distancec from the sensors
  distance_sensor_1 = read_ultrasonic_distance(trigPin_sensor_1, echoPin_sensor_1);
  delayMicroseconds(2);
  distance_sensor_2 = read_ultrasonic_distance(trigPin_sensor_2, echoPin_sensor_2);
  delayMicroseconds(2);
  distance_sensor_3 = read_ultrasonic_distance(trigPin_sensor_3, echoPin_sensor_3);
  delayMicroseconds(2);
  distance_sensor_4 = read_ultrasonic_distance(trigPin_sensor_4, echoPin_sensor_4);
  delayMicroseconds(2);
  
  // If the distance from the is greater than 10, no object has been detected and 0 is sent to the master, Otherwise an object has been detected and a 1 is sent to the master 
  if(distance_sensor_1 > 10){
    bitWrite(detection_data,1,0);
  }
  else{
    bitWrite(detection_data,1,1);
  } 

  if(distance_sensor_2 > 10){
    bitWrite(detection_data,2,0);
  }
  else{
    bitWrite(detection_data,2,1);
  } 

  if(distance_sensor_3 > 10){
    bitWrite(detection_data,3,0);
  }
  else{
    bitWrite(detection_data,3,1);
  } 

  if(distance_sensor_4 > 10){
    bitWrite(detection_data,4,0);
  }
  else{
    bitWrite(detection_data,4,1);
  } 

  // Serial.println(detection_data);
  //Verification bit on bit number 0
  bitWrite(detection_data,0,1);
  // delay(500);
}