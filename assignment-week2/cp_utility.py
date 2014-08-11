import sys, os, fcntl, signal

CHILD_PID = 0
target_file = 'test.out'
def fork_child(pending_data):
	#print 'fork_child', pending_data
	pid = os.fork()
	if pid == CHILD_PID:
		#print 'open', os.getpid()
		if os.path.exists(target_file):
			#print 'target_file exists', os.getpid()
			fd = open(target_file, 'a+')
		else:
			#print 'target_file creating', os.getpid()
			fd = open(target_file, 'w')
		try:
			fcntl.flock(fd, fcntl.LOCK_EX)
			fd.write(pending_data)
			#print 'written in child', pending_data
		finally:
			fd.close()

		return pid
	else:
		return pid

def handler(signum, frame):
	print 'handler called'
	print signum, frame

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "No input file given. usage: python cp_utility.py fname"
		sys.exit(0)
	fname = sys.argv[1]
	fp = open(fname, 'r')
	pending_data = ''
	child_pids = []
	signal.signal(signal.SIGSEGV, handler)


	try:
		while True:
			data = fp.read(1)
			if not data:
				break
			if data == '0':
				if not pending_data:
					continue
				child_pid = fork_child(pending_data)
				if child_pid == 0:
					sys.exit(0)
				else:
					child_pids.append(child_pid)
					pending_data = ''
					continue
			pending_data += data
	finally:
		fp.close()

	for pid in child_pids:
		#print 'waiting for pid', pid
		os.waitpid(pid, 0)
		#print 'done waiting for pid', pid
