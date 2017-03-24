#!/usr/bin/python3
import sys, os, subprocess, re, time, itertools, csv
from multiprocessing import Process, Manager, Pool

outfile = open('output.csv', 'w')
wr = csv.writer(outfile)

def worker(in_queue, out_list):
    while True:
        line = in_queue.get()
        row = line[1].split(',')
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
                    #out_list.append([server, servername, prime])
                out_list.append('{}, {}, {}'.format(server, servername, prime))
        except subprocess.CalledProcessError:
            out_list.append('{} {} {}'.format(server, servername, "No_DHE"))
        except subprocess.TimeoutExpired:
            out_list.append('{} {} {}'.format(server, servername, "Can't_connect"))
        except:
            out_list.append('{} {} {}'.format(server, servername, "Error"))

        # fake work
        time.sleep(.5)

if __name__ == "__main__":
    num_workers = 100

    manager = Manager()
    results = manager.list()
    work = manager.Queue(num_workers)
	
    # start for workers    
    pool = []
    for i in range(num_workers):
        p = Process(target=worker, args=(work, results))
        p.start()
        pool.append(p)
		
    # produce data
    with open("alexa_top1mil") as f:
        iters = itertools.chain(f, (None,)*num_workers)
        for line in enumerate(iters):
            work.put(line)

    for p in pool:
        p.join()
	
    print(results)
    #pool.close()
