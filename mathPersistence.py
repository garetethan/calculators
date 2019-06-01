# https://www.youtube.com/watch?v=Wim9WJeDTHQ

def main():
	i = 2800000
	while True:
		if i % 100000 == 0:
			print(f'Checking {i}...')
		per = persistence(i)
		if per > 8:
			print(f'{i} has a persistence of {per}.')
		i += 1

def persistence(n, steps=0, output=''):
	if len(str(n)) == 1:
		return steps + 1
	else:
		digits = [int(d) for d in str(n)]
		product = 1
		for d in digits:
			product *= d
		return persistence(product, steps + 1)

if __name__ == '__main__':
	main()
