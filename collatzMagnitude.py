# collatz.py
# Written by Garet Robertson.
# Last significant update 2017 August 31.
# This little program is designed to test Collatz Conjecture (https://en.wikipedia.org/wiki/Collatz_conjecture) for random large integers.

from sys import argv
from random import randint

def main():
	# check command line arguments
	if len(argv) != 2:
		print('Usage: python collatz.py n')
		exit(1)
	if int(argv[1]) < 1:
		print('Error: Input must be a positive (non-zero) integer.')
		exit(2)
	
	numDigits = int(argv[1])
	n = randint(10 ** (numDigits - 1), (10 ** numDigits) - 1)
	print(f'Verifying the Collatz Conjecture for {n}.')
	# send to recursive function
	hotpo(n)
	exit(0)

def hotpo (n):
	steps = 0
	while n != 1:
		# print(f'{n} → ', end = '')
		steps += 1
		if n % 2 == 0:
			n //= 2
		else:
			n = 3 * n + 1
	
	if steps == 1:
		print('1.\n1 step was required to solve.')
	else:
		print('1.\n{} steps were required to solve.'.format(steps))

if __name__ == '__main__':
	main()
