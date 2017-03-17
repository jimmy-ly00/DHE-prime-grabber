#!/usr/bin/python3
import sys, os, subprocess, re, csv
outfile = open('output.csv', 'w')
wr = csv.writer(outfile)

with open('alexa_top1mil', 'r') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		#define columns
		server = row[1]
		
		try:
			cmd = subprocess.check_output([os.path.dirname(sys.argv[0])+"/openssl-trace",
				"s_client", "-trace",
				"-cipher", "DHE",
				"-connect", server+":443"],
				stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1)
			for line in cmd.decode("utf-8").splitlines():
				if 'dh_p' in line:
					prime = int(re.sub(".*: ", "", line), 16)
					#a = ('{}, {}'.format(server, prime))
					wr.writerow([server, prime])
		except subprocess.CalledProcessError:
			#print('{}, {}'.format(server, "No DHE"))
			pass
		except subprocess.TimeoutExpired:
		  	#print('{}, {}'.format(server, "Can't connect"))
			pass
