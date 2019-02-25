'''
Created on Mar 2, 2018

@author: Garet
'''
# I want to be able to find all of the factors of any (relatively low) integer.
# I would incorporate this into calculator, but because it takes one number and returns several, it does not fit into the calc() method (which is recursive) at all.
# primes.txt contains a list of the first prime numbers.

from math import sqrt
from re import match
from time import time

primeList = []

def main():
	print('Choose one of the options below by entering its corresponding number.\n'
		+ '0. Find all of the factors of an integer.\n'
		+ '1. Find all the prime factors of an integer.\n'
		+ '2. Determine whether an integer is prime.\n')
	
	# Sneakily load list of primes while waiting for user.
	with open('smallPrimes.txt', 'r') as primeFile:
		global primeList
		primeList = list(map(int, primeFile.read().split()))
	print(f'In main. {primeList}')
	
	choice = input('==> ')
	while not match(r'\d+', choice):
		print(f'Invalid input. Please enter a choice below.\n')
		choice = input('==> ')
	print('Enter the number to process.')
	# Loop above ensures int() should not raise exception.
	num = int(input('==> '))
	start = time()
	if choice in choices:
		print(f'Primes in main {primeList}.')
		print(choices[choice](num))
	else:
		print('Rejected!')
		return -1
	end = time()
	print(f'Ran in {round(end - start, 4)} seconds.')
	return 0

def factorize(product):
	smallFactors = [1]
	bigFactors = [product]
	
	# Because we find two factors at a time, we only have to check up to the square root.
	for i in range(2, int(sqrt(product))):
		if product % i == 0:
			# Add to end.
			smallFactors.append(i)
			# Add to beginning (puts all factors in ascending order at the end).
			bigFactors.insert(0, product / i)
	return smallFactors + bigFactors

def primeFactorize(product):
	
	if product > 10**4:
		print('Number too large. (Limited by size of smallPrimes.txt.)')
		return 0
	
	factors = []
	i = 0
	while primeList[i] < int(sqrt(product)):
		print(f'Checking {primeList[i]}')
		if product % primeList[i] == 0:
			factors.append(primeList[i])
		i += 1
	
	return factors

def isPrime(num):
	'''I just wanted to put this here since it doesn't belong anywhere else.'''
	if num < 10**4:
		return num in primeList
	else:
		return all(num % i != 0 for i in range(2, int(sqrt(num))))

# Used by main as a menu selection
choices = {
  '0': factorize,
  '1': primeFactorize,
  '2': isPrime
}

if __name__ == '__main__':
	main()