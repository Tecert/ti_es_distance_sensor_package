# Document has to be made where the ultrasone sensors are placed and what their names are, this will probably be in the designs
# Decide how many ultrasone sensors are going to be used so that can be final
# Sometimes I get this out of nowhere No distance data received from I2C device with address 8 and bus 1, probably because the rasperry is requesting too much too soon
# Ask Nico how to implement log code in here

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import lgpio
import time


class UltrasoneSensorNode(Node):
    def __init__(self):
        super().__init__('ultrasone_sensor_node')

        # I2C Config
        self.I2C_addr = 0x08  # I2C address of Arduino
        self.I2C_bus = 1
        self.I2C_read_bytes = 1
        self.I2C_connection = None

        # Timer for polling the sensor
        self.timer_period = 0.25  # seconds
        self.timer = self.create_timer(self.timer_period, self.read_sensor_data)

        # Publisher using String messages
        self._distance_publisher_ = self.create_publisher(String, 'ti/es/distance_data', 10)
        self.log_publisher_ = self.create_publisher(String, "ti/es/logger_data",10)

        # Connect to I2C device
        self.connect_I2C()

    def publish_log(self, level: str, message: str):
        log_msg = String()
        timestamp = time.strftime('%H:%M')
        log_msg.data = f"[{timestamp}][{level}][distance_sensor] {message}"
        self.log_publisher_.publish(log_msg)
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
    def connect_I2C(self):
        try:
            self.I2C_connection = lgpio.i2c_open(self.I2C_bus, self.I2C_addr)
            self.publish_log("info", f"I2C connection opened on bus {self.I2C_bus} with address {self.I2C_addr}")
        except Exception:
            self.publish_log("error", f"Could not open I2C connection on bus {self.I2C_bus} with address {self.I2C_addr}")

    def read_sensor_data(self):
        if self.I2C_connection is None:
            self.publish_log("warning", f"No I2C connection established on bus {self.I2C_bus} with address {self.I2C_addr}")
            return

        try:
            data = lgpio.i2c_read_device(self.I2C_connection, self.I2C_read_bytes)
            sensor_byte = data[1][0]

            if sensor_byte == 0:
                self.publish_log("warning", f"No distance data received from slave device on bus {self.I2C_bus} with address {self.I2C_addr}")
            else:
                binary_repr = bin(sensor_byte)[2:].zfill(8)
                self.get_logger().info(f"Sensor Byte (bin): {binary_repr}")

                msg = String()
                msg.data = f"Sensor byte: {binary_repr}"
                self.publisher_.publish(msg)

        except Exception:
            self.publish_log("error", f"Error reading I2C slave device on bus {self.I2C_bus} with address {self.I2C_addr}")

    def destroy_node(self):
        if self.I2C_connection is not None:
            lgpio.i2c_close(self.I2C_connection)
            self.publish_log("info", f"Closed I2C connection on bus {self.I2C_bus} with address {self.I2C_addr}")
        super().destroy_node()
        


def main(args=None):
    rclpy.init(args=args)
    node = UltrasoneSensorNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("Keyboardinterrupt")
        # node.get_logger().info("KeyboardInterrupt: shutting down node...")
    finally:
        node.destroy_node()

        
if __name__ == '__main__':
    main()
