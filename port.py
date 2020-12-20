from socket import *
import socket
import time
  
def scan_port():
   target = input('Nhap vao ip')
   t_IP = gethostbyname(target)
   print ('Starting scan on host: ', t_IP)
   print(get_connection(t_IP,22))
   if get_connection(t_IP,22) == 0 or  get_connection(t_IP,23) == 0:
      return True
   return False

def get_connection(host,port):
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.settimeout(1)
      conn = s.connect_ex((host, port))
      return conn

if __name__ == '__main__':
   startTime = time.time()
   if(scan_port()):
          print("Co ssh/telnet")
   else:
          print("have no")
   print('Time taken:', time.time() - startTime)
