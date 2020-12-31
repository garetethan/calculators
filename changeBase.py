'''Change Base'''

from sys import argv, stderr
import string

def main ():
	if len(argv) != 4:
		print(f'usage: python3 {argv[0]} num oldBase newBase', file=stderr)
		exit(1)
	print(changeBase(argv[1], int(argv[2]), int(argv[3])))

def changeBase (num, oldBase, newBase):
	'''
	num: Representation of the number to convert (str).
	oldBase: Current base of num (int). This base should itself be in base 10.
	newBase: Base to convert num to (int).
	Copied from an old version of sollux.py.
	'''
	
	if oldBase < 2 or oldBase > 36 or newBase < 2 or newBase > 36:
		print('Error: Invalid base. Both bases must be positive integers no greater than 36.')
		return ''
	
	# From oldBase to base 10.
	num = int(num, oldBase)

	# From base 10 to newBase.
	if newBase == 10:
		return num
	else:
		# Define list of symbols used as digits.
		# Lists of chars come from the string module.
		symbols = string.digits + string.ascii_uppercase
	
		# Uses "the division method".
		isNeg = num < 0
		oldNum = abs(num)
		newNum = ''
		while oldNum:
			newNum = f'{symbols[oldNum % newBase]}{newNum}'
			oldNum //= newBase
		if isNeg:
			newNum = f'-{newNum}'
		return newNum

if __name__ == '__main__':
	main()
