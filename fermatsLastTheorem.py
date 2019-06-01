# Verifies Fermat's Last Theorem
MIN = -1000
MAX = abs(MIN)
EXP = 5

basesToCheck = list(range(MIN, MAX))
basesToCheck.remove(0)

def main():
	for i in basesToCheck:
		if i % 50 == 0:
			print(f'Checking x = {i}...')
		for j in basesToCheck:
			if isPerfectPower(i**EXP + j**EXP):
				print(f'Solution: {i}^{EXP} - {j}^{EXP} = {properRoot(i**EXP + j**EXP)}^{EXP}')

# Copied from <https://stackoverflow.com/a/28014277/5231183> and then modified.
def isPerfectPower(x):
	return properRoot(x) ** EXP == x and x != 0

def properRoot(x):
	return int(round((x ** (1. / EXP)).real))

if __name__ == '__main__':
	main()
