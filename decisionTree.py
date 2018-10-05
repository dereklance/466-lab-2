from TreeNode import Node
import csvParser, collections, math, sys
from itertools import groupby
from operator import itemgetter

def categoryCounts(data):
	categories = [dict['Category'] for dict in data]
	return dict(collections.Counter(categories))

def mostFrequentCategory(data):
	dict = categoryCounts(data)
	return max(dict.keys(), key=lambda key: dict[key])

def entropy(data):
	n = len(data)
	return -sum(count / n * math.log2(count / n) for count in categoryCounts(data).values())

def isUniform(list):
	return len(set(list)) <= 1

def groupByAttribute(data, attribute):
	attributeDict = {}
	for row in data:
		if row[attribute] not in attributeDict:
			attributeDict[row[attribute]] = []
		attributeDict[row[attribute]].append(row)
	return attributeDict

def selectSplittingAttribute(data, attributes, threshold):
	currentEntropy = entropy(data)
	bestAttribute = None
	maxGain = -1
	for attribute in attributes:
		if attribute == 'Category':
			continue
		attributeDict = groupByAttribute(data, attribute)
		entropyAfterSplit = sum(len(group) / len(data) * entropy(group) for group in attributeDict.values())
		informationGain = currentEntropy - entropyAfterSplit
		if informationGain > maxGain:
			maxGain = informationGain
			bestAttribute = attribute
	return bestAttribute if maxGain > threshold else None


# C4.5 Decision Tree Algorithm
def build(data, attributes, tree, threshold):
	if isUniform([dict['Category'] for dict in data]):
		print('uniform')
		tree = Node(data[0]['Category'], None)
	elif len(attributes) == 0:
		tree = Node(mostFrequentCategory(data), None)
	else:
		print('placehold')


def main():
	data = csvParser.parse(sys.argv[1])
	attributes = data[0].keys()
	x = selectSplittingAttribute(data, attributes, 0)
	print(x)

if __name__ == '__main__':
	main()