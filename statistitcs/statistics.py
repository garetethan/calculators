# statistics.py
# I am writing this to check that I understand the equation for the correlation coefficient correctly, and also so that I can check my answers to certain statistics problems where no answer is provided.

from math import sqrt

HELP = 'To save a new dataset, use save(name).\n'
	+ 'Supported functions include mean(x), variance(dataset), st(sataset) (sample standard deviation), and correlation(dataset0, dataset1)'
def main():
	while True:
		print(eval(input('==> ')))
	print('How many variables do you have?')
	variableNum = int(input('==> '))
	if variableNum == 1:
		print('Enter the data on one line as real numbers separated by spaces.')
		x = [float(i) for i in input('==> ').split()]
	elif variableNum == 2:
		print('Enter the data for the first variable on one line separated by spaces.')
		x = [float(i) for i in input('==> ').split()]
		print('Enter the data for the second variable similarly.')
		y = [float(j) for j in input('==> ').split()]
	elif variableNum > 2:
		print('Sorry, that is not supported.')
		return
	# variableNum < 1
	else:
		print('Yo, you have no data. Go get some data.')

def help():
	print(HELP)
def mean(data):
	return sum(data) / len(data)
# SAMPLE variance.
def variance(data):
	return (sum([x ** 2 for x in data]) - len(data) * (mean(data) ** 2)) / (len(data) - 1)
# SAMPLE standard deviation.
def sd(data):
	return sqrt(variance(data))

def correlation(data0, data1):
	data0Mean = mean(data0)
	data1Mean = mean(data1)
	if len(data0) != len(data1):
		print(f'The datasets given are of different lengths ({len(data0)} and {len(data1)}).')
	numer = [x * y for (x, y) in (data0, data1)] - len(data0) * data0Mean * data1Mean
	denom = sqrt((sum([x ** 2 for x in data0]) - len(data0) * data0Mean ** 2) * (sum([y ** 2 for y in data1]) - len(data1) * data1Mean ** 2))
	return numer / denom

if __name__ == '__main__':
	main()