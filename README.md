ti_es_distance_sensor_package

This repository is for the detection of obstacles around the telescope. For now, four ultrasone sensors are connected to the Arduino Uno. The Arduino Uno is at slave address 0x08 and communicates with the Rasperry Pi 4B through I2C. The output of the communication is as follows:

One byte is sent from the Arduino Uno to the Rasperry Pi. The first five bits are used for the communication. The rest are unused. For now four sensors have been connected to the Arduino Uno. Bits that are used will change according to the amount of ultrasone sensor's that are connected

Bit 0 is a verification bit to verify if data has been sent to the master when requested.
If data has been sent from the slave to the master, the verification bit(bit at position 0) will be 1, otherwise the bit will be zero.

This is how the communiction works:
0x00 = no data has been sent from the slave to the master, this data is incorrect
0x01 = data has been sent from the slave to the master, this data is correct

Bits designated for the sensors work as follows:

The value of the bit will be 0 if there is no detection within 10 cm of the ultrasone sensor. 
The value of the bit will be 1 if an object has been detected within 10 cm of the sensor.
Bit 1 is for (name of ultrasone sensor one)
Bit 2 is for (name of ultrasone sensor two)
Bit 3 is for (name of ultrasone sensor three)
Bit 4 is for (name of ultrasone sensor four)
