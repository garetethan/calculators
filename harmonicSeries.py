# Apparently the Harmonic Series diverges, but it does so very slowly.
from time import sleep

s = 0
i = 1
while True:
	s += 1 / i
	if i % 10000000 == 0:
		print(f'The sum of the first {i} terms is: {s}.')
	i += 1
