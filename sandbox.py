import math

DISALLOWED_VAR_NAMES = [i for i in dir(math) if i[0] != r'_']
print(DISALLOWED_VAR_NAMES)