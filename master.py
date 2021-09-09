import socket
import sys

def create_graph_socket():
    '''Thi function is to create a socket for plot.py'''
    try:
        global host1
        global port2
        global s2
        host1=socket.gethostname()
        port2=2345
        s2=socket.socket()
        print('Socket Created\n')
    except socket.error as msg:
        print("Socket creating error "+str(msg))

def bind_graph_socket():
    '''This function is to bind the graph socket'''
    try:
        global host1
        global port2
        global s2
        print("Binding the Master port "+str(port2))
        s2.bind((host1,port2)) #binding the graph socket
        s2.listen(5) 
    except socket.error as msg:
        print("Socket binding error "+str(msg))
        socket.close()
        sys.exit()

def creating_socket():
    '''This function is to create socket for slave.py'''
    try:
        global host1
        global port
        global s
        port=5678
        s=socket.socket()
    except socket.error as msg:
        print(f'Socket creation failed {msg}')

def connecting():
    '''This Function is for acceptng the connection with the plot.py '''
    try:
        global s
        global port
        global host1
        global conn
        global s2
        conn,accept=s2.accept() #accepting the connection of plot.py
        print(f"Connection Established with ip {accept[0]} and port {accept[1]}\n")
        s.connect((host1,port))
        getting_data()
    except socket.error as msg:
        print(f'socket connection failed {msg}')

def getting_data():
    '''This function is to get the data i.e temprature value from slave.py'''
    global s
    global data
    try :

        while True:
            data=str(s.recv(1024).decode('utf-8')) #to recive the temprature data from slave.py
            if int(data) >= 40 :
                s.send(str.encode("DECREASE")) #to send data back to slave.py
            elif int(data) <= 10 :
                s.send(str.encode("INCREASE"))
            else :
                s.send(str.encode("NORMAL"))   
                #print(data)
         
            sending_data(data) 
    except socket.error as msg:
            print("Error while recieving data"+str(msg))


def sending_data(data):
    '''This function is to send data to plot.py'''
    global conn
    conn.send(str.encode(data))

create_graph_socket()
creating_socket()
bind_graph_socket()
connecting()



