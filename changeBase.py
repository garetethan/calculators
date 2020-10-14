# Copy-pasted from pyCalc.

def changeBase(num, oldBase, newBase):
	'''Should not be used in combination with other functions in the same statement (because it returns a string not necessarily parsable as a float).
	num is assumed to be a string representation of an integer, and oldBase and newBase integers.'''
	
	if oldBase < 2 or oldBase > 36 or newBase < 2 or newBase > 36:
		print('Error: Invalid base. Both bases must be positive integers no greater than 36.')
		return ''
	
	# From oldBase to base 10.
	num = int(num, oldBase)

	# From base 10 to newBase.
	if newBase == 10:
		return num
	else:
		# Define list of symbols used as digits
		# Lists of chars come from the string module.
		symbols = digits + ascii_uppercase
	
		# Uses "the division method"
		isNeg = oldNum < 0
		oldNum = abs(oldNum)
		newNum = ''
		while oldNum:
			newNum = f'{symbols[oldNum % newBase]}{newNum}'
			oldNum //= newBase
		if isNeg:
			newNum = f'-{newNum}'
		return newNum
