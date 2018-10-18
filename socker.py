#Developed by TheSpeedX
import socket
import Queue
import threading
import time

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
checkQueue = Queue.Queue()
socksProxies = Queue.Queue()

print(' This Script was made by SpeedX')
if not (len(sys.argv) == 1 or  len(sys.argv) == 3):
        print "This Script Was Created By SpeedX!!"
        print "Invalid Parameters used..."
        print "\n\nUsage:"
	print "python2 socker.py <socks_file_list> <file_to_write>"
	print "\n\nBoth parameters are optional...\nBut if used both must be used..."
	print "Don't use < or > while giving filenames..."
	print "Remember File Names are case-sensitive...."
        exit()
if not (sys.argv[0] == "socker.py" or  sys.argv[0] == "socker"):
        print "This Script Was Created By SpeedX!!"
        print "Don't Be OVERSMART by changing script file name or its contents!!"
        print "Get Your Hands off you chessy ass !!!"
        exit()
if len(sys.argv)==3:
	inputFile=sys.argv[1]
	outputPath=sys.argv[2]
inputFile = open(raw_input("Proxy list: "), 'r')
outputPath = raw_input("Output file: ")
exists = os.path.isfile(inputFile)
if not exists:
	print "The File "+inputFile+" Doesn't exists !!!"
	print "Try Again !!!"


threads = int(raw_input("Number of threads: "))
timeout = int(raw_input("Timeout(seconds): "))
for line in inputFile.readlines():
	checkQueue.put(line.strip('\n'))
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
