import sys, os, fcntl, signal, traceback

CHILD_PID = 0
target_file = 'test.out'
def fork_child(pending_data):
	try:
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
	except Exception, fault:
		print 'Exception occurred', str(fault)
		traceback.print_exc()
		return -1

def handler(signum, frame):
	try:
		print 'handler called'
		print signum, frame
	except Exception, fault:
		print 'Failure in handler', str(fault)

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
				if child_pid == -1:
					print 'Failed to fork child, exiting after waiting for child processes'
					break
				if child_pid == 0:
					sys.exit(0)
				else:
					print 'Forked child', child_pid
					child_pids.append(child_pid)
					pending_data = ''
					continue
			pending_data += data
	finally:
		fp.close()

	print 'Waiting for child processes to end'
	for pid in child_pids:
		try:
			os.waitpid(pid, 0)
		except Exception, fault:
			print 'Waiting for child %s failed, error:%s', (pid, str(fault))

