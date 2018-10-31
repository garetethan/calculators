'''
A place to save major code blocks that I am in the process of re-implementing in calculator.py.
'''

while expression.lower() != 'quit':
		# If it is a variable assignment, save the value
		if '=' in expression:
			# Should just contain the name of the variable and its value.
			varName, varValue = expression.split('=')
			variables[varName.strip()] = calc(varValue)
		# Else it should be a mathematical expression to be evaluated.
		else:
			# Look for word follows by anything other than '(' (including the end of the string).
			variableTokens = split(r'([a-zA-z]+[^(]|[a-zA-z]+$)', expression)
			 
			variableTokensLen = len(variableTokens)
			if variableTokensLen % 2 == 0:
				print('Error: Even number of variable tokens in textDriver().')
				 
			filteredExpression = ''
			for i in range(int(variableTokensLen / 2)):
				# The inserted string literal below should remain consistent with the name of the dictionary of user-defined variables.
				filteredExpression += variableTokens[i * 2] + str(variables[variableTokens[(i * 2) + 1].strip()]) + ' '
			 
			# In case the for loop above didn't run
			if filteredExpression == '':
				filteredExpression = expression
				 
			print(f'Sending {filteredExpression} to calc.')
			variables['ans'] = calc(expression)
			print(variables['ans'])
		
		# Get input for next run.
		expression = input('==> ')

def graphicalDriver():
	'''Still a work in progress. Should appear as a window with a textbox where commands can be entered normally, but there are also clickable buttons.'''
	
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