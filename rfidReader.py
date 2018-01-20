import serial
import socket
import sys
import os
from _thread import *
import serial.serialutil

last_dev = os.popen('ls /dev/ttyUSB* | tail -n 1').read()
last_dev=last_dev.replace("\n", "")
print(last_dev);
ser = serial.Serial(last_dev, 9600) # here you have to write your port. If you dont know how to find it just write ls -l /dev/tty.* in your terminal (i'm using mac)
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_address = ('192.168.137.105', 10005)

HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 10101 # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created');
conn1=None

#print ('connecting')
#sock.connect(server_address)
#print ('connected')
#Bind socket to local host and port
try:
    
    s.bind((HOST, PORT))
except socket.error as msg:
    if msg.errno == 98:
        print ('Port is already in use');
    else:
        print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]);
        sys.exit()
    
print ('Socket bind complete');


#Start listening on socket
s.listen(10)
print ('Socket now listening');
 
 
#Function for handling connections. This will be used to create threads
def clientthread():
    #Sending message to connected client
    #message='Welcome to the server. Type something and hit enter\n'
    #conn.send(bytes(message.encode('utf-8'))) #send only takes string
    
    #infinite loop so that function do not terminate and thread do not end.    
    while True:
        try:
            print("loop starts");
            global ser
            response = ser.readline()
            response=response.replace(b'\x02', b'')
            print("reading data")
            if(conn1):
                conn1.send(response)
            
            print (response);
        except serial.SerialException:            
            #x=os.system("ls /dev/ttyUSB*")
            #print(x);
            #if(x==0):
            try:
                print("ok");                
                last_dev = os.popen('ls /dev/ttyUSB* | tail -n 1').read()
                last_dev=last_dev.replace("\n", "")
                print(last_dev);          
                ser = serial.Serial(last_dev, 9600)
            except:
                print("");
        except FileNotFoundError:
            print("");
        except KeyboardInterrupt:            
            print("");
        except:
            print("");
            
    #ser.close()
    print("out of loop1");
    #came out of loop
    #conn1.close()


#now keep talking with the client
clientNo=0
start_new_thread(clientthread ,())
while 1:
   #wait to accept a connection - blocking call
    conn, addr = s.accept()
    if(conn1):
        conn1.close()
        
    conn1=conn
    clientNo=clientNo+1
    print ('Connected with ' + addr[0] + ':' + str(addr[1]));    
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.    


s.close()
