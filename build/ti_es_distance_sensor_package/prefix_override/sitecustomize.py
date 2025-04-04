import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/clare/Documents/ros_workplace/install/ti_es_distance_sensor_package'
