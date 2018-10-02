/**
 * collatz.c
 * 
 * Created by Garet Robertson.
 * Last updated on 2016 June 27.
 * 
 * This little program is designed to test Collatz Conjecture (https://en.wikipedia.org/wiki/Collatz_conjecture) for any given integer.
 * The hotpo (an initialism of "half or triple plus one") function recursively checks the value of the integer, keeping track of how it changes it using printf().
 * If it is even, then it divides it by two.
 * If it is odd, then it multiplies it by three, then adds one.
 * Unless it is one, in which case its job is done and it returns.
 * The Collatz conjecture states that performing this operation continuously will always lead to the number one.
 * (When the operations are performed on the number one, it simply loops back to itself.)
 */

#include <stdio.h>
#include <stdlib.h>

int steps = 0;

int hotpo (int n);

int main (int argc, char* argv[])
{
    // check number of arguments given
    if (argc != 2) {
        printf("Usage: ./collatz n\n");
        return 1;
    }
    
    int n = (int) strtol(argv[1], (char**) NULL, 10);
    
    return hotpo(n);
}

int hotpo (int n)
{
    if (n < 1) {
        printf("Error: Negative number or zero given.\n");
        printf("Because of the nature of the Collatz conjecture, this program has been designed to work only on positive integers (excluding zero).\n");
        printf("If you use the same formula on zero or negative numbers, it often encounters infinite loops (that this program does not properly deal with).\n");
        printf("If you entered a fraction or decimal, note that this program automatically chops off anything after a full stop or a backslash.\n");
        printf("For this reason, inputs such as '0.9/1', '0.97', and '0.04 * 6' will all be rendered as zero.\n");
        return 1;
    }
    else if (n == 1) {
        printf("1.\nTotal steps required to solve: %i.\n", steps);
        return 0;
    }
    else {
        printf("%i → ", n);
        steps++;
        
        if (n % 2 == 0) {
            return hotpo(n / 2);
        }
        else {
            return hotpo((3 * n) + 1);
        }
    }
}