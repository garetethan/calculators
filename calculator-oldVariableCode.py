'''
The old code that I was using to try to let the user save variables with custom names.
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
