from TreeNode import Node
import csvParser, collections, math, sys
from itertools import groupby
from operator import itemgetter
from lxml import etree

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

def printTree(root):
	print("")
	print("\t( Node: {})\tLabel: {}".format(root.name, root.label))
	print("Children:\nLabels:",end="")
	for child in root.children:
		print("\t|{} |".format(child.label), end="")
	print("\n")
	for child in root.children:
		print("\t|{} |".format(child.name), end="")
	print("\n==============================================================")
	for child in root.children:
		printTree(child)


# Decision nodes not done, haven't checked correctness of nesting on output
def outputXML(root):
	#tree = etree.Element("Tree", name="Decision Tree")
	rootNode = etree.Element("node", var="{}".format(root.name))
	for child in root.children:
		edge = etree.Element("edge", var="{}".format(child.label))
		rootNode.append(edge)
		childNode = outputXML(child)
		edge.append(childNode)

	return rootNode



# Takes a list of dictionaries as data and an attribute
# and returns a dictionary where each key is a value in
# the domain of attribute and the values are all data
# points that have that value in them
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
	#print("\n\n")
	for attribute in attributes:
		if attribute == 'Category':
			continue
		attributeDict = groupByAttribute(data, attribute)
		entropyAfterSplit = sum(len(group) / len(data) * entropy(group) for group in attributeDict.values())
		informationGain = currentEntropy - entropyAfterSplit
		#print("Information Gain for {}:\t{}".format(attribute, informationGain))
		if informationGain > maxGain:
			maxGain = informationGain
			bestAttribute = attribute
	return bestAttribute if maxGain > threshold else None


# C4.5 Decision Tree Algorithm
def build(data, attributes, tree, threshold):
	if isUniform(dict['Category'] for dict in data):
		tree.setName(data[0]['Category'])
	elif len(attributes) == 0:
		tree.setName(mostFrequentCategory(data), None)
	else:		# Select splitting attribute
		bestAttribute = selectSplittingAttribute(data, attributes, threshold)
		if not bestAttribute:
			tree.setName(mostFrequentCategory(data))
		else:
			tree.setName(bestAttribute)
			attributeDict = groupByAttribute(data, bestAttribute)
			for attributeName in attributeDict.keys():
				newData = attributeDict[attributeName]
				if len(newData) > 0:
					newAttributes = list(attributes)
					newAttributes.remove(bestAttribute)
					childNode = Node(None, attributeName)
					tree.addChild(childNode)
					build(newData, newAttributes, childNode, threshold)

def main():
	# CHANGED TO READ FROM SPECIFIC FILE NOT ARGV[1]
	data = csvParser.parse("trunk/tree03-100-words.csv")
	attributes = list(data[0].keys())
	root = Node('Root', None)
	build(data, attributes, root, 0.01)
	s = etree.tostring(outputXML(root), pretty_print=True, encoding='unicode')
	print(s)



if __name__ == '__main__':
	main()
