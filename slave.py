import socket
import sys

response ='NORMAL'
def creating_temp_socket():
    '''This Function is to create a Socket for temp.py'''
    try:
        global host1
        global port1
        global s1
        s1=socket.socket()
        host1=socket.gethostname()
        port1=8765
    except socket.error as msg:
        print(f'socket creation failed {msg}')

def creating_master_socket():
    '''This Function is to create a Socket for master.py'''
    try:
        global port2
        global s2
        s2=socket.socket()
        port2=5678
    except socket.error as msg:
        print(f'socket creation failed {msg}')

def accepting_master_connection():
    '''This function is to accept the connection of master and also connecting with the temp.py'''
    global conn
    global s2
    global s1
    global host1
    global port1
    conn, accept=s2.accept() #to accept the connection of master
    s1.connect((host1,port1)) #to connect with the temp..py
    print(f"Connection Established with ip {accept[0]} and port {accept[1]}")

def collecting_temp_data():
    '''This function is to collect the temprature data from temp.py'''
    try:
        global s1
        global conn
        global response
        while True:
            data=s1.recv(1024) #to store the data recieved from temp.py
            s1.send(str.encode(response))# to send the response of mater to temp.py
            global temp_value
            temp_value=data.decode('utf-8')
            sending_to_master(conn) 
    except socket.error as msg:
        print(f'socket connection failed {msg}')

def binding_master():
    '''this Function is to bind The master Socket'''
    try:
        global host1
        global s2
        global port2
        port2=5678
        #s2.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #to exclude the error of 'address already used'
        s2.bind((host1,port2)) #to bind the connection from master
        s2.listen(5)
    except socket.error as msg:
        print(f'socket binding error {msg}')
        socket.close()
        sys.exit()


def sending_to_master(conn):
    '''This Function is to send data (Temprature value) to master and also reciving the Response'''
    global temp_value
    global response
    while True:
        conn.send(str.encode(temp_value)) #To send the temprature  value to Master.py
        response=str(conn.recv(1024),'utf-8') #to get response from master.py
        collecting_temp_data()

def main_temp():
    '''This Function is to run Above Functions'''
    creating_temp_socket()
    creating_master_socket()
    binding_master()
    accepting_master_connection()
    collecting_temp_data()
    
main_temp()
