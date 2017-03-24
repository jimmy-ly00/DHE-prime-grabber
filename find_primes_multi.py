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
                return '{} {} {}'.format(server, servername, prime)
     
    except subprocess.CalledProcessError:
        return ('{} {} {}'.format(server, servername, "No_DHE"))
    except subprocess.TimeoutExpired:
        return ('{} {} {}'.format(server, servername, "Can't_connect"))
    except:
        return ('{} {} [}'.format(server, servername, "Error"))
    
if __name__ == "__main__":
    workers = 50
    pool = Pool(workers)
    with open('alex_top1mil') as f:
        result = pool.map(process_line, f,workers)
    for item in result:
        wr.writerow([item])
