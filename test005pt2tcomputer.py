#Brandon Riley
# live graph implementation for test 005
import time
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
import B_Test_file005
import os

x_vals = []
sensorValueInlet_data = []
sensorValueOulet_data = []



def update_plot(frame):
    plt.cla()
    plt.plot(x_vals, sensorValueInlet_data, label='Sensor 1')
    plt.plot(x_vals, sensorValueOulet_data, label='Sensor 2')
    plt.xlabel('TIME')
    plt.ylabel('CO2 levels')
    plt.legend()
    
def process_data():
    gTime = os.environ.get('x_vals')
    valueI = os.environ.get('sensorValueInlet_data')
    valueO = os.environ.get('sensorValueOutlet_data')
    
    x_vals.append(gTime)
    sensorValueInlet_data.append(valueI)
    sensorValueOulet_data.append(valueO)
    
#def write_adsorption_Data_csv():
 #   with open('CO2_data.csv', 'w', newline='') as csvfile:
  #      csv.writer.writerow(['Time', 'InletSensor', 'OutletSensor'])
   #     for x, s1, s2 in zip(x_vals, sensorValueInlet_data, sensorValueOulet_data):
   #         csv.writer.writerow([x, s1, s2]) 
    #x_vals.clear()
    #sensorValueInlet_data.clear()
    #sensorValueOulet_data.clear()
    
def on_close(event):
    with open('CO2_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Time', 'InletSensor', 'OutletSensor'])
        for x, s1, s2 in zip(x_vals, sensorValueInlet_data, sensorValueOulet_data):
            csv.writer.writerow([x, s1, s2]) 
    
fig, ax = plt.subplots()
fig.canvas.mpl_connect('close_event', on_close)

ani = FuncAnimation(fig, update_plot, interval = 1000)
plt.show(block=False)
plt.pause(0.01)