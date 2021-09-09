import random
import socket
import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
import logging
from logging.handlers import RotatingFileHandler

y_axis=[]
x_axis=[]
plt.style.use('fivethirtyeight') # This is the plotting style

logger = logging.getLogger("LOG FILE OF TEMP DATA") 
logger.setLevel(logging.INFO) #set logging to info
logger.addHandler(RotatingFileHandler("Temp_Time.txt", maxBytes=2000, backupCount=1)) 

def create_graph_socket():
    '''This function is to create a socket to communicate with master'''

    try:
        global host1
        global port2
        global s2
        host1=socket.gethostname() 
        port2=2345
        s2=socket.socket() 
    except socket.error as msg:
        print("Socket creating error "+str(msg))

def connecting ():
    '''This function is to connect to the Master Module to have Temp data'''
    global s2
    global host1
    global port2
    try:
        s2.connect((host1,port2)) #to connect to the master module
    except socket.error as msg:
        print(f'socket connection failed {msg}')
        sys.exit()

def plotting_data(i):
    '''This function is to plotting the data'''
    global s2
    p=str(s2.recv(1024).decode('utf-8'))
    temp=int(p[:2])
    y_axis.append(temp) #appending the temprature values
    time=(datetime.datetime.now().strftime("%H:%M:%S")) #collecting the time in Hour : Minute : Sec format
    x_axis.append(time) #appending the time values
    if len(y_axis) == 20: 
        del y_axis[:1] #to delete the data if the y_axis exceeds length 20
    if len(x_axis) == 20:
        del x_axis[:1] #to delete the data if x_-axis exceeds length 20
    plt.cla() #to clear the plot each time to print a new one
    plt.plot(x_axis, y_axis)
    plt.xticks(rotation=45,ha='left') #to rotate the x_axis data 45 degree to left
    plt.title('Temperature Time Graph') 
    plt.xlabel('time')
    plt.ylabel('Temprature')
    plt.tight_layout() #for layout
    logger.info(f'Time is {time} and temprature is {temp}°C\n') #to write into log file

create_graph_socket()
connecting()
ani=FuncAnimation(plt.gcf(),plotting_data, interval=1000) #to animate the plotting function
plt.tight_layout()
plt.show()
