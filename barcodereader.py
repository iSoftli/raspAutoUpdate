import evdev
from evdev import *
#from azure.storage.queue import QueueService, QueueMessageFormat
import threading
import time
from queue import *
import datetime
import socket
from _thread import *
# responsible for uploading the barcodes to the azure storage queue.
class BarcodeUploader:
  def __init__(self):
  
    # Instiantiate the azure queue service (from the azure.storage.queue package)
    #self.queue_service = QueueService(account_name='wereoutof', account_key='your-key-here')

    # azure functions is _very_ confused is the text isn't base64 encoded
    #self.queue_service.encode_function = QueueMessageFormat.text_base64encode

    # use a simple queue to avoid blocking operations
    self.queue = LifoQueue()
    t = threading.Thread(target=self.worker, args=())
    t.daemon = True
    t.start()

  # processes all messages (barcodes) in queue - uploading them to azure one by one
  def worker(self):
      while True:
        while not self.queue.empty():
          try:
            barcode = self.queue.get()
            #self.queue_service.put_message('barcodes', u'account-key:' + barcode)
            self.sock.sendall(barcode)
          except Exception as exc:
            print("Exception occured when uploading barcode:"  + repr(exc))
      
      # re-submit task into queue
            self.queue.task_done()
            self.queue.put(barcode)
          else:
            print("Barcode " + barcode + " registered")
            self.queue.task_done()
        time.sleep(1)

  def register(self, barcode):
      print ("Registering barcode " + barcode + "...")
      self.queue.put(barcode)

current_barcode = ""
conn1=None
# Reads barcode from "device"
def readBarcodes():
  global current_barcode
  global device
  print ("Reading barcodes from device")
  while True:
      if(device is not None):
        print("found the dvice");
        try:            
          for event in device.read_loop():
                if event.type == evdev.ecodes.EV_KEY and event.value == 1:
                  keycode = categorize(event).keycode
                  if keycode == 'KEY_ENTER':
                    #uploader.register(current_barcode)
                    current_barcode+=  '\r' + '\n';
                    print(current_barcode);            
                    if(conn1):
                        conn1.sendall(bytes(current_barcode.encode('utf-8')))
                        
                    current_barcode = ""
                  else:
                    print(keycode);
                    current_barcode += keycode[4:]
        except:
            print("error no device");
            #if(device is None):
            device=find_device()    
      else:
          print("else finding device");
          device=find_device()


  #break
# Finds the input device with the name "Barcode Reader ".
# Could and should be parameterized, of course. Device name as cmd line parameter, perhaps?
def find_device():
  device=None
  device_name = 'Optoelectronics Co., Ltd. USB Code Reader'
  devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
  for d in devices:
      print("List device " + d.name)
      #if d.name == device_name:
      print("Found device " + d.name)
      device = d
          
  return device

# Find device...
device = find_device()

if device is None:
  print("Unable to find " )
else:
  print("");
    
  #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  #server_address = ('192.168.0.110', 10006)
  #sock.connect(server_address)  
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 10102 # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created');
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
#... instantiate the uploader...
  #uploader = BarcodeUploader()
  # ... and read the bar codes.
start_new_thread(readBarcodes ,())
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    if(conn1):
        conn1.close()
        
    conn1=conn
    print ('Connected with ' + addr[0] + ':' + str(addr[1]))    
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    
#readBarcodes()

s.close()