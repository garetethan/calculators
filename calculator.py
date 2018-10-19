'''
Created on Dec 24, 2017

@author: Garet
'''


# STILL UNDER CONSTRUCTION.
# I want to make a Python calculator around the eval() function.
# But I don't want it to just be a command-line thing. I want to replace the
# Windows calculator. So I found a third party graphics module (apparently
# there is no built in one) that seems quite common and have started to build
# the app.
# All numbers should be handled as Decimals. This prevents nasty floating point imprecision.
# TODO:
# Let numbers be entered as days, hours, minutes, etc. Convert everything to
# seconds, perform calculations, then express in largest units and also smaller
# units if necessary.
# Make a factorize or unmultiply function.
# Make LCD and GCD functions.
# Add tau as a constant (if math doesn't already define it).
# Let the text driver accept variable assignments, e.g.
# ==> x = 6
# ==> x + 7
# 13
# Make the text driver continuously prompt for more input until told to quit
# (so one can perform multiple calculates in one run).
# Consider replacing the || / abs() switch in calc with a regex solution. (This
# seems like it would proabably be simpler.)
# Make it possible to type in functions (e.g. cos) without parentheses when
# they only have one simple, literal argument (e.g. cos2). I think it might be
# possible to loop through looking (with a regex) for a word followed
# immediately by a number, then surround the number with parentheses.
# Once you get most of the other things working, I would like to be able to map
# keys on my keyboard to different things so that I do not have to use all of
# keys around the edge to type in a mathematical expression. (I don't know if
# there would be a good way to do this, though.)
# Make it possible to change the decimal precision setting (getcontext().prec) while the program is running.

from math import *
from decimal import *
from graphics import *
from re import split
import string

DECIMAL_ONE = Decimal(1)

def main():
    # Set the precision of all Decimals that we create.
    getcontext().prec = 24
    getcontext().rounding = ROUND_HALF_UP
    textDriver()
    
def graphicalDriver():
    
    # Settings (constants).
    BUTTON_LABELS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '000', '+', '-', '*', '/', 'x^2', 'x^3', 'x^y']
    BUTTON_WIDTH = 50
    BUTTON_HEIGHT = 25
    TOP_MARGIN_HEIGHT = 100
    WIN_WIDTH = 500
    HALF_WIN_WIDTH = round(WIN_WIDTH / 2)
    WIN_HEIGHT = 300
    TEXT_SIZE = 15
    TEXT_FONT = 'courier'
    TEXT_COLOUR = 'black'
    USER_INPUT_WIDTH = 30
    RESULT_DISPLAY_WIDTH = 30
    
    # Create window.
    win = GraphWin('Calculator', WIN_WIDTH, WIN_HEIGHT)
    win.setBackground('white')
    
    # Draw text input box
    userInput = Entry(Point(HALF_WIN_WIDTH, TEXT_SIZE), USER_INPUT_WIDTH)
    userInput.setSize(TEXT_SIZE)
    userInput.setFace(TEXT_FONT)
    userInput.setTextColor(TEXT_COLOUR)
    userInput.draw(win)
    
    # Draw box to display results of calculations.
    resultDisplay = Text(Point(round(WIN_WIDTH / 2), TEXT_SIZE * 2), 'Result will appear here.')
    resultDisplay.setSize(TEXT_SIZE)
    resultDisplay.setFace(TEXT_FONT)
    resultDisplay.setTextColor(TEXT_COLOUR)
    resultDisplay.draw(win)
    
		# Draw buttons.
    rows = len(BUTTON_LABELS) // BUTTON_HEIGHT + 1
    columns = min(WIN_WIDTH // BUTTON_WIDTH, len(BUTTON_LABELS))
    
    buttonIndex = 0
    while (buttonIndex < rows * columns) and (buttonIndex < len(BUTTON_LABELS)):
        # Row index is buttonIndex // rows, column index is buttonIndex % columns
        topLeftX = (buttonIndex // rows) * BUTTON_WIDTH
        topLeftY = TOP_MARGIN_HEIGHT + ((buttonIndex % columns) * BUTTON_HEIGHT)
        drawButton = drawButton(win, topLeftX, topLeftY, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_LABELS[buttonIndex])
        buttonIndex += 1
    
    # Create an exit button.
    drawButton(WIN_WIDTH - 60, 10, BUTTON_WIDTH, BUTTON_HEIGHT, 'Exit')
    
    # "Listen" for Enter and button clicks.
    while True:
        # "Listen" for button click.
        clickPoint = win.getMouse()
        if clickPoint.getY() > TOP_MARGIN_HEIGHT:
            clickRow = clickPoint.getY() // BUTTON_HEIGHT
            clickColumn = clickPoint.getX() // BUTTON_WIDTH
            buttonIndex = int(clickRow * (WIN_WIDTH // BUTTON_WIDTH) + clickColumn)
            print('DEBUG index = {}'.format(buttonIndex))
            if buttonIndex < len(BUTTON_LABELS):
                newInput = userInput.getText() + BUTTON_LABELS[buttonIndex]
                userInput.setText(newInput)
        
        # "Listen" for Enter key.
        if win.getKey() == 'Return':
            # Calculate and display result.
            try:
                result = calc(userInput.getText())
                resultDisplay.setText(result)
            except ZeroDivisionError:
                resultDisplay.setText('Undefined! (Attempted division by zero.)')
            except OverflowError:
                resultDisplay.setText('Woah! That number is too big.')
            except NameError:
                resultDisplay.setText('You used a word that I do not recognize. Check spelling.')
    
    
    # Just an adjustment of how arguments are given to graphics.py's Rectangle method.
    # It does not return anything, but it draws the Rectangle.
    def drawButton(win, topLeftX, topLeftY, width, height, text):
        drawButton = Rectangle(Point(topLeftX, topLeftY), Point(topLeftX + width, topLeftY + height))
        drawButton.setFill('grey')
        drawButton.draw(win)
        newLabel = Text(Point(topLeftX + (width / 2), topLeftY + (height / 2)), text)
        newLabel.setText(text)
        newLabel.setFace(TEXT_FONT)
        newLabel.setTextColor(TEXT_COLOUR)
        newLabel.draw(win)
        return

# Takes the expression and gives the result at the command-line instead of graphically.
def textDriver():
    
    # Create a space for the user to store numbers temporarily.
    # The name of this variable should remain consistent with the string literal inserted into expression below.
    variables = {'ans': 0}
    
    print('Enter mathematical expression to evaluate below.\n')
    
    expression = input('==> ')
    while expression.lower() != 'quit':
        # If it is a variable assignment, save the value
        if '=' in expression:
            exec(expression)
        # Else it should be a mathematical expression to be evaluated.
        else:
          print(calc(expression))
        
        # Get input for next run.
        expression = input('==> ')

# Takes a string expression and returns the result as a decimal.
# Does not catch exceptions.
def calc(expression):
    
    # Adding a space to the end makes filtering through and changing things easier.
    expression += ' '
    
    i = 0
    # Number of absolute value bars we have come across.
    absCount = 0
    while i < len(expression):
        
        # Replace absolute-value bars with the abs() function that eval() will recognize.
        if expression[i] == '|':
            if absCount % 2 == 0:
                expression = expression[:i - 1] + 'abs(' + expression[i:]
            else:
                expression = expression[:i - 1] + ')' + expression[i:]
        
        # Adds multiplication where it is implied between parentheses.
        if expression[i] == ')' and expression[i + 1] == '(':
            expression = expression[:i] + '*' + expression[i:]
        i += 1
    
    # ^ is XOR in Python. ** is used for exponentiation.
    expression = expression.replace('^', '**')
    
    # Python's log function has a default base of e.
    expression = expression.replace('ln', 'log')
    
    # Let Python evaluate the filtered mathematical expression and round to ten digits after the decimal.
    return Decimal(round(eval(expression), 10))

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

# Meant to be called on a list that the user has defined.
def mean(nums):
	return sum(nums) / len(nums)

# From statistics. Meant to be called on a list.
def variance(nums):
	squareSum = 0
	for num in nums:
		squareSum += num ** 2
	return (squareSum - len(nums) * (mean(nums) ** 2)) / (len(nums) - 1)

# Standard deviation from statistics. Meant to be called on a list.
def sd(nums):
	return sqrt(variance(nums))


# Should not be used in combination with other functions in the same statement (because it returns a string not necessarily parsable as a float).
# num is treated as a decimal, and oldBase and newBase as ints.
def changeBase(num, oldBase, newBase, precision=10):
    
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
    symbols = string.digits + string.ascii_uppercase
    
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
    main()
