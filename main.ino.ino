#include <SD.h> //Load SD library
int chipSelect = 4; //chip select pin for the MicroSD Card Adapter
File file; // file object that is used to read and write data
int analogPin1 = A0;
int analogPin2 = A1;
/**
 * Get the resistance (in Ohms) of the sensor.
 */
 //code found on circuit.io
float getResistance(int pin)
{ 
  //supply to sensor
  float Vcc = 5.0;
  
  //sensor resistor value
  float res = 10000;
  
  float sensorVoltage = analogRead(pin) * Vcc / 1023;
  return res * (Vcc / sensorVoltage - 1);
}

//code found on circuit.io
float getForce(int pin)
{
  float resistance = getResistance(pin);
  //calculate force using curve broken into two parts of different slope
  if (resistance <= 600)
    return (1.0 / resistance - 0.00075) / 0.00000032639;
  else
    return (1.0 / resistance)  / 0.000000642857;
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
  // read the input on analog pin 0:
   float read_force = getForce(analogPin1);

  // read the input on analog pin 1:
   float read_force2 = getForce(analogPin2);
   
  //convert force to pounds
   float reading1 = read_force * 0.224809;
   float reading2 = read_force2 * 0.224809;
   
  // Open file and write to SD card
  file = SD.open("file.txt", FILE_WRITE); // open "file.txt" to write data
  if (file) {
    file.print(millis()); // write data to file
    file.print(", ");
    file.println(reading1);
    file.print(", ");
    file.println(reading2);
    file.close(); // close file
  } else {
    Serial.println("Could not open file (writing).");
  }
  
  // print out the value you read:
  Serial.print(reading1);
  Serial.print(", ");
  Serial.println(reading2);

  //Delay until the next data reading
  delay(20); // wait for 20ms
}
