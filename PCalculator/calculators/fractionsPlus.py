'''
Created on Apr 13, 2018

@author: Garet
I starting building a Fraction object, but Python already has that. Of course Python alread has that.
But it did not have a mixed number object, so I built that.
'''

from fractions import Fraction, gcd

class MixedNumber:
    """An instance of this class represents a mixed number
    (https://en.wikipedia.org/wiki/Fraction_(mathematics)#Mixed_numbers) that
    contains two components, and integer and a Fraction."""
    
    def __init__ (self, whole = 0, fraction = Fraction(0, 1)):
        self._whole = int(whole)
        self._fraction = fraction
        self._simplify()
    
    def __add__ (self, other):
        """a + b"""
        return MixedNumber(self.whole + other.whole, self.fraction + other.fraction)
    
    def __sub__ (self, other):
        """a - b"""
        return MixedNumber(self.whole - other.whole, self.fraction - other.fraction)
    
    def __mul__ (self, other):
        """a * b"""
        # Convert self and other to (probably) improper fractions, multiply, and convert back.
        return MixedNumber(0, self.toFraction() * other.toFraction())
    
    def __truediv__ (self, other):
        """a / b"""
        return MixedNumber(0, self.toFraction() / other.toFraction())
    
    def __floordiv__ (self, other):
        """a // b"""
        return MixedNumber(0, self.toFraction() // other.toFraction())
    
    def __eq__ (self, other):
        """a = b"""
        return (self.whole == other.whole) and (self.fraction == other.fraction)
    
    def __lt__ (self, other):
        """a < b"""
        if self.whole != other.whole:
            return self.whole < other.whole
        else:
            return self.fraction < other.fraction
    
    def __le__ (self, other):
        """a <= b"""
        if self.whole != other.whole:
            return self.whole <= other.whole
        else:
            return self.fraction <= other.fraction
    
    def __gt__ (self, other):
        """a > b"""
        if self.whole != other.whole:
            return self.whole > other.whole
        else:
            return self.fraction > other.fraction
        
    def __ge__ (self, other):
        """a >= b"""
        if self.whole != other.whole:
            return self.whole >= other.whole
        else:
            return self.fraction >= other.fraction
        
    def __ne__ (self, other):
        """a != b"""
        return not (self == other)
    
    # Private because it should never need to be used outside this class.
    def _simplify (self):
        """Reduces Fraction (and increases whole number accordingly) if Fraction is improper.
        Fraction always keeps itself simplified."""
        # If whole and fraction have different signs
        if (self.whole < 0 and self.fraction > 0) or (self.whole > 0 and self.fraction < 0):
            # Combine whole and fraction parts into a (probably) improper fraction.
            self._fraction += self.whole
            self._whole = 0
        
        # If improper fraction
        if abs(self.fraction) > 1:
            fractionOverflow = int(self.fraction)
            # Purpusefully sneak by the automatic setters to avoid infinite recursion.
            self._whole += fractionOverflow
            self._fraction -= fractionOverflow
    
    def toFraction (self):
        """Converts a mixed number to a Fraction that is (probably) improper."""
        return self.whole + self.fraction
    
    def deepCopy (self):
        """Creates a new MixedNumber identical to self."""
        return MixedNumber(self.whole, self.fraction.__deepcopy__())
    
    def isNegative (self):
        """self < 0"""
        return (self.whole == 0) and (self.fraction == Fraction(0))
    
    def __float__ (self):
        """float(self)"""
        return self.whole + self.fraction
    
    def __repr__ (self):
        """repr(self), implemented as float(self)."""
        return float(self)
    
    def __str__ (self):
        """str(self)"""
        return str(self.whole) + ' ' + str(abs(self.fraction))
    
    @property
    def whole (self):
        """Returns the whole number part of self."""
        return self._whole
    
    @whole.setter
    def whole (self, whole):
        """Sets the whole number part of self."""
        self._whole = whole
        self._simplify()
    
    @property
    def fraction(self):
        """Returns the Fraction part of self."""
        return self._fraction
    
    @fraction.setter
    def fraction(self, fraction):
        """Sets the fraction part of self."""
        self._fraction = fraction
        self._simplify()
    
    @classmethod
    def lcm (cls, a, b):
        """Returns least common multiple of two ints."""
        return (a * b) / gcd(a, b)
    
def demo():
    f0 = Fraction(3, -14)
    f1 = Fraction(4, 7)
    mN0 = MixedNumber(4, f0)
    mN1 = MixedNumber(10, f1)
    print(f'The sum of {mN0} and {mN1} is {mN0 + mN1}.')
    print(f'The difference between {mN0} and {mN1} is {mN0 - mN1}.')
    print(f'The produce of {mN0} and {mN1} is {mN0 * mN1}.')
    print(f'The quotient of {mN0} divided by {mN1} is {mN0 / mN1}.')
    print(f'The remainder of the above division is {mN0 // mN1}.')
    print(f'Is {mN0} less than or equal to {mN1}? {mN0 <= mN1}.')
    print(f'Is {mN0} greater than {mN1}? {mN0 > mN1}.')

if __name__ == '__main__':
    demo()