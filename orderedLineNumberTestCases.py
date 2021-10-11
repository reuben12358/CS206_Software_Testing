import os
import time
import random
from natsort import natsorted

uPathGen = "benchmarks/general/universe.txt"
statementCoveragePathGen = "benchmarks/general/statementCoverageLineNumbers"
branchCoveragePathGen = "benchmarks/general/branchCoverageLineNumbers"
statementLineNumberFileGen = "benchmarks/general/statementCoverageLineNumbers/lineNumbers.txt"
branchLineNumberFileGen = "benchmarks/general/branchCoverageLineNumbers/lineNumbers.txt"
listDirStatementGen = "benchmarks/general/statementCoverage"
listDirBranchGen = "benchmarks/general/branchCoverage"

def main():
    start = time.time()
    benchmarks = ['tcas', 'totinfo', 'schedule', 'schedule2', 'printtokens', 'printtokens2', 'replace']
    
    randomizedTestCases = []   # stores randomized test cases for benchmarks tcas -> replace
    totalTestCases = []
    additionalTestCases = []

    randomizedTestSuiteStatement = []
    randomizedTestSuiteBranch = []
    totalTestSuiteStatement = []
    totalTestSuiteBranch = []
    additionalTestSuiteStatement = []
    additionalTestSuiteBranch = []

    tempRandomizedTestSuiteStatement = []
    tempRandomizedTestSuiteBranch = []
    tempTotalTestSuiteStatement = []
    tempTotalTestSuiteBranch = []
    tempAdditionalTestSuiteStatement = []
    tempAdditionalTestSuiteBranch = []

    redundant = 0


    # get test cases for each prioritization method
    for benchmark in benchmarks:
        uPath = uPathGen.replace("general", benchmark)
        statementCoveragePath = statementCoveragePathGen.replace("general", benchmark)
        branchCoveragePath = branchCoveragePathGen.replace("general", benchmark)
        statementLineNumberFile = statementLineNumberFileGen.replace("general", benchmark)
        branchLineNumberFile = branchLineNumberFileGen.replace("general", benchmark)
        listDirStatement = listDirStatementGen.replace("general", benchmark)
        listDirBranch = listDirBranchGen.replace("general", benchmark)

        testCases = universe(uPath)

        # need to order line number file numerically (least to greatest)
        # so that it can correspond to correct test cases before being randomized together
        # right now the line number file starts with test case 1000
        orderedStatementLineNumberFile = orderCoverageFile(listDirStatement)
        orderedBranchLineNumberFile = orderCoverageFile(listDirBranch)

        orderedStatementLineNumberTestCases = dict()
        i = 0
        for line in orderedStatementLineNumberFile:
            orderedStatementLineNumberTestCases[line] = testCases[i]
            i = i + 1

        orderedBranchLineNumberTestCases = dict()
        i = 0
        for line in orderedBranchLineNumberFile:
            orderedBranchLineNumberTestCases[line] = testCases[i]
            i = i + 1

        # ------------------------------------------------------------------------------------------------------------------------------------------
        lineNumberFileTestCases = list(zip(orderedStatementLineNumberFile, testCases))   # so line number and test cases are randomized correspondingly
        
        randomizedTestCases = randomize(lineNumberFileTestCases)
        totalTestCases.append(total(lineNumberFileTestCases))   # not implemented yet
        additionalTestCases.append(additional(lineNumberFileTestCases))   # not implemented yet

        randomnizedGcovFiles, randomizedAssocTestCase = zip(*randomizedTestCases)

        randGcovFilesAssocTestCase = dict()
        i = 0
        while i < len(randomnizedGcovFiles):   # or len(randomizedAssocTestCase)
            randGcovFilesAssocTestCase[randomnizedGcovFiles[i]] = randomizedAssocTestCase[i]
            i = i + 1

        #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # coverage
        statementCoverage = parseCoverageFile(statementLineNumberFile)   # statement
        branchCoverage = parseCoverageFile(branchLineNumberFile)   # branch

        print("len(statementCoverage)")
        print(len(statementCoverage))
        print("len(randGcovFilesAssocTestCase)")
        print(len(randGcovFilesAssocTestCase))
        print("len(branchCoverage)")
        print(len(branchCoverage))

        # for key, value in statementCoverage.items():
        #     print(key, value)
        #     break

        # for key, value in branchCoverage.items():
        #     print(key, value)
        #     break

        # statement
        f= open(statementCoveragePath + "/2orderedStatementLineNumberTestCases.txt","w+")
        for key, values in orderedStatementLineNumberTestCases.items():
            f.write(key)
            f.write(": ")
            f.write(values)
            f.write(" : ")
            if ((listDirStatement + "/" + key) in statementCoverage.keys()):
                for value2 in statementCoverage[listDirStatement + "/" + key]:
                    f.write(value2)
                    f.write(", ")
            # elif (listDirStatement + "/" + key) not in statementCoverage.keys():
                # print("NOT IN: ")   # schedule2/statementCoverage/statementCoverage_191/198/892/908/1074/1290/2259_schedule2.c.gcov
                # print(listDirStatement + "/" + key)
            f.write("\n")
        f.close()


        # branch
        f= open(branchCoveragePath + "/2orderedBranchLineNumberTestCases.txt","w+")
        for key, values in orderedBranchLineNumberTestCases.items():
            f.write(key)
            f.write(": ")
            f.write(values)
            f.write(" : ")
            if ((listDirBranch + "/" + key) in branchCoverage.keys()):
                for value2 in branchCoverage[listDirBranch + "/" + key]:
                    f.write(value2)
                    f.write(", ")
            # elif (listDirBranch + "/" + key) not in branchCoverage.keys():
            #     print("NOT IN: ")   # schedule2/statementCoverage/statementCoverage_191/198/892/908/1074/1290/2259_schedule2.c.gcov
            #     print(listDirBranch + "/" + key)
            f.write("\n")
        f.close()
    

    return

def orderCoverageFile(listDir):
    arr = os.listdir(listDir)   # unordered list of files for coverage
    onlyGcov = []

    for file in arr:
        if "json" not in file:
            onlyGcov.append(file)


    sortedArr = natsorted(onlyGcov)   # sorted files from test case 1 -> max

    return sortedArr


def parseCoverageFile(file):
    coverage = dict()

    with open(file) as f:
        lines = f.readlines()

    for line in lines:
        fileName = line.partition(": ")[0]
        numbers = line.partition(": ")[2]
        numberList = []
        
        for number in numbers.split(', '):
            if (number != "\n"):   # avoid appending \n that is at the end of list of numbers
                numberList.append(number)

        # print("fileName")
        # print(fileName)
        # print("numberList")
        # print(numberList)

        coverage[fileName] = numberList   # add fileName and numberList to statement dict

        # break   # for testing only one line in the file

    return coverage

## prioritization methods ------------------------------------------------------------------
def randomize(testCases):
    # shuffledTestCases = sorted(testCases, key=lambda k: random.random())  # use sorted instead of random.shuffle() to avoid returning None
    random.shuffle(testCases)

    # return shuffledTestCases
    return testCases

def total(testCases):
    
    return

def additional(testCases):
    return

## universe.txt -------------------------------------------------------------------------------
def universe(file):
    with open(file) as f:
        testCases = f.readlines()
    
    return testCases

main()