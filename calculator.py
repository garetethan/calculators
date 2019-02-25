'''
Created on Dec 24, 2017

@author: Garet


I want to make a Python calculator around the eval() function.
All numbers should be handled as Decimals. This prevents nasty floating point imprecision.

TODO:
* Variables seem to be working, but I want '7x' to evaluate to 7 times the value of x rather than a variable named _7x (if creating the var) or 7 concatenated to x (if referencing the var). This will mean that variable names will NOT be allowed to have numbers ANYWHERE in them (otherwise it is impossible to tell if 'foo3bar' is one, two, or three values). (The only alternative would be to check when saving each var if its name is contained in another var, and rejecting it if so, but this sounds labour intensive, and I think the outcome is worse.)
* Make a factorize or unmultiply function.
* Once you get most of the other things working, I would like to be able to map keys on my keyboard to different things so that I do not have to use all of keys around the edge to type in a mathematical expression. (I don't know if there would be a good way to do this, though.)
* math domain error is handled in sqrt(), but also needs to be handled in log().
So I don't think I understand this completely, but I think that, because of the way I am using Decimals, they are imprecise, and therefore offer no clear advantage over just using floats. This is because I am allowing eval() to convert a string like '-2' or '3 + 5' into the number -2 and 8, respectively, before Decimal() ever gets a hold of them. I need to find a way to turn all numbers into decimals before anything else happens to them.
* Add permutation and combination functions.
'''

from decimal import *
from math import *
# Necessary for DISALLOWED_VAR_NAMES below.
import math
from re import *
from sys import argv
from string import digits, ascii_uppercase
# Used to print list of available operations.
from tabulate import tabulate

FLOATING_POINT_PRECISION = 12
VAR_NAME_REGEX = r'[a-z_]\w*'
DISALLOWED_VAR_NAMES = [item for item in dir(math) if item[0] != '_']

def textDriver():
	'''Gets an expression from the user at the command line. If it is a variable assignment, it calc()s the right hand side and saves it. Otherwise, it assumes it to be a mathematical expression and prints the Decimal returned by calc()ing it.'''
	# First check if any flags were given.
	print(argv)
	if len(argv) > 1:
		if argv[1] == 'help':
			printHelp()
			return 1
		
		if argv[1] == 'ops':
			printOps()
			return 2
	
	# Set the precision of all Decimals that we create.
	getcontext().prec = FLOATING_POINT_PRECISION
	# The only sane way to round numbers.
	getcontext().rounding = ROUND_HALF_UP
	
	# Create a space for the user to store numbers temporarily (not between runs).
	# The name of this variable should remain consistent with the string literal inserted into expression below.
	variables = {'ans': 0}
	
	print('Enter a mathematical expression to evaluate below, or \'quit\'.\n')
	
	# Identical line at the end of the following while loop.
	expression = input('==> ')
	while expression != 'quit':
		if expression == 'help':
			printHelp()
			continue
		
		# If it is a variable assignment, save the value
		if '=' in expression:
			varName, varValue = expression.split('=')
			varName = varName.strip()
			varValue = insertVars(varValue, variables)
			if varName in DISALLOWED_VAR_NAMES:
				print(f'That name is not allowed because the math module (which this program imports ALL OF THE THINGS from) has a variable or a method by that name.')
			# As long as insertVars() was successful.
			elif varValue:
				if not match(f'^{VAR_NAME_REGEX}$', varName):
					# Add underscore to beginning if first char is a digit.
					if match(r'\d', varName[0]):
						varName = '_' + varName
					varName = sub(f'\W', r'_', varName.lower())
					print(f'Value saved as {varName}')
				try:
					variables[varName] = calc(varValue)
				# I tried to use 'e' as the name of the error message, causing it to print 2.71828...
				except NameError as err:
					print(f'Error: {err}')
		# Else it should be a mathematical expression to be evaluated (but it might include references to variables that have to be replaced with values).
		else:
			# Insert variable values.
			expression = insertVars(expression, variables)
			if expression:
				try:
					variables['ans'] = calc(expression)
					print(variables['ans'])
				except NameError as err:
					print(f'Error: {err}')
		
		# Get input for next run.
		expression = input('==> ')
	
	return 0
	
def insertVars(expression, variables):
	varFindingRegex = f'{VAR_NAME_REGEX}(?![a-zA-Z_\(])'
	varNames = findall(varFindingRegex, expression)
	expParts = split(varFindingRegex, expression)
	newExp = expParts[0]
	for i in range(len(varNames)):
		try:
			newExp = newExp + str(variables[varNames[i]]) + expParts[i + 1]
		except KeyError as err:
			# If variable is actually a constant from math module, leave it as text and wrap in Decimal() constructor.
			if varNames[i] in DISALLOWED_VAR_NAMES:
				newExp = f'{newExp}Decimal({varNames[i]}){expParts[i + 1]}'
			else:
				print(f'Error: There is no defined variable named {err}.')
				return None
	return newExp

def calc(expression):
	'''Takes a string expression and returns the result as a Decimal. Does not catch any exceptions.'''
	
	# Wrap all numbers with Decimal() before we perform any other operations with them, so that everything stays exact.
	# For some inexplicable magic reason, "-Decimal('7')" eval()s to Decimal('-7'). This makes things so much less complicated.
	expression = sub(r'([\d\.]+)', r'Decimal(\1)', expression)
	# Replace absolute-value bars with the abs() function that eval() will recognize.
	# Assumes that absolute-value bars are never nested (which is impossible to tell for sure).
	expression = sub(r'\|(.*?)\|', r'abs(\1)', expression)
	# Replace '^' (Python XOR) with '**' (exponentiation) and ')(' with ')*(' (implicit multiplication).
	replacements = {'^': '**', ')(': ')*('}
	for old in replacements:
		expression = expression.replace(old, replacements[old])
	
	# Let Python evaluate the filtered mathematical expression.
	return eval(expression)

# Define missing trig functions.
def sec(num):
	return 1 / Decimal(cos(num))

def csc(num):
	return 1 / Decimal(sin(num))

def cot(num):
	return 1 / Decimal(tan(num))

def asec(num):
	return Decimal(acos(1 / num))

def acsc(num):
	return Decimal(asin(1 / num))

def acot(num):
	return Decimal(acot(1 / num))

# Define trig functions that assume inputs are in degrees.
def sind(num):
	return Decimal(sin(radians(num)))

def cosd(num):
	return Decimal(cos(radians(num)))

def tand(num):
	return Decimal(tan(radians(num)))

def secd(num):
	return 1 / Decimal(cos(radians(num)))

def cscd(num):
	return 1 / Decimal(sin(radians(num)))

def cotd(num):
	return 1 / Decimal(tan(radians(num)))

# Define arc (inverse) trig functions that convert outputs to degrees.
def asind(num):
	return Decimal(degrees(asin(num)))

def acosd(num):
	return Decimal(degrees(acos(num)))

def atand(num):
	return Decimal(degrees(atan(num)))

def asecd(num):
	return Decimal(degrees(acos(1 / num)))

def acscd(num):
	return Decimal(degrees(asin(1 / num)))

def acotd(num):
	return Decimal(degrees(atan(1 / num)))

# Square, cube, and cuberoot, because I want them.
def sq(num):
	return num ** 2

def sqrt(num):
	'''Returns the positive square root of any positive, real number.
	Defined here (overwriting math module) just so that we can use Decimal's sqrt() and print a statement in the case of negative input.'''
	try:
		return num.sqrt()
	except InvalidOperation as err:
		print('Square root of a negative encountered. This calculator does not support imaginary numbers, so the square root of the absolute value of the given value has been returned.')
		return num.copy_abs().sqrt()

def cb(num):
	return Decimal(num ** 3)

def cbrt(num):
	return Decimal(num ** Decimal(1.0 / 3.0))

# Quadratic formula
# Adds discriminant.
def quadraticA(a, b, c):
	return Decimal(-b + sqrt(sq(b) - 4 * a * c) / 2 * a)

# Subtracts discriminant.
def quadraticS(a, b, c):
	return Decimal(-b - sqrt(sq(b) - 4 * a * c) / 2 * a)

# Overwrites math's ln() so that we can use Decimal's instead.
def ln(num):
	return num.ln()

def logC(num, base):
	# Change-of-base formula.
	return Decimal(ln(num) / ln(base))

def log10(num):
	return num.log10()

def lg(num):
	return logC(num, 2)

# Uses Decimal's e^x method.
def exp(num):
	return num.exp()

# gcd defined in math.
def lcm(a, b):
	'''Lowest common multiple.'''
	return a * b / gcd(a, b)

def changeBase(num, oldBase, newBase, precision=10):
	'''Should not be used in combination with other functions in the same statement (because it returns a string not necessarily parsable as a float).
num is treated as a decimal, and oldBase and newBase as ints.'''
	
	# From oldBase
	whole, _, fractional = num.strip().partition('.')
	num = int(whole + fractional, oldBase) * oldBase ** -len(fractional)

	# To newBase
	if num % 1 == 0:
		return Decimal(_intToBase(num, newBase))
	
	if newBase != 10:
		s = _intToBase(int(round(num / newBase ** -precision)), newBase)
		if precision:
			return Decimal(str(s)[:-precision] + '.' + str(s)[-precision:])
		else:
			return s
	else:
		return Decimal(num)

# ALL uses of '+' below are concatenation and not addition.
def _intToBase(number, newBase):
	# Define list of symbols used as digits
	# Lists of chars come from the string module.
	symbols = digits + ascii_uppercase
	
	# Uses "the division method"
	isNeg = number < 0
	number = abs(number)
	ans = ''
	while number:
		ans = symbols[number % newBase] + ans
		number //= newBase
	if isNeg:
		ans = '-' + ans
	return Decimal(ans)

def printHelp():
	with open('calculatorHelp.txt', 'r') as helpFile:
		for line in helpFile:
			if line[0] != '#':
				print(line, end='')

def printOps():
	opList = []
	with open('calculatorOps.csv', 'r') as opsFile:
		for line in opsFile:
			opList.append(line.split(';'))
	print(tabulate(opList, headers=['Operation', 'Number of Operands', 'Description'], tablefmt='fancy_grid'))
if __name__ == '__main__':
	textDriver()
