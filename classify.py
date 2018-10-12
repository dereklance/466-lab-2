import decisionTree as dt
import csvParser
import sys
import copy
from TreeNode import Node

# Takes a decision tree and a data point to classify and returns
# the predicted class label
def classifyPoint(tree, dataPoint):
    while tree.children:
        category = tree.name
        for child in tree.children:
            if dataPoint[category] == child.label:
                tree = child

    return tree.name

# Takes a decision tree and a collection of data to classify and returns
# a list of tuples where each tuple is of the form:
#               (dataPoint (dict), classLabel (string))
def classifyCollection(tree, data):
    classification = []

    for dataPoint in data:
        classLbl = classifyPoint(tree, dataPoint)
        pointClassif = (dataPoint, classLbl)
        classification.append(pointClassif)

    return classification

def isTrainingSet(data):
    return ('Category' in data[1].keys())

def removeClassLabels(data):
    dc = copy.deepcopy(data)
    for d in dc:
        d.pop("Category")
    return dc

def main():
    if not len(sys.argv) == 3:
        print("\t\tMissing arguments\n\tProper Call :\tpython classify.py <CSVFile> <XMLFile>")
        return

    dataFile = sys.argv[1]
    dTreeFile = sys.argv[2]

    data = csvParser.parse(dataFile)
    dataB = csvParser.parse("C:/Users/Ian/Documents/CSC466/Lab02/trunk/tree03-100-words.csv")
    attributes = list(data[0].keys())

    # Replace this with converting the xml file to tree
    root = Node('Root', None)
    dt.build(dataB, attributes, root, 0.01)

    if (isTrainingSet(data)):
        print("\n\tTraining set detected as input, ignoring actual classes " + "during classification")

        actualClasses = []
        for dataPoint in data:
            actualClasses.append(dataPoint['Category'])
        dataC = removeClassLabels(data)

    else:
        dataC = data

    classes = classifyCollection(root, dataC)


    print("Print mode : [V]erbose [S]hort\t",end="")
    printMode = input()
    while not printMode.lower() == "v" and not printMode.lower() == "s":
        print("entered: |{}|".format(printMode))
        print("Please enter V for verbose printing or S for a shorter output")
        printMode = input()

    # Add different print options for if the csv file was a training dataset or
    # not
    if printMode.lower() == "v":
        for classif in classes:
            print("\nDatapoint :")
            for key, val in classif[0].items():
                print("\t{} : {}".format(key, val))
            print("\tClassification for datapoint\t:\t{}".format(classif[1]))
    else:
        for i, classif in enumerate(classes):
            print("\tClassification for datapoint #{}\t:\t{}".format(i+1, classif[1]))

    if (isTrainingSet(data)):
        numErr = 0
        tot = 0
        for i, classif in enumerate(classes):
            if not classif[1] == actualClasses[i]:
                print("Record {} classified as {}, actual class {}".format(i, actualClasses[i], classif[1]))
                numErr += 1
            tot = i + 1
        print("\nTotal records classified:\t\t{}".format(tot))
        print("# records correctly classified:\t\t{}".format(tot - numErr))
        print("# records incorrectly classified:\t{}".format(numErr))
        print("Accuracy:\t{}%".format(((tot - numErr) / tot) * 100))
        print("Error rate:\t{}%".format(numErr - tot))




if __name__ == '__main__':
	main()
