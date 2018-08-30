'''
Created on Mar 8, 2018

@author: Garet
'''
import string

def main():
    strInputs = input('Enter the number, the old base, and the new base.\n').split()
    while strInputs[0] != 'quit':
        num = changeBase(strInputs[0], int(strInputs[1]), int(strInputs[2]))
        print(f'{num}')
        strInputs = input('Enter the number, the old base, and the new base.\n').split()
    
def changeBase(num, oldBase, newBase, precision=10):
    
    # From oldBase
    whole, _, fractional = num.strip().partition('.')
    num = int(whole + fractional, oldBase) * oldBase ** -len(fractional)

    # To newBase
    if num % 1 == 0:
        return intToBase(num, newBase)
    
    if newBase != 10:
        s = intToBase(int(round(num / newBase ** -precision)), newBase)
        if precision:
            return s[:-precision] + '.' + s[-precision:]
        else:
            return s
    else:
        return num

# ALL uses of '+' below are concatenation and not addition.
def intToBase(number, newBase):
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
    return ans

if __name__ == '__main__':
    main()