import random
import socket
import time
import sys

response='NORMAL' 
def random_number(response):
    '''This Function is to produce Random Value Which indicates the temprature'''
    if response == 'NORMAL':
        time.sleep(2)
    else:
        time.sleep(1)
    global temp
    temp=str(random.randint(5,59))
    return temp
    
def create_temp_socket():
    '''This function is to create the Socket for Slave.py'''
    try:
        global host1
        global port1
        global s1
        host1=socket.gethostname()
        port1=8765
        s1=socket.socket()
        print('Socket Created')
    except socket.error as msg:
        print("Socket creating error "+str(msg))

def bind_temp_socket():
    '''This function is to bind the slave.py socket'''
    try:
        global host1
        global port1
        global s1
        print("Binding the port"+str(port1))
        #s1.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s1.bind((host1,port1)) #to bind the slave.py socket
        s1.listen(5)
    except socket.error as msg:
        print("Socket binding error "+str(msg))
        socket.close()
        sys.exit() #to close the python file

def temp_socket_accept():
    '''This function is to accept the connection of slave.py'''
    conn,accept=s1.accept()
    print(f"Connection Established with ip {accept[0]} and port {accept[1]}")
    send_temp_data(conn)
    conn.close() #to close the connection with slave.py

def send_temp_data(conn):
    '''This function is to send the temprature data to slave.py and also reciving the response'''
    while True:
        try :
            global response
            temp=random_number(response) #to get the temprature value 
            conn.send(str.encode(temp)) #to send the temprature value to slave.py
            response =str(conn.recv(1024),'utf-8') #to get the response from slave.py
            if response == 'NORMAL':
                print('Temprature is Pleasent:')
            elif response == 'DECREASE':
                print("It's hot Outside --> Turning On the Cooler")
            else:
                print("It,s cold Outside---> Turning on The Heater")
        except socket.error as msg :
            print(msg)
            socket.close()
            sys.exit()


def main():
    '''To call the above functions'''
    create_temp_socket()
    bind_temp_socket()
    temp_socket_accept()
main()

