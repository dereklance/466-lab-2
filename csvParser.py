import json, sys, os

def parse(filename):
	dataPoints = []
	with open(filename, 'r') as file:
		lines = file.read().strip().split(os.linesep)
		category = lines[2]
		variables = lines[0].split(',')
		
		for line in lines[3:]:
			row = line.split(',')
			dict = {}
			for index, variableName in enumerate(variables):
				if variableName == category:
					dict['Category'] = row[index]
				else:
					dict[variableName] = row[index]
			dataPoints.append(dict)
	return dataPoints

def main():
	print(json.dumps(parse(sys.argv[1]), indent=2))

if __name__ == '__main__':
	main()
