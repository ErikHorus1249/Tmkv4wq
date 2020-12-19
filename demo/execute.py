import subprocess
import time
print ("start")
start_time = time.time()
subprocess.call("./main.sh")
print("scanned in "+str(round((time.time()-start_time),2))+" seconds")
