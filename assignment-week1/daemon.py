import os, time

newpid = os.fork()
if newpid == 0:
	time.sleep(10)
	print 'child process ending'
else:
	print 'parent waiting for child to end'
	os.wait()
	print 'parent process ending'