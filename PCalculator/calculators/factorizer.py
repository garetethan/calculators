'''
Created on Mar 2, 2018

@author: Garet
'''
# I want to be able to find all of the factors of any (relatively low) integer.
# I would incorporate this into calculator, but because it takes one number and returns several, it does not fit into the calc() method (which is recursive) at all.
# primes.txt contains a list of the first prime numbers.

from math import sqrt
from re import match
from time import time

def main():
    start = time()
    print(f'Choose one of the options below by entering its corresponding number.')
    print('0. Find all of the factors of an integer.')
    print('1. Find all the prime factors of an integer.')
    print('2. Determine whether an integer is prime.')
    choice = input('==> ')
    while not match('\\d', choice):
        print(f'Invalid input. Please enter a choice below.\n')
        choice = input('==> ')
    print('Enter the number to process.')
    num = input('==> ')
    if choice in choices:
        print(choices[choice](num))
    end = time()
    print(f'Ran in {round(end - start, 4)} seconds.')
    

def factorize(product):
    smallFactors = [1]
    bigFactors = [product]
    
    # Because we find two factors at a time, we only have to check up to the square root.
    for i in range(2, int(sqrt(product))):
        if product % i == 0:
            # Add to end.
            smallFactors.append(i)
            # Add to beginning (puts all factors in ascending order at the end).
            bigFactors.insert(0, int(product / i))
    return smallFactors + bigFactors

# def primeFactorize(num):

# I just wanted to put this here since it doesn't belong anywhere else.
def isPrime(num):
    for i in range(2, int(sqrt(num))):
        if num % i == 0:
            return False
    return True

# Used by main as a menu selection
# choices = {
#     '0': facorize,
#     '1': primeFactorize,
#     '2': isPrime
# }

if __name__ == '__main__':
    main()