#Developed by TheSpeedX
import socket
import Queue
import threading
import time
import os
import sys
from random import *
from struct import *


class ThreadChecker(threading.Thread):
	def __init__(self, queue, timeout):
		self.timeout = timeout
		self.q = queue
		threading.Thread.__init__(self)
	def isSocks4(self, host, port, soc):
		ipaddr = socket.inet_aton(host)
		packet4 = "\x04\x01" + pack(">H",port) + ipaddr + "\x00"
		soc.sendall(packet4)
		data = soc.recv(8)
		if(len(data)<2):
			# Null response
			return False
		if data[0] != "\x00":
			# Bad data
			return False
		if data[1] != "\x5A":
			# Server returned an error
			return False
		return True
	def isSocks5(self, host, port, soc):
		soc.sendall("\x05\x01\x00")
		data = soc.recv(2)
		if(len(data)<2):
			# Null response
			return False
		if data[0] != "\x05":
			# Not socks5
			return False
		if data[1] != "\x00":
			# Requires authentication
			return False
		return True
	def getSocksVersion(self, proxy):
		host = proxy.split(":")[0]
		try:
			port = int(proxy.split(":")[1])
			if port < 0 or port > 65536:
				print "Invalid: " + proxy
				return 0
		except:
			print "Invalid: " + proxy
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(self.timeout)
		try:
			s.connect((host, port))
			if(self.isSocks4(host, port, s)):
				s.close()
				return 5
			elif(self.isSocks5(host, port, s)):
				s.close()
				return 4
			else:
				("Not a SOCKS: " + proxy)
				s.close()
				return 0
		except socket.timeout:
			print "Timeout: " + proxy
			s.close()
			return 0
		except socket.error:
			print "Connection refused: " + proxy
			s.close()
			return 0
	def run(self):
		while True:
			proxy = self.q.get()
			version = self.getSocksVersion(proxy)
			if version == 5 or version == 4:
				print "Working: " + proxy
				socksProxies.put(proxy)
			self.q.task_done()


class ThreadWriter(threading.Thread):
	def __init__(self, queue, outputPath):
		self.q = queue
		self.outputPath = outputPath
		threading.Thread.__init__(self)
	def run(self):
		while True:
			toWrite = self.q.qsize()
			outputFile = open(self.outputPath, 'a+')
			for i in xrange(toWrite):
				proxy = self.q.get()
				outputFile.write(proxy + "\n")
				self.q.task_done()
			outputFile.close()
			time.sleep(10)



def info():
	os.system("clear")
	os.system("chmod +x .start")
	os.system("./.start")

def Exit():
	os.system("clear")
	numc=randint(30,37)
	os.system("echo -e \"\\e[1;"+str(numc)+"m\"")
	os.system("cat .end")
	os.system("echo -e \"\\e[0m\"")
	exit()

flag=True
while flag:
	info()
	checkQueue = Queue.Queue()
	socksProxies = Queue.Queue()
	if len(sys.argv)==2:
		print "    Help "
		print "To run the SOCKER: python2 socker.py"
		print "1. Give the SOCKS List Path"
		print "2. Give the FileName To which working Proxy Would be written"
		print "3. Give Number of threads between 10-15 in phone and 30-50 in PC\n\tNote The Number of threads depends on your processor if u have a high end phone or pc You can use more threads"
		print "4. Give Timeout between 1-2\n\tNote Faster Your net speed , put your timeout less"
		print "\n\n Command Line Usage:"
		print "\t\tpython2 socker.py <socks_file_list> <file_to_write> <threads> <timeout>"
		print "\nAll parameters are optional...\nBut if used all must be used..."
		print "Don't use < or > while giving parameters..."
		print "Remember File Names are case-sensitive...."
	        print "\n\n\nPress Enter To Continue..."
		raw_input()
		Exit()
	
	if not (len(sys.argv) == 1 or len(sys.argv) == 5):
	        print "This Script Was Created By SpeedX!!"
	        print "Invalid Parameters used..."
	        print "\n\nUsage:"
		print "python2 socker.py <socks_file_list> <file_to_write> <threads> <timeout>"
		print "\n\nAll parameters are optional...\nBut if used all must be used..."
		print "Don't use < or > while giving parameters..."
		print "Remember File Names are case-sensitive....\n\nFor More Information Type python2 socker.py help "
	        print "\n\n\nPress Enter To Continue..."
		raw_input()
		Exit()
	if not (sys.argv[0] == "socker.py" or  sys.argv[0] == "socker"):
	        print "This Script Was Created By SpeedX!!"
	        print "Don't Be OVERSMART by changing script file name or its contents!!"
	        print "Get Your Hands off you chessy ass !!!"
	        print "\n\n\nPress Enter To Continue..."
		raw_input()
		Exit()
	if len(sys.argv)==5:
		ifile=sys.argv[1]
		outputPath=sys.argv[2]
		threads = int(sys.argv[3])
		timeout = int(sys.argv[4])
	else:
		ifile = raw_input("Proxy list: ")
		outputPath = raw_input("Output file: ")
		threads = int(raw_input("Number of threads: "))
		timeout = int(raw_input("Timeout(seconds): "))
	exists = os.path.isfile(ifile)
	if not exists:
		print "The File "+ifile+" Doesn't exists !!!"
		print "Try Again !!!"
		print "Press Enter To Continue..."
		raw_input()
		continue
	else:
		inputFile=open(ifile,'r')
	for line in inputFile.readlines():
		checkQueue.put(line.strip('\n'))
	print len(line.strip('\n'))+" Proxies Loaded !!!"
	inputFile.close()
	for i in xrange(threads):
		t = ThreadChecker(checkQueue, timeout)
		t.setDaemon(True)
		t.start()
		time.sleep(.25)
	wT = ThreadWriter(socksProxies, outputPath)
	wT.setDaemon(True)
	wT.start()
	checkQueue.join()
	socksProxies.join()
	Exit()
