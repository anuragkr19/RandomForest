# -*- coding: utf-8 -*-
"""
External Reference:-

https://github.com/random-forests/tutorials/blob/master/decision_tree.ipynb
https://www.youtube.com/watch?v=LDRbO9a6XPU&t=517s
https://en.wikipedia.org/wiki/Predictive_analytics#Classification_and_regression_trees_.28CART.29
https://machinelearningmastery.com/implement-random-forest-scratch-python/
http://ciml.info/dl/v0_99/ciml-v0_99-ch13.pdf
https://archive.ics.uci.edu/ml/datasets/Iris
"""

import csv
import os
import math
import random as rd
import numpy as np
from sys import argv
import operator
 

header = ['sepal length','sepal width','petal length','petal width']

#class used to split dataset based on the answer to the question into true and false branch
class Node:
    
    def __init__(self,question,true_branch,false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch


#Return no of classcount at the leaf level
class Leaf:
    
    def __init__(self, rows):
        self.classCount = class_counts(rows)


#Question for partitioning the dataset
class Question:

    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        # Compare the feature value in an example to the
        # feature value in this question.
        val = example[self.column]
        return val == self.value

    def __repr__(self):
        # This is just a helper method to print
        # the question in a readable format.
        condition = "=="
        return "Is %s %s %d?" % (header[self.column], condition, int(self.value))


#count the number of rows for each class type and return the result in a dictionary type object
def class_counts(rows):
    counts = {}
    for row in rows:
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] +=1
    return counts

#return list with unique values for a particular column
def getListForCol(dataSet,col):
    
    listTemp = []
    
    for i in range(len(dataSet)):
        listTemp.append(dataSet[i][col])
    
    return set(listTemp)

#fetch training dataset from csv file
def loadTrainingData():
    dataPoints = []
    fileh = open(os.getcwd() + "//iris_train.csv",'r')
    try:
        csv_reader = csv.reader(fileh,delimiter=',')
        for row in csv_reader:
            tempList = []
            tempList.append(row[0]) # sepal length
            tempList.append(row[1]) # sepal width
            tempList.append(row[2]) # petal length
            tempList.append(row[3]) # petal width
            if row[4] == 'Iris-setosa':
                class_name = 0
            elif row[4] == 'Iris-versicolor':
                class_name = 1
            else:
                class_name = 2
            tempList.append(class_name) # class
            dataPoints.append(tempList)
    except:
        pass
    fileh.close()
    return dataPoints

#fetch test dataset from csv file
def loadTestData():
    dataPoints = []
    fileh = open(os.getcwd() + "//iris_test.csv",'r')
    try:
        csv_reader = csv.reader(fileh,delimiter=',')
        for row in csv_reader:
            tempList = []
            tempList.append(row[0]) # sepal length
            tempList.append(row[1]) # sepal width
            tempList.append(row[2]) # petal length
            tempList.append(row[3]) # petal width
            if row[4] == 'Iris-setosa':
                class_name = 0
            elif row[4] == 'Iris-versicolor':
                class_name = 1
            else:
                class_name = 2
            tempList.append(class_name) # class
            dataPoints.append(tempList)
    except:
        pass
    fileh.close()
    return dataPoints

#return the question
def getQuestion(colDict,colName,value):
    condition = "=="
    return "%s %s %d?" %(colDict[colName],condition,value) 

#partition dataset based on question into two lisst true_rows,false_rows
def partitionDataSet(dataset,question):
    
    true_rows,false_rows = [],[]
    for row in dataset:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    
    return true_rows,false_rows

#calculate entropy of the dataset
def calculateEntropy(dataSet):
    counts = class_counts(dataSet)
    impurity = 0.0
    probl_of_lbl = 0.0
    try:
        for lbl in counts:
            probl_of_lbl = (counts[lbl]) / float(len(dataSet))
            impurity += ((probl_of_lbl * - (math.log(2,probl_of_lbl))))
    except:
        pass
    return impurity

#calculate info_gain 
def info_gain(left,right,parent_entropy):
    n = len(left) + len(right)
    p_left = len(left)/n
    p_right = len(right)/n
    return (parent_entropy - ((p_left * calculateEntropy(left)) - (p_right) * calculateEntropy(right)))

#returning the best split and best info_gain
def findBestSplit(colDict,dataSet):
    best_gain = 0
    best_ques = None
    parent_entropy = calculateEntropy(dataSet)
    
    #no of features to be considered for split is square root of the total number of input features
    n_features = int(math.sqrt(len(dataSet[0])-1))
    gain = 0.0
    features = list()
    
    #randomly selecting sub set of features and finding best feature to split on data.
    while len(features) < n_features:
        index = rd.randrange(len(dataSet[0])-1)
        if index not in features:
            features.append(index)

    for index in features:
        #get unique values for column in list
        uniqueListForCol = getListForCol(dataSet,index)
        for value in uniqueListForCol:
            #get question for each value in the uniqueList
            question = Question(index,value)
            
            #split the dataset
            true_rows,false_rows = partitionDataSet(dataSet,question)
            
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue
            
            #calculate information gain from this split
            gain = info_gain(true_rows, false_rows, parent_entropy)
            
            #selecting the best gain and best question
            if gain >= best_gain:
                best_gain = gain
                best_ques = question
                
                
    return best_gain,best_ques
    
#printing decision tree
def print_decision_Tree(node,spacing = " "):
    
    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        print (spacing + "Predict", node.classCount)
        return
    
    #Print the question at this node
    print(spacing + str(node.question))
    
    # Call this function recursively on the true branch
    print(spacing + '--> True: ')
    print_decision_Tree(node.true_branch , spacing + "  ")
    
    # Call this function recursively on the false branch
    print(spacing + '--> False: ')
    print_decision_Tree(node.false_branch, spacing + " ")

    
#Build decision tree with dataSet,colDict is a dictionary which consists of key = col_index,value = column_name 
def build_decision_Tree(dataSet,colDict,maxDepth,depth):
    
    gain, question = findBestSplit(colDict,dataSet)
        
    if gain == 0:
        return Leaf(dataSet)
    
    if(depth >= maxDepth):
        return Leaf(dataSet)
    
    true_rows, false_rows = partitionDataSet(dataSet,question)

    # Recursively build the true branch.
    true_branch = build_decision_Tree(true_rows,colDict,maxDepth,depth + 1)

    # Recursively build the false branch.
    false_branch = build_decision_Tree(false_rows,colDict,maxDepth,depth + 1)
    
    return Node(question,true_branch,false_branch)
       
#classify the record on the node if the row satisfy condition asked in the form of question at this node
def classify(row, node):
   
    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        return node.classCount

    # Decide whether to follow the true-branch or the false-branch.
    # Compare the feature / value stored in the node,
    # to the example we're considering.
    
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch) 
    

#getting bootstrap sample of data
def bootstrap_sample(data):
    resultList = []
    randomRows = np.random.randint(len(data),size=len(data))
    for i in randomRows:
        resultList.append(data[i])
    return resultList


def findHeightHelper(node):
    if isinstance(node, Leaf):
        return 1
    
    leftPart = findHeightHelper(node.true_branch)
    rightPart = findHeightHelper(node.false_branch)
    return 1 + max(leftPart,rightPart)
    
def print_leaf(counts):
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = (int(counts[lbl] / total * 100))
    
    return probs


def main(*args):
    
    #fetching training data from csv file in the trainData list
    trainData = loadTrainingData()
    #fetching test data from csv file in the testData list
    testData = loadTestData()
    
    colDict= {}
    colDict[0] = "sepal length"
    colDict[1] = "sepal width"
    colDict[2] = "petal length"
    colDict[3] = "petal width"
    
    count_no_trees = int(input("Please enter no of trees to generate "))
    list_tress = [] * count_no_trees
    result = 0
    count = 0
    
    

    #generate each tree with depth 10
    while count_no_trees > 0:
        #getting bootstrap sample
        bootstrapTrainData = bootstrap_sample(trainData)
        tree = build_decision_Tree(bootstrapTrainData,colDict,30,1)
        count = 0
        #adding learned decision tree in the set
        list_tress.append(tree)
        count_no_trees-=1
    
    
    count = 0
    
    #doing prediction on test dataset from learned random forest
    print('Performing prediction on test data ')
    print(' ')
    
    
    #for each data item of testData getting predictions from different 
    # learned decision tree classifier
    for row in testData:
        result = [print_leaf(classify(row, tree)) for tree in list_tress]
        class_types = {}
        for i in range(len(result)):
            dict_result = result[i]
            
            maxLabel = max(dict_result, key=lambda k: dict_result[k])
            if maxLabel not in class_types:
                class_types[maxLabel] = 1
            else:
                val = class_types[maxLabel]
                class_types[maxLabel] = val + 1

        #getting class label with maximum vote
        finalLabel = max(class_types.items(), key=operator.itemgetter(1))[0]
        
        for key,val in class_types.items():
            if row[-1] == finalLabel:
                count+=1
                break
                
        print('Actual {0} predicted {1}'.format(row[-1],finalLabel))
            
    print('Accuracy for Test Data ' + str((count/len(testData))*100) + ' %')

main(*argv[0:])
    
        