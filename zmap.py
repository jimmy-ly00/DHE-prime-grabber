#!/usr/bin/python3
import sys, os, subprocess, re, csv
from multiprocessing import Pool

FILE = "zmap_results"
WORKERS = 80

outfile = open('output.csv', 'w')
wr = csv.writer(outfile)

def process_line(line):
    row = line.split(',')	
    server = row[0]
    try:
        cmd = subprocess.check_output([os.path.dirname(sys.argv[0])+"/openssl-trace",
            "s_client", "-trace",
            "-cipher", "DHE",
            "-connect", server+":443"],
            stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1)
        for line in cmd.decode("ISO-8859-1").splitlines():
            if 'dh_p' in line:
                prime = int(re.sub(".*: ", "", line), 16)
                return '{} {}'.format(server, prime)
     
    except subprocess.CalledProcessError:
        return ('{} {}'.format(server, "No_DHE"))
    except subprocess.TimeoutExpired:
        return ('{} {}'.format(server, "Can't_connect"))
    except:
        return ('{} {}'.format(server, "Error"))
    
if __name__ == "__main__":
    pool = Pool(WORKERS)
    with open(FILE) as f:
        result = pool.map(process_line, f, WORKERS)
    for item in result:
        wr.writerow([item])
