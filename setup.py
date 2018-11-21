import os
import sys
import time
from subprocess import call

if (float(sys.version[:3])<3):
	print("[ERROR] Python "+sys.version[:3]+" is not supported. Run file with Python 3")
	exit()

if (os.getuid() is not 0):
	print("[ERROR] Setup script must be execute with sudo")
	exit()

if (os.path.isfile('/bin/startup/netblink.py') is True):
	print("[ERROR] Program already instaled")
	exit()

print(r"""
              ___ ___  __                   
	|\ | |__   |  |__) |    | |\ | |__/ 
	| \| |___  |  |__) |___ | | \| |  \      
                    
""")
print("	+ Preparing program directory")
call("sudo mkdir -p /bin/startup ",shell=True)
print("	+ Creating temporary files")

f = open("netblink.py", "w")
f.write(r"""
from subprocess import call
import time
import socket
time.sleep(2)
for o in range(0,10):
	
	start_time = time.time()
	
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		ip = s.getsockname()[0]
		s.close() 
		ip=ip[ip.find(".")+1:]
		ip=ip[ip.find(".")+1:]

		ip=ip[ip.find(".")+1:] #COMMENT THAT LINE TO LEAVE 3. OCTET
		ip=ip.replace(".","") 
	except:
		ip="404"
		pass
	call("sudo echo gpio >> /sys/class/leds/led0/trigger",shell=True)
	time.sleep(2)
	call("sudo echo 1 >> /sys/class/leds/led0/brightness",shell=True)
	time.sleep(2)
	for i in range(0, len(ip)):
		if(int(ip[i]) is 0):
			call("sudo echo 0 >> /sys/class/leds/led0/brightness",shell=True)
			time.sleep(1)
			call("sudo echo 1 >> /sys/class/leds/led0/brightness",shell=True)
		for o in range(0, int(ip[i])):
			call("sudo echo 0 >> /sys/class/leds/led0/brightness",shell=True)
			time.sleep(0.01)
			call("sudo echo 1 >> /sys/class/leds/led0/brightness",shell=True)
			time.sleep(0.4)
		time.sleep(2)
	call("sudo echo 0 >> /sys/class/leds/led0/brightness",shell=True)
	time.sleep(2)
	elapsed_time = time.time() - start_time
	call("echo mmc0 >>/sys/class/leds/led0/trigger",shell=True)
	time.sleep(60-int(elapsed_time))
""")
f.close()
call("sudo mv netblink.py /bin/startup/netblink.py",shell=True)

print("	+ Copying python executable to target directory ")
print("	+ Creating systemctl service file")

with open("/lib/systemd/system/netblink.service", "w") as f:
	f.write(r"""[Unit]
Description=Led blinking network service
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python3 /bin/startup/netblink.py

[Install]
WantedBy=multi-user.target
		""")
	f.close
print("	+ Changing file permissions")
call("sudo chmod 644 /lib/systemd/system/netblink.service",shell=True)
time.sleep(1)
print("	+ Reloading systemctl")
call("sudo systemctl daemon-reload",shell=True)
time.sleep(2)
print("	+ Enabling netblink.service ")
call("sudo systemctl enable netblink.service",shell=True)
print("	= DONE\n")


