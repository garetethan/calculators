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
# Create a generic log function that takes a base variable.

from math import *
from graphics import *
from re import split


def main():
    textDriver()
    
def graphicalDriver():
    
    # Settings (constants).
    buttonLabels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '000', '+', '-', '*', '/', 'x^2', 'x^3', 'x^y']
    buttonWidth = 50
    buttonHeight = 25
    topMarginHeight = 100
    winWidth = 500
    winHalfWidth = round(winWidth / 2)
    winHeight = 300
    textSize = 15
    textFont = 'courier'
    textColour = 'black'
    userInputWidth = 30
    resultDisplayWidth = 30
    
    # Create window.
    win = GraphWin('Calculator', winWidth, winHeight)
    win.setBackground('white')
    
    # Draw text input box
    userInput = Entry(Point(winHalfWidth, textSize), userInputWidth)
    userInput.setSize(textSize)
    userInput.setFace(textFont)
    userInput.setTextColor(textColour)
    userInput.draw(win)
    
    # Draw box to display results of calculations.
    resultDisplay = Text(Point(round(winWidth / 2), textSize * 2), 'Result will appear here.')
    resultDisplay.setSize(textSize)
    resultDisplay.setFace(textFont)
    resultDisplay.setTextColor(textColour)
    resultDisplay.draw(win)
    
    rows = len(buttonLabels) // buttonHeight + 1
    columns = min(winWidth // buttonWidth, len(buttonLabels))
    
    buttonIndex = 0
    while (buttonIndex < rows * columns) and (buttonIndex < len(buttonLabels)):
        # Row index is buttonIndex // rows, column index is buttonIndex % columns
        topLeftX = (buttonIndex // rows) * buttonWidth
        topLeftY = topMarginHeight + ((buttonIndex % columns) * buttonHeight)
        drawButton = drawButton(win, topLeftX, topLeftY, buttonWidth, buttonHeight, buttonLabels[buttonIndex])
        buttonIndex += 1
    
    # Create an exit button.
    drawButton(winWidth - 60, 10, buttonWidth, buttonHeight, 'Exit')
    
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
    
    
    # Just an adjustment of how arguments are given to graphics.py's Rectangle method.
    # It does not return anything, but it draws the Rectangle.
    def drawButton(win, topLeftX, topLeftY, width, height, text):
        drawButton = Rectangle(Point(topLeftX, topLeftY), Point(topLeftX + width, topLeftY + height))
        drawButton.setFill('grey')
        drawButton.draw(win)
        newLabel = Text(Point(topLeftX + (width / 2), topLeftY + (height / 2)), text)
        newLabel.setText(text)
        newLabel.setFace('courier')
        newLabel.setTextColor('white')
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
        # If it is a variable assignment, blindly pass to exec().
        if '=' in expression:
            # Should just contain the name of the variable and its value.
            varName, varValue = expression.split('=')
            variables[varName.strip()] = calc(varValue)
        # Else it should be a mathematical expression to be evaluated.
        else:
#             # Look for word follows by anything other than '(' (including the end of the string).
#             variableTokens = split(r'([a-zA-z]+[^(]|[a-zA-z]+$)', expression)
#             
#             variableTokensLen = len(variableTokens)
#             if variableTokensLen % 2 == 0:
#                 print('Error: Even number of variable tokens in textDriver().')
#                 
#             filteredExpression = ''
#             for i in range(int(variableTokensLen / 2)):
#                 # The inserted string literal below should remain consistent with the name of the dictionary of user-defined variables.
#                 filteredExpression += variableTokens[i * 2] + str(variables[variableTokens[(i * 2) + 1].strip()]) + ' '
#             
#             # In case the for loop above didn't run
#             if filteredExpression == '':
#                 filteredExpression = expression
#                 
#             print(f'Sending {filteredExpression} to calc.')
            variables['ans'] = calc(expression)
            print(variables['ans'])
        
        # Get input for next run.
        expression = input('==> ')

# Takes a string expression and returns the result as a float.
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

def logC(num, base):
    return log(num) / log(base)

def log10(num):
    return logC(num, 10)

def changeBase(num, oldBase, newBase):
    # TODO.
    # Convert num to an array of its digits, convert to base ten by multipying
    # each digit by oldBase^index, then convert to newBase using // and %.
    
    # Convert to base 10.
    base10Sum = 0
    if oldBase == 10:
        base10Sum = num
    else:
        # Thanks to https://stackoverflow.com/a/21270338/5231183.
        numDigits = [int(d) for d in str(floor(num))]
        for d in numDigits:
            base10Sum += oldBase ** d
    
    # Convert to new base.
    newNum = base10Sum
    if newBase != 10:
        newDigits = []
        newNumLen = exponent = floor(logC(num, newBase)) + 1
        while base10Sum != 0:
            newDigits[newNumLen - exponent - 1] = base10Sum // (newBase ** exponent)
            base10Sum %= (newBase ** exponent)
            exponent -= 1
        
        newNum = int(''.join(newDigits))
    return newNum

if __name__ == '__main__':
    main()
