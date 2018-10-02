'''
primesFormatter.py
Made just to remove specific whitespace from primes.txt.
Created on Mar 6, 2018

@author: Garet
'''
from factorizer import isPrime

maxPrime = int(input('How high should we go in finding primes?\n'))
primes = []

for i in range(maxPrime):
    if isPrime(i):
        primes.append(i)

print(f'DEBUG: len(primes) == {len(primes)}')
primesFile = open('primes.txt', 'w')
  
for p in primes:
    primesFile.write(str(p) + ' ')