#2-21 added recursive main method
import serial
import time
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

trigger = 1100 #this is the ppm it switches to desorption
DesorptionTime = 20

# Find the ports for your Arduinos
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

# Configure the serial ports
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

#sets sensor port num & communication rate 
arduinoData2=serial.Serial('com4',9600)
arduinoData=serial.Serial('com3',9600)


def main():
    T=1 #delay in seconds for each reading output
    triggerCount = 0
    while True :
        time.sleep(T) #delay in seconds for each reading output
        SensorData=readDataPacket() #data read as a tuple
        valueSensor1=SensorData[0] #read first value from data packet
        valueSensor2=SensorData[1] #read second value from data packet
        currentTime=SensorData[2] #read ct from data packet
        
        # see if senosr activates trigger and counts 'trips'
        if valueSensor1 > trigger:
            print(valueSensor1, valueSensor2, currentTime)
            triggerCount += triggerCount
            
        # enter absorbtion mode    
        if valueSensor1 <= trigger:
            print(valueSensor1, valueSensor2, currentTime)
            absorption()
            
        # enter desorption mode if tigger is activated 5 times     
        if triggerCount == 5: 
            desorption()
            print("I am desorbing for 90 minutes", currentTime)
            time.sleep(DesorptionTime) #holds the code for the desorption time, make sure the heat tape arduino has its proper code with delays 
            main() #call back main method to restart whole cycle

#Sends on/OFF to arduino for desorption stage
def desorption():
    command1 = 'OFF'
    command = 'ON'
    arduino_5.write(command.encode('utf-8'))
    arduino_6.write(command.encode('utf-8'))
    arduino_7.write(command1.encode('utf-8'))
    arduino_8.write(command1.encode('utf-8'))
    arduino_9.write(command1.encode('utf-8'))

#Sends on/OFF to arduino for absorption stage    
def absorption():
    command1 = 'OFF'
    command = 'ON'
    arduino_5.write(command1.encode('utf-8'))
    arduino_6.write(command1.encode('utf-8'))
    arduino_7.write(command.encode('utf-8'))
    arduino_8.write(command.encode('utf-8'))
    arduino_9.write(command.encode('utf-8'))

#read in the data from each arduino sensor             
def readDataPacket():
    while(arduinoData.inWaiting()==0): #creates a while loop that continues until there is datata avalible to read from sensor1
        pass
    dataPacket=arduinoData.readline()
    dataPacket=str(dataPacket,'utf-8')
    dataPacket=dataPacket.strip('\r\n')
    dataPacket=dataPacket.strip('CO2: ')
    
    while(arduinoData2.inWaiting()==0): #creates a while loop that continues until there is datata avalible to read from sensor2
        pass
    dataPacket2=arduinoData2.readline()
    dataPacket2=str(dataPacket2,'utf-8')
    dataPacket2=dataPacket2.strip('\r\n')
    dataPacket2=dataPacket2.strip('CO2: ')
    
    from datetime import datetime
    current_time = datetime.now()
    current_time_seconds = current_time.strftime("%H:%M:%S")
    #sensor value holds value triggering absorbtion/desorbtion
    sensor_value = float(dataPacket)
    sensor_value2 = float(dataPacket2)
    return sensor_value, sensor_value2, current_time_seconds
    
    
if __name__ == "__main__":
    main()