'''
Created on Dec 24, 2017

@author: Garet


STILL UNDER CONSTRUCTION.
I want to make a Python calculator around the eval() function.
All numbers should be handled as Decimals. This prevents nasty floating point imprecision.

TODO:
* Variables seemd to be workng, but I want '7x' to evaluate to 7 times the value of x rather than a variable named _7x (if creating the var) or 7 concatenated to x (if referencing the var). This will mean that variable names will to be allowed to have numbers ANYWHERE in them (otherwise it is impossible to tell if 'foo3bar' is one, two, or three values). (The only alternative would be to check when saving each var if its name is contained in another var, and rejecting it if so, but this sounds labour intensive, and I think the outcome is worse.)
* Make a factorize or unmultiply function.
* Once you get most of the other things working, I would like to be able to map keys on my keyboard to different things so that I do not have to use all of keys around the edge to type in a mathematical expression. (I don't know if there would be a good way to do this, though.)
* math domain error is handled in sqrt(), but also needs to be handled in log().
'''

from math import *
# Necessary for DISALLOWED_VAR_NAMES below.
import math
from decimal import *
from re import *
from random import random
from string import digits, ascii_uppercase

FLOATING_POINT_PRECISION = 12
DECIMAL_ONE = Decimal(1)
VAR_NAME_REGEX = r'[a-z_]\w*'
DISALLOWED_VAR_NAMES = [item for item in dir(math) if item[0] != r'_']

def textDriver():
	'''Gets an expression from the user at the command line. If it is a variable assignment, it calc()s the right hand side and saves it. Otherwise, it assumes it to be a mathematical expression and prints the Decimal returned by calling calc() on it.'''
	
	# Set the precision of all Decimals that we create.
	getcontext().prec = FLOATING_POINT_PRECISION
	getcontext().rounding = ROUND_HALF_UP
	
	# Create a space for the user to store numbers temporarily (not between runs).
	# The name of this variable should remain consistent with the string literal inserted into expression below.
	variables = {'ans': 0}
	
	print('Enter mathematical expression to evaluate below.\n')
	
	# Identical line at the end of the following while loop.
	expression = input('==> ')
	while expression != 'quit':
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
	
def insertVars(expression, variables):
	varFindingRegex = f'{VAR_NAME_REGEX}(?![a-zA-Z_\(])'
	varNames = findall(varFindingRegex, expression)
	expParts = split(varFindingRegex, expression)
	newExp = expParts[0]
	for i in range(len(varNames)):
		try:
			newExp = newExp + str(variables[varNames[i]]) + expParts[i + 1]
		except KeyError as err:
			# If variable is actually a constant from math module, just leave it as text.
			if varNames[i] in DISALLOWED_VAR_NAMES:
				newExp = newExp + varNames[i] + expParts[i + 1]
			else:
				print(f'Error: There is no defined variable named {err}.')
				return None
	return newExp

def calc(expression):
	'''Takes a string expression and returns the result as a Decimal. Does not catch any exceptions.'''
		
	# Replace absolute-value bars with the abs() function that eval() will recognize.
	# Assumes that absolute-value bars are never nested (which is impossible to tell for sure).
	expression = sub(r'\|*.?\|', 'abs(\1)', expression)
	# Replace '^' (Python XOR) with '**' (exponentiation); ')(' with ')*(' (implicit multiplication); and 'ln' with 'log' (which is base e by default).
	replacements = {'^': '**', ')(': ')*(', 'ln': 'log'}
	for old in replacements:
		expression = expression.replace(old, replacements[old])
	
	# Let Python evaluate the filtered mathematical expression and round to ten digits after the decimal.
	return Decimal(round(eval(expression), FLOATING_POINT_PRECISION))

# Define missing trig functions.
def sec(num):
	return Decimal(1 / cos(num))

def csc(num):
	return Decimal(DECIMAL_ONE / sin(num))

def cot(num):
	return Decimal(DECIMAL_ONE / tan(num))

def asec(num):
	return Decimal(acos(DECIMAL_ONE / num))

def acsc(num):
	return Decimal(asin(DECIMAL_ONE / num))

def acot(num):
	return Decimal(acot(DECIMAL_ONE / num))

# Define trig functions that assume inputs are in degrees.
def sind(num):
	return Decimal(sin(radians(num)))

def cosd(num):
	return Decimal(cos(radians(num)))

def tand(num):
	return Decimal(tan(radians(num)))

def secd(num):
	return Decimal(DECIMAL_ONE / cos(radians(num)))

def cscd(num):
	return Decimal(DECIMAL_ONE / sin(radians(num)))

def cotd(num):
	return Decimal(DECIMAL_ONE / tan(radians(num)))

# Define arc (inverse) trig functions that convert outputs to degrees.
def asind(num):
	return Decimal(degrees(asin(num)))

def acosd(num):
	return Decimal(degrees(acos(num)))

def atand(num):
	return Decimal(degrees(atan(num)))

def asecd(num):
	return Decimal(degrees(acos(DECIMAL_ONE / num)))

def acscd(num):
	return Decimal(degrees(asin(DECIMAL_ONE / num)))

def acotd(num):
	return Decimal(degrees(atan(DECIMAL_ONE / num)))

# Square, cube, and cuberoot, because I want them.
def sq(num):
	return Decimal(num ** 2)

def sqrt(num):
	'''Returns the positive square root of any positive, real number.
	Defined here just so that we can print a statement about complex numbers.'''
	try:
		return math.sqrt(num)
	except ValueError as err:
		print('Square root of a negative encountered. This calculator does not support imaginary numbers, so the square root of the absolute value of the given value has been returned.')
		return math.sqrt(abs(num))

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

def logC(num, base):
	return Decimal(log(num) / log(base))

def log10(num):
	return Decimal(logC(num, 10))

def lcm(a, b):
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



if __name__ == '__main__':
	textDriver()
