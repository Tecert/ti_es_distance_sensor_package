**# ti_es_distance_sensor_package
This repository is for the detection of obstacles around the telescope. For now, three ultrasone sensors are connected to the Arduino Uno. The Arduino Uno communicates with the Rasperry Pi 4B through I2C. The output of the communication is as follows:

One byte is sent from the Arduino Uno to the Rasperry Pi. The first four bits are used for the communication. The rest are unused for now.

Bit 0 is a verification bit to verify if data has been sent to the master when requested
If data has been sent to the master from the slave the verification bit(bit 0) will be 1**
Otherwise the bit will be zero
For now three sensors have been connected to the Arduino Uno. 

This is how the communiction works:
0x00 = no data has been sent from the slave to the master, this data is incorrect
0x01 = data has been sent from the slave to the master, this data is correct

Bits designated for the sensors work as follows

0 means that there is no detection within 10 cm and 1 means an object has been detected within 10 cm of the sensor
Bit 1 is for (name of ultrasone sensor one)
Bit 2 is for (name of ultrasone sensor two)
Bit 3 is for (name of ultrasone sensor three)
