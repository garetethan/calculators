'''
Created on Dec 24, 2017

@author: Garet
'''


# STILL UNDER CONSTRUCTION.
# A while ago I tried to build a calculator in Java that took a String
# expression and evaluated it. I wanted it to correctly handle parentheses and
# order of operations. This was hard enough that I never really got it working.
# I decided that Python was probably an easier language to use to create little
# apps that I did not expect anyone but myself to use. So I started creating
# the same thing in Python using more or less the same strategy. Then I found
# out that Python, as usual, has a method that essentially does this all for
# you. It's called eval() and it's available everywhere.
# But I don't want it to just be a command-line thing. I want to replace the
# Windows calculator. So I found a third party graphics module (apparently
# there is no built in one) that seems quite common and have started to build
# the app.
# TODO:
# Let numbers be entered as days, hours, minutes, etc. Convert everything to
# seconds, perform calculations, then express in largest units and also smaller
# units if necessary.
# Make a factorize or unmultiply function.
# Make LCD and GCD functions.
# Add tau as a constant (if math doesn't already define it).
# Add a changeBase() function that lets one change the base of a number to
# enter / get numbers e.g. in base 12.

from math import *
from graphics import *

buttonLabels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '000', '+', '-', '*', '/', 'x^2', 'x^3', 'x^y']
buttonWidth = 50
buttonHeight = 25
topMarginHeight = 100

def main():
    
    winWidth = 500
    winHeight = 300
    win = GraphWin('Calculator', winWidth, winHeight)
    win.setBackground('white')
    
    # Draw text input box
    userInputTextSize = 15
    userInputWidth = 30
    userInput = Entry(Point(winWidth // 2, userInputTextSize), userInputWidth)
    userInput.setSize(userInputTextSize)
    userInput.setTextColor('black')
    userInput.setFace('courier')
    userInput.draw(win)
    
    resultDisplay = Text(Point(winWidth // 2, userInputTextSize * 2), 'Result will appear here.')
    resultDisplay.draw(win)
    
    rows = len(buttonLabels) // buttonHeight + 1
    columns = winWidth // buttonWidth
    
    i = 0
    while (i < rows * columns) and (i < len(buttonLabels)):
        # Row index is i // rows, column index is i % columns
        topLeftX = (i // rows) * (buttonWidth)
        topLeftY = topMarginHeight + (i % columns) * (buttonHeight)
        newButton = newButton(topLeftX, topLeftY, 50, 50, buttonLabels[i])
        i += 1
    
    # Create an exit button.
    exitButton = newButton(winWidth - 60, 10, 50, 50, 'Exit')
    
    # "Listen" for Enter and button clicks.
    while True:
        # "Listen" for button click.
        clickPoint = win.getMouse()
        if clickPoint.getY() > topMarginHeight:
            clickRow = clickPoint.getY() // buttonHeight
            clickColumn = clickPoint.getX() // buttonWidth
            buttonIndex = int(clickRow * (winWidth // buttonWidth) + clickColumn)
            print('DEBUG index = {}'.format(buttonIndex))
            if buttonIndex < len(buttonLabels):
                newInput = userInput.getText() + buttonLabels[buttonIndex]
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

# Takes the expression and gives the result at the command-line instead of graphically.
def textDriver():
    
    expression = raw_input('Enter a mathematical expression to evaluate below.\n')
    print('The result is: {}'.format(calc(expression)))

# Takes a string expression and returns the result as a float.
def calc(expression):
    
    # Adding a space to the end makes filtering through and changing things easier.
    expression += ' '
    
    
    i = 0
    # Number of absolute value bars we have come across.
    absCount = 0
    while i < len(expression):
        
        # Add '.0' to the end of all integers so that all calculations are floating point, not integer.
        if expression[i].isdigit():
            i += 1
            while expression[i].isdigit():
                i += 1
            if expression[i] != '.':
                expression = expression[:i] + '.0' + expression[i:]
                i += 1
        
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
    # ^ is XOR in Python.
    expression = expression.replace('^', '**')
    
    # Python's log function has a default base of e.
    expression = expression.replace('ln', 'log')
    
    
    print('[DEBUG] About to evaluate {}'.format(expression))
    
    # Let Python evaluate the filtered mathematical expression and round to ten digits after the decimal.
    return round(eval(expression), 10)

# Define missing trig functions.
def sec(num):
    return 1 / cos(num)

def csc(num):
    return 1 / sin(num)

def cot(num):
    return 1 / tan(num)

def asec(num):
    return acos(1 / num)

def acsc(num):
    return asin(1 / num)

def acot(num):
    return acot(1 / num)

# Define trig functions that assume inputs are in degrees.
def sind(num):
    return sin(radians(num))

def cosd(num):
    return cos(radians(num))

def tand(num):
    return tan(radians(num))

def secd(num):
    return 1 / cos(radians(num))

def cscd(num):
    return 1 / sin(radians(num))

def cotd(num):
    return 1 / tan(radians(num))

# Define arc (inverse) trig functions that convert outputs to degrees.
def asind(num):
    return degrees(asin(num))

def acosd(num):
    return degrees(acos(num))

def atand(num):
    return degrees(atan(num))

def asecd(num):
    return degrees(acos(1 / num))

def acscd(num):
    return degrees(asin(1 / num))

def acotd(num):
    return degrees(atan(1 / num))

# Square and cube, because I want them.
def sq(num):
    return num ** 2

def cb(num):
    return num ** 3

def cbrt(num):
    return num ** (1.0 / 3.0)

# Negation
def negate(num):
    return 0 - num

# Quadratic formula
# Adds discriminant.
def quadraticA(a, b, c):
    return (negate(b) + sqrt(sq(b) - 4 * a * c)) / 2 * a

# Subtracts discriminant.
def quadraticS(a, b, c):
    return (negate(b) - sqrt(sq(b) - 4 * a * c)) / 2 * a

def changeBase(num, oldBase, newBase):
    # TODO.
    # Convert num to an array of its digits, convert to base ten by multipying
    # each digit by oldBase^index, then convert to newBase using // and %.
    return num

# Just an adjustment of how arguments are given to graphics.py's Rectangle method.
def newButton(win, topLeftX, topLeftY, width, height, text):
    newButton = Rectangle(Point(topLeftX, topLeftY), Point(topLeftX + width, topLeftY + height))
    newButton.setFill('grey')
    newButton.draw(win)
    newLabel = Text(Point(topLeftX + (buttonWidth / 2), topLeftY + (buttonHeight / 2)), text)
    newLabel.setText(text)
    newLabel.setFace('courier')
    newLabel.setTextColor('white')
    newLabel.draw(win)

if __name__ == '__main__':
    main()
