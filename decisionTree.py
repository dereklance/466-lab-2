from TreeNode import Node
import math
import csvParser, collections

def categoryCounts(data):
	categories = [dict['Category'] for dict in data]
	return collections.Counter(categories)

def mostFrequentCategory(data):
	dict = categoryCounts(data)
	return max(dict.keys(), key=lambda key: dict[key])

def entropy(data):
	n = len(data)
	counts = [count / n * math.log2(count / n)
		for count in categoryCounts(data).values()]
	return -sum(counts)

def isUniform(list):
	return len(set(list)) <= 1

# def selectSplittingAttribute(data, attributes, threshold):
# 	entropy = entropy(data)
# 	for attribute in attributes:


# C4.5 Decision Tree Algorithm
def build(data, attributes, tree, threshold):
	if isUniform([dict['Category'] for dict in data]):
		print('uniform')
		tree = Node(data[0]['Category'], None)
	elif len(attributes) == 0:
		tree = Node(mostFrequentCategory(data), None)
	else:
		


def main():
	data = csvParser.parse('tree03-20-words.csv')

if __name__ == '__main__':
	main()