# Document has to be made where the ultrasone sensors are placed and what their names are, this will probably be in the designs
# Decide how many ultrasone sensors are going to be used so that can be final
# Sometimes I get this out of nowhere No distance data received from I2C device with address 8 and bus 1, probably because the rasperry is requesting too much too soon
# Ask Nico how to implement log code in here

import lgpio
import time
# Variable used for I2C_open and I2C_close
I2C_connection = None

# I2C address
I2C_addr = 0x08 # bus address

# I2C bus 1 is chosen for communication with I2C device
I2C_bus = 1

# read bytes
I2C_read_bytes = 1


# Bit 0 is a verification bit to verify if data has been sent to the master when requested
# If data has been sent to the master from the slave the verification bit(bit 0) will be 1
# Otherwise the bit will be zero

# For now four sensors have been connected to the Arduino Uno. This is how the communiction works:

# 0x00 = no data has been sent from the slave to the master, this data is incorrect 
# 0x01 = data has been sent from the slave to the master, this data is correct

# Bits designated for the sensors work as follows
# 0 means that there is no detection within 10 cm and 1 means an object has been detected within 10 cm of the sensor

# Bit 1 is for <name of ultrasone sensor one>
# Bit 2 is for <name of ultrasone sensor two>
# Bit 3 is for <name of ultrasone sensor three>
# Bit 4 is for <name of ultrasone sensor four>

# To see where the placements of the ultrasone sensors go to this document : <document of the position of the ultrasone sensors on the telescope>
def connect_I2C():
    global I2C_connection
    # Try to open bus 1 with slave address 8. if bus can't be opened an error message is printed on the screen
    try:
       I2C_connection = lgpio.i2c_open(I2C_bus, I2C_addr)
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except:
        print(f"Could not open bus with number {I2C_bus} and connect to I2C device at address {I2C_addr}")
        return
    
    try:
        data = lgpio.i2c_read_device(I2C_bus,I2C_read_bytes)
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except:
        print(f"Connection could not be established with I2C device at address {I2C_addr} and bus2 {I2C_bus}")
        return
    

    try:
        # If no data is received and the first value of the array is one, raise a I2CNoDataError
        if(data[1][0] == 0):
            print(f"No distance data received from I2C device with address {I2C_addr} and bus {I2C_bus}")
        else:
            print(data[1][0])

    except KeyboardInterrupt:
        raise KeyboardInterrupt


def main():
    interval = 0.25
    next_time = time.time() + interval
    try:
        while True:
            current_time = time.time()
            if current_time >= next_time:
                connect_I2C()
                next_time += interval
            time.sleep(0.001)
            

    # Handle Keyboard Exception
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        if I2C_connection!= None:
            lgpio.i2c_close(I2C_connection)

if __name__ == '__main__':
    main()
