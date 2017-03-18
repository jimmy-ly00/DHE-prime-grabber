#!/usr/bin/python3
import sys, os, subprocess, re, csv
from multiprocessing import Pool

outfile = open('output.csv', 'w')
wr = csv.writer(outfile)

def process_line(line):
	row = line.split(',')	
	server = row[0]
	servername=row[1].strip('\n')
	try:
		cmd = subprocess.check_output([os.path.dirname(sys.argv[0])+"/openssl-trace",
			"s_client", "-trace",
			"-cipher", "DHE",
			"-connect", server+":443"],
			stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1)
		for line in cmd.decode("ISO-8859-1").splitlines():
			if 'dh_p' in line:
				prime = int(re.sub(".*: ", "", line), 16)
				#print('{}, {}, {}'.format(server, servername, prime))
				wr.writerow([server, servername, prime])
	except subprocess.CalledProcessError:
		#print('{}, {}'.format(server, "No DHE"))
		pass
	except subprocess.TimeoutExpired:
	  	#print('{}, {}'.format(server, "Can't connect"))
		pass

if __name__ == "__main__":
    pool = Pool()
    with open('alexa_top1mil') as f:
        results = pool.map(process_line, f,)

