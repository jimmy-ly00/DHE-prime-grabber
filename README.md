# DHE-prime-grabber
Grabs Diffie-Hellman primes from certificates using OpenSSL. 

Censys raw data were used from here: https://censys.io/data

Primes from Alexa Top 1mil and IPv4 with cipher suits DHE can be found from here: https://drive.google.com/open?id=0B9QfvGuHrkSWVng0REhyUUFqQ2s

### Example
Uses re-compiled OpenSSL with trace option on to view the Diffie-Hellman handshake protocol. Make sure openssl-trace and alexa_top1mil are in the same folder. Includes multiprocessing to make use of all cores and increase speed performance. Outputs a csv file instead of stdout for I/O bound reasons. You can manually update the workers if you are not bounded by the network bandwidth!

Tip: You can run the script as a background process by ```nohup ./find_primes_multi.py & ```

**Warning**: IPv4 contains 50 million rows and could take up to 60 hours to run from a home network. As of 2017, it downloads 50GB and uploads 35GB worth of certificates and exchanges.

### Linux
```python
./find_primes_multi.py
```

If multiprocessing fails use:
```python
./find_primes.py 
```

### Windows
To run under Windows, you must change the relevant script cmd. Will implement this under one script later.
```python
cmd = subprocess.check_output([os.path.dirname(sys.argv[0])+"/openssl-trace",
                "s_client", "-trace",
                "-cipher", "DHE",
                "-connect", server+":443"],
                stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1) 
```
to 
```python
cmd = subprocess.check_output("openssl-trace.exe",
                "s_client", "-trace",
                "-cipher", "DHE",
                "-connect", server+":443"],
                stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3) 
```

To run, open cmd and cd into the working directory and execute:
```python
python ./find_primes_multi.py
```

If multiprocessing fails use:
```python
python ./find_primes.py 
```
