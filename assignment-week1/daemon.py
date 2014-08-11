import os, time

try:
	newpid = os.fork()	
	if newpid == 0:
		time.sleep(5)
		print 'child process ending'
	else:
		print 'parent spawned child with pid', newpid
		print 'parent process waiting for child to end'
		os.wait()
		print 'parent process ending'
except os.OSError, fault:
	print 'Execption occurred during fork', str(fault)
except Exception, fault:
	print 'Error occurred', str(fault)