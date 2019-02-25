'''
Tests for the calculator.py program.
'''

from unittest import TestCase
from calculator import *
from math import pi
from decimal import *

PI_ON_SIX = Decimal(pi / 6)

class TestArithmetic(TestCase):
	def testAddition(self):
		self.assertEqual(calc('-7 + 13'), Decimal('6'))
	
	def testDivision(self):
		self.assertEqual(calc('1 / -10'), Decimal('-0.1'))
		# Test precision.
		self.assertEqual(calc('(1 / 3) * 3'), Decimal('1'))