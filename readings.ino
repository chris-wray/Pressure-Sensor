#include <SD.h> //Load SD library
#include <math.h>
int chipSelect = 4; //chip select pin for the MicroSD Card Adapter
File file; // file object that is used to read and write data
int analogPin1 = A0;
int analogPin2 = A1;


float getVoltage(int pin)
{ 
  //supply to sensor
  float Vcc = 3.3;
  
  //sensor resistor value
  float res = 3300;
 
  float sensorVoltage;
 
  if(pin == 0){
    sensorVoltage = (analogRead(A0) * Vcc);  
  }
  else if(pin == 1){
    sensorVoltage = (analogRead(A1) * Vcc) ; 
  }
  else if(pin == 2){
    sensorVoltage = (analogRead(A2) * Vcc) ; 
  }  
  //Serial.print("sensorVoltage:");
  //Serial.println(sensorVoltage);
  //Serial.print("Resistance:");
  //Serial.println((res * sensorVoltage) / (sensorVoltage - Vcc));
  return sensorVoltage/1023.0;
}

float getForce(float sensorVoltage){
  float force = 2.921771 - (-15.46268/-0.9896529)*(1 - exp(0.9896529*sensorVoltage));
  if(force <=4)
  {
    return 0.00;
  } 
  return force;
}

void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
   pinMode(chipSelect, OUTPUT); // chip select pin must be set to OUTPUT mode
  if (!SD.begin(chipSelect)) { // Initialize SD card
    Serial.println("Could not initialize SD card."); // if return value is false, something went wrong.
  }
  
  if (SD.exists("file.txt")) { // if "file.txt" exists, fill will be deleted
    Serial.println("File exists.");
    if (SD.remove("file.txt") == true) {
      Serial.println("Successfully removed file.");
    } else {
      Serial.println("Could not removed file.");
    }
  }
}

// the loop routine runs over and over again forever:
void loop() {

  // Open file and write to SD card
  file = SD.open("file.txt", FILE_WRITE); // open "file.txt" to write data
  if (file) {
    file.print(getForce(getVoltage(0))); // write data to file
    file.print(", ");
    file.print(getForce(getVoltage(1)));
    file.print(", ");
    file.println(getForce(getVoltage(2)));
    file.close(); // close file
  } else {
    Serial.println("Could not open file (writing).");
  }
  
  // print out the value you read
  Serial.print("Sensor 0: ");
  Serial.print(getForce(getVoltage(0)));
  Serial.print("\tSensor 1: ");
  Serial.print(getForce(getVoltage(1)));
  Serial.print("\tSensor 2: ");
  Serial.print(getForce(getVoltage(2)));
  Serial.println();

  //Delay until the next data reading
  delay(1000); // wait for 20ms
}
