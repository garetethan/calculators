# collatz.py
# Written by Garet Robertson.
# Last updated 2017 August 31.
# This little program is designed to test Collatz Conjecture (https://en.wikipedia.org/wiki/Collatz_conjecture) for any given integer.

from sys import argv

def main():
    # check command line arguments
    if len(argv) != 2:
        print('Usage: python collatz.py n')
        exit(1)
    if int(argv[1]) < 1:
        print('Error: Input must be a positive (non-zero) integer.')
        exit(2)
    
    # send to recursive function
    hotpo(int(argv[1]), 0)
    exit(0)

def hotpo (n, steps):
    if n == 1:
        if steps == 1:
            print('1.\n1 step was required to solve.')
        else:
            print('1.\n{} steps were required to solve.'.format(steps))
        exit(0)
    else:
        print('{} → '.format(n), end = '')
        steps += 1;
        
        if n % 2 == 0:
            hotpo(int(n / 2), steps)
        else:
            hotpo(int(3 * n + 1), steps)

if __name__ == '__main__':
    main()