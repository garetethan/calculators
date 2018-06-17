'''
Created on Mar 8, 2018

@author: Garet
'''
import re

expression = 'sind(asind(40))'
print(re.split(r'([a-zA-z]+[^(]|[a-zA-z]+$)', expression))
print(re.split(r'(A[^R]|A$)', 'ABCDEFARGHA'))