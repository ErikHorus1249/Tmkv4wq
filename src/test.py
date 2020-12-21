from socket import *
import time
startTime = time.time()

if __name__ == '__main__':
   target = input('Enter the host to be scanned: ')
   t_IP = gethostbyname(target)
   print ('Starting scan on host: ', t_IP)
   s = socket(AF_INET, SOCK_STREAM)
   i = 22
   conn = s.connect_ex((t_IP, i))
   if(conn == 0) :
    print ('Port %d: OPEN' % (i,))
    s.close()

#    for i in range(20, 50):
#       s = socket(AF_INET, SOCK_STREAM)
      
#       conn = s.connect_ex((t_IP, i))
#       if(conn == 0) :
#          print ('Port %d: OPEN' % (i,))
#       s.close()
print('Time taken:', time.time() - startTime)