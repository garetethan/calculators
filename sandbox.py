import math
from re import sub
from decimal import Decimal

expression = input('==> ')
expression = sub(r'(-?[\d\.]+)', r'Decimal(\1)', expression)
expression = sub(r'\|(.*?)\|', r'abs(\1)', expression)
print(f'[DEBUG] After substitution:\n{expression}')
print(f'[DEBUG] After eval:\n{eval(expression)}')