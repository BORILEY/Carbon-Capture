#has coms for lab computer not laptop
import serial
import time
import serial.tools.list_ports
from datetime import datetime

trigger = 770  # this is the ppm it switches to desorption
DesorptionTime = 20

# Find the ports for your Arduinos
ports = serial.tools.list_ports.comports()
arduino_port_5 = "COM" + str(5)
arduino_port_6 = "COM" + str(6)
arduino_port_7 = "COM" + str(7)
arduino_port_8 = "COM" + str(8)
arduino_port_9 = "COM" + str(9)

# Check if ports are found
if arduino_port_5 is None:
    print("Arduino on COM5 not found.")
if arduino_port_6 is None:
    print("Arduino on COM6 not found.")
if arduino_port_7 is None:
    print("Arduino on COM7 not found.")
if arduino_port_8 is None:
    print("Arduino on COM8 not found.")
if arduino_port_9 is None:
    print("Arduino on COM9 not found.")
# If any port is not found, exit the program

# Create Serial instances for each Arduino
arduino_5 = serial.Serial()
arduino_6 = serial.Serial()
arduino_7 = serial.Serial()
arduino_8 = serial.Serial()
arduino_9 = serial.Serial()
#arduinos = [serial.Serial(port=f"COM{port_num}", baudrate=9600) for port_num in range(5, 10)]
arduino_5.baudrate = 9600
arduino_5.port = arduino_port_5
arduino_5.open()

arduino_6.baudrate = 9600
arduino_6.port = arduino_port_6
arduino_6.open()

arduino_7.baudrate = 9600
arduino_7.port = arduino_port_7
arduino_7.open()

arduino_8.baudrate = 9600
arduino_8.port = arduino_port_8
arduino_8.open()

arduino_9.baudrate = 9600
arduino_9.port = arduino_port_9
arduino_9.open()
# Serial instances for sensor data
arduinoData = serial.Serial('COM3', 9600)
arduinoData2 = serial.Serial('COM4', 9600)
time.sleep(1)


def main():
    T = 1  # delay in seconds for each reading output
    while True:
        time.sleep(T)
        sensor_data = read_data_packet()
        value_sensor1, value_sensor2, current_time = sensor_data

        if value_sensor2 <= trigger:
            print(value_sensor1, value_sensor2, current_time)
            absorption()

        if value_sensor2 > trigger:
            print(value_sensor1, value_sensor2, current_time)
            desorption()
            print("I am desorbing for 90 minutes", current_time)
            time.sleep(DesorptionTime)


def desorption():
    command1 = 'OFF'
    command = 'ON'
    arduino_5.write(command.encode('utf-8'))
    arduino_6.write(command.encode('utf-8'))
    arduino_7.write(command1.encode('utf-8'))
    arduino_8.write(command1.encode('utf-8'))
    arduino_9.write(command1.encode('utf-8'))


def absorption():
    command1 = 'OFF'
    command = 'ON'
    arduino_5.write(command1.encode('utf-8'))
    arduino_6.write(command1.encode('utf-8'))
    arduino_7.write(command.encode('utf-8'))
    arduino_8.write(command.encode('utf-8'))
    arduino_9.write(command.encode('utf-8'))


def read_data_packet():
    def get_latest_status(arduino):
        status = b''
        while arduino.in_waiting > 0:
            status += arduino.readline()
        return status

    data_packets = []
    for arduino in [arduinoData, arduinoData2]:
        status = get_latest_status(arduino)
        data_packet = status.decode('utf-8').strip('\r\n').strip('CO2: ')
        try:
            while(arduinoData.inWaiting()==0 & arduinoData2.inWaiting()==0): #creates a while loop that continues until there is data avalible to read from sensor1
                pass
            data_packets.append(float(data_packet))
        except ValueError:
            print("Error: Received invalid data from Arduino")
            # Handle the error here (e.g., set data_packet to a default value or log the error)
            data_packets.append(0.0)  # Default value or any appropriate handling

    current_time = datetime.now().strftime("%H:%M:%S")
    return data_packets[0], data_packets[1], current_time



if __name__ == "__main__":
    main()
