# DHE-prime-grabber
Grabs Diffie-Hellman primes from certificates using OpenSSL

### Example
Uses re-compiled OpenSSL with trace option on to view the Diffie-Hellman handshake protocol. Make sure openssl-trace and alexa_top1mil are in the same folder. Includes multiprocessing to make use of all cores and increase speed performance. Outputs a csv file instead of stdout for I/O bound reasons.

```python
./find_primes_multiprocess.py
```

If multiprocessing fails use:
```python
./find_primes.py 
```

