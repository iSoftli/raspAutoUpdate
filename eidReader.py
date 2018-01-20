from beid import BeidReader
from pprint import pprint
import sys
import socket
import base64
import json
from threading import Thread
from _thread import *
#Function for handling connections. This will be used to create threads

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    while True:
        print("reading data");
        if(conn):
            data = conn.recv(1024)
            print("have read data");
            if data:
                print(data);        
                if data==b'Done':
                    print("ok");
                    break
                print("ok1");
                #break
                print(data);
                try:
                    my_reader1 = MyReader()
                    dataReader=my_reader1.getData()
                    print(dataReader);
                #dataReader="test"
                    conn.sendall(dataReader.encode('utf-8'))
                    print('data sent1');
                    stringNewLine='\n'+'\r'        
                    conn.sendall(stringNewLine.encode('utf-8'))
                except:
                    stringNewLine='Error'
                    conn.sendall(stringNewLine.encode('utf-8'))
                    print('data sent');
                    stringNewLine='\n'+'\r'
                    conn.sendall(stringNewLine.encode('utf-8'))        
                    print("error");
            else:     
                print("out of loop");
                break   

    #came out of loop
    conn.close()


class MyReader(BeidReader):
    #my_json_string=""
    my_json_string =""
    def on_inserted(self, card):
        print("ok1");
        card.read_infos(1)
        b64_text  = base64.b64encode(card.photo)
        #print(card.photo.encode('b64'))
        #pprint(card.read_infos(1))
        #print(b64_text);
        #data = json.dumps({"payload": b64_text.decode('ascii') })
        #print (data);
        #printa(data);
        self.my_json_string =json.dumps({'Address': card.adresse,'PinCode': card.code_postal,'Bus':card.commune_delivrance,'Location': card.localite,
                                     'Lieu':card.lieu_naissance,'Country':card.nationalite,'Name':card.nom,'CardNumber':card.num_carte,'Nation Number':card.num_nat,
                                     'FullName':card.prenoms,'Sex':card.sexe,'Suffix':card.suffixe,'DOB':card.date_naissance,"payload": b64_text.decode('ascii')})
        print(self.my_json_string);
        #if(conn):
         #   conn.sendall(self.my_json_string.encode('utf-8'))
          #  print('data sent');
           # stringNewLine='\n'+'\r'
            #conn.sendall(stringNewLine.encode('utf-8'))
            #print('line sent');
            
    def getData(self):
        return self.my_json_string
    
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_address = ('192.168.0.110', 10004)
#sock.connect(server_address)
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 10103 # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created');        
print('connected');
try:
    
    s.bind((HOST, PORT))
except socket.error as msg:
    if msg.errno == 98:
        print ('Port is already in use');
    else:
        print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]);
        sys.exit()
    
print ('Socket bind complete');


s.listen(10)
print ('Socket now listening');


#my_reader = MyReader()
#now keep talking with the client
#my_reader = MyReader()
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print ('Connected with ' + addr[0] + ':' + str(addr[1]));
    try:
        my_reader = MyReader()
        if(conn):
            dataReader=my_reader.getData()
            print(dataReader);
            #dataReader="test"
            conn.sendall(dataReader.encode('utf-8'))
            print('data sent1');
            stringNewLine='\n'+'\r'        
            conn.sendall(stringNewLine.encode('utf-8'))
            
        start_new_thread(clientthread ,(conn,))
    except:
        stringNewLine='Error'
        conn.sendall(stringNewLine.encode('utf-8'))
        print('data sent');
        stringNewLine='\n'+'\r'
        conn.sendall(stringNewLine.encode('utf-8'))        
        print("error");
#conn.close()

s.close()

#print(my_reader.card.num_carte)
#print(my_reader.card.num_nat)
