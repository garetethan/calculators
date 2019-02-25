class TestTrig(CalcTest):
	
	# Missing trig functions and their arcs.
	def testSec(self):
		self.assertAreClose(sec(pi / 6), Decimal(2 / sqrt(3)))
	
	def testCsc(self):
		self.assertAreClose(csc(pi / 6), Decimal(2))
	
	def testCot(self):
		self.assertAreClose(cot(pi / 6), Decimal(sqrt(3)))
	
	def testAsec(self):
		self.assertAreClose(asec(2 / sqrt(3)), Decimal(pi / 6))
	
	def testAcsc(self):
		self.assertAreClose(acsc(2), Decimal(pi / 6))
	
	def testAcot(self):
		self.assertAreClose(acot(sqrt(3)), Decimal(pi / 6))
	
	# All trig functions for use with degrees.
	def testSind(self):
		self.assertAreClose(sind(30), Decimal(0.5))
	
	def testCosd(self):
		self.assertAreClose(cosd(30), Decimal(sqrt(3) / 2))
	
	def testTand(self):
		self.assertAreClose(tand(30), Decimal(1 / sqrt(3)))
	
	def testSecd(self):
		self.assertAreClose(secd(30), Decimal(2 / sqrt(3)))
	
	def testCscd(self):
		self.assertAreClose(cscd(30), Decimal(2))
	
	def testCotd(self):
		self.assertAreClose(cotd(30), Decimal(sqrt(3)))
	
	def testAsind(self):
		self.assertAreClose(asind(0.5), 30)
	
	def testAcosd(self):
		self.assertAreClose(acosd(sqrt(3) / 2), 30)
	
	def testAtand(self):
		self.assertAreClose(atand(1 / sqrt(3)), 30)
	
	def testAsecd(self):
		self.assertAreClose(asecd(2 / sqrt(3)), 30)
	
	def testAcscd(self):
		self.assertAreClose(acscd(2), 30)
	
	def testAcotd(self):
		self.assertAreClose(acotd(sqrt(3)), 30)

class TestSquareCube(CalcTest):
	'''Tests sq(), cb(), sqrt(), and cbrt().'''
	
	def testSq(self):
		self.assertAreClose(sq(-5), 25)
	
	def testSqrt(self):
		self.assertAreClose(sqrt(25), 5)
		# Negative numbers are absolute-valued.
		self.assertAreClose(sqrt(-25), 5)
	
	def testCb(self):
		self.assertAreClose(cb(-5), -125)
	
	def testCbrt(self):
		self.assertAreClose(cbrt(-125), 5)

class TestQuadratic(CalcTest):
	'''Tests quadraticA() and quadraticS().'''
	pass