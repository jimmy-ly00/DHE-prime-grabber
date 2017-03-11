# DHE-prime-grabber
Grabs Diffie-Hellman primes from certificates using OpenSSL

### Example
Uses re-compiled OpenSSL with trace option on to view the Diffie-Hellman handshake protocol. Make sure openssl-trace and alexa_top1mil is in the same folder.

```python
./find_primes.py
or
./find_primes.py > data.csv
```
