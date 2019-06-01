# statistics.py
# This will hopefully be an extension to the main calculator program that specifically works with probabilities and statistics.

def main():
	print(eval(input('Enter expression below.')))

class ProbabilityDist():
	
	# To be overwritten by children.
	def probEQ(self, x):
		'''P(X = x).'''
		pass
	
	def probNE(self, x):
		'''P(X != x).'''
		return 1 - self.probEQ(x)
	
	def probLT(self, x):
		'''P(X < x).'''
		pass
	
	def probLE(self, x):
		'''P(X <= x).'''
		pass
	
	def probGT(self, x):
		'''P(X > x).'''
		pass
	
	def probGE(self, x):
		'''P(X >= x).'''
		pass
	
	def expectedValue(self):
		pass
	
	def variance(self):
		pass
	
	def __ne__(self, other):
		return not self == other

class DiscreteProbabilityDist(ProbabilityDist):
	'''Defines some equalities of inequalities so that children don't have to define both probLT() and probGE(), for example.'''
	def probGT(self, x):
		return 1 - self.probLE(x)
	
	def probGE(self, x):
		return 1 - self.probLT(x)

class ContinuousProbabilityDist(ProbabilityDist):
	'''Defines some equalities of inequalities so that children don't have to define both probLT() and probGE(), for example.'''
	def probLE(self, x):
		return self.probLT(x)
	
	def probGT(self, x):
		return 1 - self.probLT(x)
	
	def probGE(self, x):
		return self.GT(x)

class Bin(DiscreteProbabilityDist):
	'''Binomial distribution.'''
	
	def __init__(self, n, p):
		self.n = n
		self.p = p
		self.expectedValue = n * p
		self.variance = n * p * (1 - p)
	
	def probEQ(self, x):
		return (self.n choose x) * self.p**x * (1 - self.p)**(self.n - x)
	
	def probLT(self, x):
		sum = 0
		for i in range(x):
			sum += (self.n choose i) * self.p**i * (1 - self.p)**(self.n - i)
		
		return 
	
	def probLE(self, x):
		return
	
	# probNE defined in ProbabilityDist; probGT and probGE defined in DiscreteProbabilityDist.
	
	def expectedValue(self):
		return self.expectedValue
	
	def variance(self):
		return self.variance
	
	def clone(self):
		return Bin(self.n, self.p)
	
	def __format__(self):
		return f'X ~ Bin({self.n}, {self.p})'
	
	def __repr__(self):
		return f'Bin({self.n}, {self.p})'
	
	def __eq__(self, other):
		'''Only if they have identical n and p.'''
		return (self.n == other.n) and (self.p == other.p)
	
	# __ne__() defined in ProbabilityDist.
	
	def __lt__(self, other):
		'''Compares expected values.'''
		return self.expectedValue < other.expectedValue
	
	def __le__(self, other):
		'''Compares expected values.'''
		return self.expectedValue <= other.expectedValue
	
	def __gt__(self, other):
		'''Compares expected values.'''
		return not self <= other
	
	def __ge__(self, other):
		'''Compares expected values.'''
		return not self < other
	
	def __hash__(self):
		return (self.n, self.p).__hash__()

class Poisson(DiscreteProbabilityDist):
	'''Poisson probability distribution.'''
	def __init__(self, rate, length=1):
		self.rate = rate * length
		self.expectedValue = self.rate
		self.variance = self.rate
	
	def expectedValue(self):
		return self.expectedValue
	
	def variance(self):
		return self.variance