'''
Created on Mar 8, 2018

@author: Garet
'''
import string

def main():
    num = changeBase('A3.557B75', 12, 10)
    print(f'{num}')
    
def changeBase(num, oldBase, newBase, precision=10):
    # TODO.
    # Convert num to an array of its digits, convert to base ten by multipying
    # each digit by oldBase^index, then convert to newBase using // and %.
    
    # From oldBase
    whole, _, fractional = num.strip().partition('.')
    num = int(whole + fractional, oldBase) * oldBase ** -len(fractional)

    # To newBase
    if newBase != 10:
        s = intToBase(int(round(num / newBase ** -precision)), newBase)
        if precision:
            return s[:-precision] + '.' + s[-precision:]
        else:
            return s
    else:
        return num

# ALL uses of '+' below are concatenation and not addition.
def intToBase(number, new_base):
    # Define list of symbols used as digits
    symbols = string.digits + string.ascii_uppercase
    
    # Uses "the division method"
    isNeg = number < 0
    number = abs(number)
    ans = ''
    while number:
        ans = symbols[number % new_base] + ans
        number //= new_base
    if isNeg:
        ans = '-' + ans
    return ans

if __name__ == '__main__':
    main()