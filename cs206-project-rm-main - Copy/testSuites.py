import os
import time
import random
from operator import itemgetter

statementCoveragePathGen = "benchmarks/general/statementCoverageLineNumbers"
branchCoveragePathGen = "benchmarks/general/branchCoverageLineNumbers"



def main():
    start = time.time()
    # benchmarks = ['tcas']
    # benchmarks = ['totinfo', 'schedule', 'schedule2', 'printtokens', 'printtokens2', 'replace']
    benchmarks = ['tcas', 'totinfo', 'schedule', 'schedule2', 'printtokens', 'printtokens2', 'replace']
    
    for benchmark in benchmarks:
        # print("benchmark")
        # print(benchmark)
        statementCoveragePath = statementCoveragePathGen.replace("general", benchmark)
        branchCoveragePath = branchCoveragePathGen.replace("general", benchmark)

        # statement ---------------------------------------------------------------------------
        with open(statementCoveragePath + "/2orderedStatementLineNumberTestCases.txt") as f:
            orderedStatementLines = f.readlines()

        orderedStatementList = filenameTestcaseCoverage(orderedStatementLines)

        origOrderedStatementList1 = orderedStatementList.copy()
        origOrderedStatementList2 = orderedStatementList.copy()
        origOrderedStatementList3 = orderedStatementList.copy()

        randomizedStatementTestSuite = randomizeStatement(origOrderedStatementList1)
        totalStatementTestSuite = totalStatement(origOrderedStatementList2)
        additionalStatementTestSuite = additionalStatement(origOrderedStatementList3)

        # branch---------------------------------------------------------------------------------
        with open(branchCoveragePath + "/2orderedBranchLineNumberTestCases.txt") as f:
            orderedBranchLines = f.readlines()

        orderedBranchList = filenameTestcaseCoverage(orderedBranchLines)

        origBranchStatementList1 = orderedBranchList.copy()
        origBranchStatementList2 = orderedBranchList.copy()
        origBranchStatementList3 = orderedBranchList.copy()

        randomizedBranchTestSuite = randomizeBranch(origBranchStatementList1)
        totalBranchTestSuite = totalBranch(origBranchStatementList2)
        additionalBranchTestSuite = additionalBranch(origBranchStatementList3)


        # write to statement files-----------------------------------------------------------------
        f = open(statementCoveragePath + "/randomizedStatementTestSuite.txt","w+")
        for key, values in randomizedStatementTestSuite:
            f.write(key)
            f.write(": ")
            f.write(values)
            f.write("\n")
        f = open(statementCoveragePath + "/totalStatementTestSuite.txt","w+")
        for key, values in totalStatementTestSuite:
            f.write(key)
            f.write(": ")
            f.write(values)
            f.write("\n")
        f = open(statementCoveragePath + "/additionalStatementTestSuite.txt","w+")
        for key, values in additionalStatementTestSuite:
            f.write(key)
            f.write(": ")
            f.write(values)
            f.write("\n")

        # write to branch files-----------------------------------------------------------------
        f = open(branchCoveragePath + "/randomizedBranchTestSuite.txt","w+")
        for key, values in randomizedBranchTestSuite:
            f.write(key)
            f.write(": ")
            f.write(values)
            f.write("\n")
        f = open(branchCoveragePath + "/totalBranchTestSuite.txt","w+")
        for key, values in totalBranchTestSuite:
            f.write(key)
            f.write(": ")
            f.write(values)
            f.write("\n")
        f = open(branchCoveragePath + "/additionalBranchTestSuite.txt","w+")
        for key, values in additionalBranchTestSuite:
            f.write(key)
            f.write(": ")
            f.write(values)
            f.write("\n")

    return

# STATEMENT TEST PRIORITIZATIONS
def totalStatement(orderedList):
    testSuite = []

    fileName, testCase, coverage = zip(*orderedList)
    coverageSize = []
    for item in coverage:
        coverageSize.append(len(item))

    fileNameTestCaseCoverageAndSize = list(zip(fileName, testCase, coverage, coverageSize))
    sortedFileNameTestCaseCoverageAndSize = sorted(fileNameTestCaseCoverageAndSize, key=itemgetter(3))
    fileName, testCase, coverage, coverageSize = zip(*sortedFileNameTestCaseCoverageAndSize) # coverage size not needed anymore; only needed it for sorting

    # first (a)
    index = 0
    a = coverage[index]

    # add (left, middle) to test suite
    testSuite.append((fileName[index], testCase[index]))

    if (len(a) == 0):
        print("total len(a) = 0")
        return testSuite

    tempA = []
    for value in a.split(', '):
        tempA.append(value)
    a = tempA
    # keep track of right (var)
    var = a
    lenC = []
    lenC.append(len(var))
    # remove (a) from list
    fileName = popTuple(fileName, index)
    testCase = popTuple(testCase, index)
    coverage = popTuple(coverage, index)

    count = 0

    # loop start
    while len(var) != 0:
        if (len(coverage) == 0):
            break

        # pick new first (b)
        b = coverage[index]
        tempB = []
        for value in b.split(', '):
            tempB.append(value)
        b = tempB
        ######## remove b from list
        coverage = popTuple(coverage, index)
        # compute right (a) set intersection right (b) => (c)
        c = set(var).intersection(set(b))


        # compare size of b to size of c
        if len(var) > len(c):
            var = c
            lenC.append(len(var))
            testSuite.append((fileName[index], testCase[index]))

        # discard
        testCase = popTuple(testCase, index)
        fileName = popTuple(fileName, index)

        count = count + 1

    return testSuite

def additionalStatement(orderedList):
    testSuite = []

    # sort based on right (Descending)
    fileName, testCase, coverage = zip(*orderedList)
    coverageSize = []
    print("additionalStatement coverage")
    print(coverage)
    for item in coverage:
        print("additionalStatement item")
        print(item)
        coverageSize.append(len(item))
    fileNameTestCaseCoverageAndSize = list(zip(fileName, testCase, coverage, coverageSize))
    sortedFileNameTestCaseCoverageAndSize = sorted(fileNameTestCaseCoverageAndSize, key=itemgetter(3))
    fileName, testCase, coverage, coverageSize = zip(*sortedFileNameTestCaseCoverageAndSize) # coverage size not needed anymore; only needed it for sorting

    # first (a)
    index = 0
    a = coverage[index]

    # add (left, middle) to test suite
    testSuite.append((fileName[index], testCase[index]))
    
    if (len(a) == 0):
        print("additional len(a) = 0")
        return testSuite

    tempA = []
    for value in a.split(', '):
        tempA.append(value)
    a = tempA
    # keep track of right (var)
    var = a
    lenC = []
    lenC.append(len(var))
    # remove (a) from list
    fileName = popTuple(fileName, index)
    testCase = popTuple(testCase, index)
    coverage = popTuple(coverage, index)

    count = 0
    count2 = 0

    # loop start
    while len(var) != 0:
        # if count > 15:
        #     break

        if (len(coverage) == 0):
            print("\nlen(coverage) == 0\n")
            break

        # loop start2
        for items in coverage:
            # if count2 > 15:
            #     break

            # compute (var) set intersection right (i)
                # need to convert items to list of strings to match with var
            right = []
            items = list(items)
            number = ''
            pastItem = ''
            singleDigit = True
            for item in items:
                if len(item) != 1:
                    singleDigit = False
                    break   # not a single digit
                if pastItem == ' ':
                    right.append(number)
                    number = ""
                    pastItem = ''
                if item != ',' and item != ' ':
                    number = number + item
                if item == ' ':
                    pastItem = ' '
            if not singleDigit:
                for item in items:
                    right.append(item)
            storeIntersection = set(var).intersection(set(right))
            # store intersection into right(i)
            coverage = editTuple(coverage, count2, storeIntersection)   # coverage[item] =  c   item = count2 for index
            count2 = count2 + 1


        # sort based on right (descending)   -----------------------------------------------------------------------------------
        coverageSize = []
        for item in coverage:
            coverageSize.append(len(item))

        fileNameTestCaseCoverageAndSize = list(zip(fileName, testCase, coverage, coverageSize))
        sortedFileNameTestCaseCoverageAndSize = sorted(fileNameTestCaseCoverageAndSize, key=itemgetter(3))
        fileName, testCase, coverage, coverageSize = zip(*sortedFileNameTestCaseCoverageAndSize) # coverage size not needed anymore; only needed it for sorting
        # ------------------------------------------------------------------------------------ ------------------------------------------------------------------------------------
        
        # pick first (b) and add left middle to test suite
        b = coverage[index]
        # print("b")
        # print(b)
        tempB = []
        for value in b:
            tempB.append(value)
        b = tempB

        ################ remove b from list
        coverage = popTuple(coverage, index)

        # testSuite.append((fileName[index], testCase[index]))

        # var = right (a) set inersection right (b)
        c = set(a).intersection(set(b))

        # compare size of b to size of c
        if len(var) > len(c):
            var = c
            lenC.append(len(var))
            testSuite.append((fileName[index], testCase[index]))

        # discard
        testCase = popTuple(testCase, index)
        fileName = popTuple(fileName, index)


        count = count + 1
        count2 = 0

    return testSuite

def randomizeStatement(orderedList):
    # print("orderedList")
    # print(orderedList)

    testSuite = []

    # randomize
    random.shuffle(orderedList)
    randomizedList = orderedList
    fileName, testCase, coverage = zip(*randomizedList)

    # random left (a)
    index = 0
    a = coverage[index]

    # add (left, middle) to test suite
    testSuite.append((fileName[index], testCase[index]))

    if (len(a) == 0):
        print("randomize len(a) = 0")
        return testSuite

    tempA = []
    for value in a.split(', '):
        tempA.append(value)
    a = tempA
    # keep track of right (Var)
    var = a
    lenC = []
    lenC.append(len(var))
    # remove (a) from list
    fileName = popTuple(fileName, index)
    testCase = popTuple(testCase, index)
    coverage = popTuple(coverage, index)

    count = 0

    # loop start
    while len(var) != 0:
        # print("count: " + str(count))

        # randomize
        # print("random list len")
        # print(len(randomizedList))

        randomizedList.pop(index)
        if (len(randomizedList) == 0):
            # print("broke")
            return testSuite
        random.shuffle(randomizedList)
        fileName, testCase, coverage = zip(*randomizedList)

        # pick a random left (b)
        # print("lenC")
        # print(lenC)
        b = coverage[index]
        tempB = []
        for value in b.split(', '):
            tempB.append(value)
        b = tempB
        # remove (b) from list
        coverage = popTuple(coverage, index)
        # compare size of right of (a) and (b) and keep track of smallest
        # if (len(var) < len(b)):
        #     smallest = len(var)
        # elif (len(b) < len(var)):
        #     smallest = len(b)
        # elif len(var) == len(b):
        #     smallest = len(var)

        # compute right (a) set intersection right (b) => (c)
        c = set(var).intersection(set(b))
        # print("c")
        # print(c)
        # print('a')
        # print(a)
        # print('b')
        # print(b)
        # print('c')
        # print(c)
        # print("Var")
        # print(var)
        # print('END\n')
        # if count > 15:
        #     break

        # compare size of smallest to size of (c)
        if len(var) > len(c):
            var = c
            lenC.append(len(var))
            testSuite.append((fileName[index], testCase[index]))
            # print("TEST SUITE APPENDNED")

        # discard
        testCase = popTuple(testCase, index)
        fileName = popTuple(fileName, index)

        count = count + 1

    return testSuite

# BRANCH TEST PRIORITIZIONAS
def totalBranch(orderedList):
    testSuite = []

    fileName, testCase, coverage = zip(*orderedList)
    numberOfZeros = []
    for item in coverage:
        zeros = 0

        fixedItem = []
        item = list(item)
        number = ''
        pastItem = ''
        singleDigit = True
        for item1 in item:    
            if len(item1) != 1:
                singleDigit = False
                break   # not a single digit
            if pastItem == ' ':
                fixedItem.append(number)
                number = ""
                pastItem = ''
            if item1 != ',' and item1 != ' ':
                number = number + item1
            if item1 == ' ':
                pastItem = ' '
        if not singleDigit:
            for item1 in item:
                fixedItem.append(item1)

        for item2 in fixedItem:
            if (int(item2) == 0):
                zeros = zeros + 1

        numberOfZeros.append(zeros)

    fileNameTestCaseCoverageAndSize = list(zip(fileName, testCase, coverage, numberOfZeros))
    sortedFileNameTestCaseCoverageAndSize = sorted(fileNameTestCaseCoverageAndSize, key=itemgetter(3))
    fileName, testCase, coverage, numberOfZeros = zip(*sortedFileNameTestCaseCoverageAndSize) # coverage size not needed anymore; only needed it for sorting

    # first (a)
    index = 0
    a = coverage[index]

    # add (left, middle) to test suite
    testSuite.append((fileName[index], testCase[index]))

    if (len(a) == 0):
        # print("total len(a) = 0")
        return testSuite

    tempA = []
    for value in a.split(', '):
        tempA.append(int(value))
    a = tempA
    # keep track of right (var)
    var = a
    lenC = []
    lenC.append(len(var))
    # remove (a) from list
    fileName = popTuple(fileName, index)
    testCase = popTuple(testCase, index)
    coverage = popTuple(coverage, index)

    varZero = 0
    for y in range(0, len(var)):
        if (var[y] == 0):
            varZero = varZero + 1

    count = 0

    # loop start
    while varZero != 0:
        # print("varZero")
        # print(varZero)

        if (len(coverage) == 0):
            break

        # pick new first (b)
        b = coverage[index]
        tempB = []
        for value in b.split(', '):
            tempB.append(int(value))
        b = tempB
        ######## remove b from list
        coverage = popTuple(coverage, index)
        # compute right (a) set intersection right (b) => (c)
        # c = set(var).intersection(set(b))
        c = []

        for y in range(0, len(var)):
            c.append(var[y] + b[y])
        
        # find zeros
        varZero = 0
        cZero = 0
        for y in range(0, len(var)):
            if (var[y] == 0):
                varZero = varZero + 1
        for y in range(0, len(c)):
            if (c[y] == 0):
                cZero = cZero + 1

        # compare size of var to size of c
        if varZero > cZero:
            var = c
            lenC.append(len(var))
            testSuite.append((fileName[index], testCase[index]))

        # discard
        testCase = popTuple(testCase, index)
        fileName = popTuple(fileName, index)

        count = count + 1

    return testSuite

def additionalBranch(orderedList):
    testSuite = []

    # sort based on right (Descending)
    fileName, testCase, coverage = zip(*orderedList)

    intCoverage = []

    # convert coverage from list of strings to list of ints
    for item in coverage:
        fixedItem = []   # 1, 6, 7 to 167
        item = list(item)
        number = ''
        pastItem = ''
        singleDigit = True
        for item1 in item:    
            if len(item1) != 1:
                singleDigit = False
                break   # not a single digit
            if pastItem == ' ':
                fixedItem.append(int(number))
                number = ""
                pastItem = ''
            if item1 != ',' and item1 != ' ':
                number = number + item1
            if item1 == ' ':
                pastItem = ' '
        if not singleDigit:
            for item1 in item:
                fixedItem.append(int(item1))
        intCoverage.append(fixedItem)

    # print("intCoverage[0]")
    # print(type(intCoverage[0]))
    # print(intCoverage[0])

    coverage = tuple(intCoverage)   # COVERAGE IS NOW INTS

    numberOfZeros = []
    for item in coverage:
        zerosCounter = 0
        for y in range(0, len(item)):
            if (item[y] == 0):
                zerosCounter = zerosCounter + 1

        numberOfZeros.append(zerosCounter)

    fileNameTestCaseCoverageAndSize = list(zip(fileName, testCase, coverage, numberOfZeros))
    sortedFileNameTestCaseCoverageAndSize = sorted(fileNameTestCaseCoverageAndSize, key=itemgetter(3))
    fileName, testCase, coverage, numberOfZeros = zip(*sortedFileNameTestCaseCoverageAndSize) # coverage size not needed anymore; only needed it for sorting

    # first (a)
    index = 0
    # a = coverage[index]
    var = coverage[index]
    varZero = numberOfZeros[index]

    # add (left, middle) to test suite
    testSuite.append((fileName[index], testCase[index]))
    
    if (varZero == 0):
        # print("additional a has no zeros")
        return testSuite

    # tempA = []
    # for value in a.split(', '):
    #     tempA.append(int(value))
    # a = tempA

    # keep track of right (var)
    # var = a
    # varZero = aZero
    lenC = []
    lenC.append(len(var))
    # remove (a) from list
    fileName = popTuple(fileName, index)
    testCase = popTuple(testCase, index)
    coverage = popTuple(coverage, index)

    count = 0
    count2 = 0

    # loop start
    while varZero != 0:
        # print("varZero")
        # print(varZero)
        # if count > 15:
        #     break

        if (len(coverage) == 0):
            # print("\nlen(coverage) == 0\n")
            break

        # loop start2
        for items in coverage:
            # if count2 > 15:
            #     break

            # compute (var) set intersection right (i)
            # storeIntersection = set(var).intersection(set(right))
            storeIntersection = []
            for y in range(0, len(var)):
                storeIntersection.append(var[y] + items[y])   # coverage(i) is tuple of 3 vars

            # store intersection into right(i)
            coverage = editTuple(coverage, count2, storeIntersection)   # coverage[item] =  c   item = count2 for index
            count2 = count2 + 1

        numberOfZeros = []
        for item in coverage:
            zerosCounter = 0
            for y in range(0, len(item)):
                if (item[y] == 0):
                    zerosCounter = zerosCounter + 1

            numberOfZeros.append(zerosCounter)


        # sort based on right (descending)   -----------------------------------------------------------------------------------
        # coverageSize = []
        # for item in coverage:
        #     coverageSize.append(len(item))


        # convert from numbers to string so single digit parsing will work
        # for item in coverage:
        #     print()

        # print("coverage")
        # print(coverage)

        fileNameTestCaseCoverageAndSize = list(zip(fileName, testCase, coverage, numberOfZeros))
        sortedFileNameTestCaseCoverageAndSize = sorted(fileNameTestCaseCoverageAndSize, key=itemgetter(3))
        fileName, testCase, coverage, numberOfZeros = zip(*sortedFileNameTestCaseCoverageAndSize) # coverage size not needed anymore; only needed it for sorting
        # ------------------------------------------------------------------------------------ ------------------------------------------------------------------------------------
        
        # pick first (b) and add left middle to test suite
        b = coverage[index]
        # print("b")
        # print(b)
        # tempB = []
        # for value in b:
        #     tempB.append(int(value))
        # b = tempB

        ################ remove b from list
        coverage = popTuple(coverage, index)

        # testSuite.append((fileName[index], testCase[index]))

        # var = right (a) set inersection right (b)
        # c = set(a).intersection(set(b))

        c = []
        for y in range(0, len(var)):
            c.append(var[y] + b[y])

        # find zeros
        varZero = 0
        for y in range(0, len(var)):
            if (var[y] == 0):
                varZero = varZero + 1
        cZero = 0
        for y in range(0, len(c)):
            if (c[y] == 0):
                cZero = cZero + 1

        # compare size of b to size of c
        if varZero > cZero:
            var = c
            lenC.append(len(var))
            testSuite.append((fileName[index], testCase[index]))
            # print("testSuite[index]")
            # print(testSuite[index])

        # discard
        testCase = popTuple(testCase, index)
        fileName = popTuple(fileName, index)


        count = count + 1
        count2 = 0

    return testSuite

def randomizeBranch(orderedList):
    testSuite = []

    # randomize
    random.shuffle(orderedList)
    randomizedList = orderedList
    fileName, testCase, coverage = zip(*randomizedList)

    # random left (a)
    index = 0
    a = coverage[index]

    # add (left, middle) to test suite
    testSuite.append((fileName[index], testCase[index]))

    tempA = []
    for value in a.split(', '):
        tempA.append(int(value))
    a = tempA

    # keep track of right (Var)
    var = a
    lenC = []
    lenC.append(len(var))
    # remove (a) from list
    fileName = popTuple(fileName, index)
    testCase = popTuple(testCase, index)
    coverage = popTuple(coverage, index)

    varZero = 0
    for y in range(0, len(var)):
        if (var[y] == 0):
            varZero = varZero + 1

    if (varZero == 0):
        # print("randomize len(a) = 0")
        return testSuite

    count = 0

    # loop start
    while varZero != 0:
        # print("varZero")
        # print(varZero)
        # randomize
        randomizedList.pop(index)
        if (len(randomizedList) == 0):
            break
        random.shuffle(randomizedList)
        fileName, testCase, coverage = zip(*randomizedList)

        # pick a random left (b)
        b = coverage[index]
        tempB = []
        for value in b.split(', '):
            tempB.append(int(value))
        b = tempB
        # remove (b) from list
        coverage = popTuple(coverage, index)
        # compare size of right of (a) and (b) and keep track of smallest

        # compute right (a) set intersection right (b) => (c)
        # c = set(var).intersection(set(b))
        c = []

        for y in range(0, len(var)):
            c.append(var[y] + b[y])
        
        # find zeros
        varZero = 0
        cZero = 0
        for y in range(0, len(var)):
            if (var[y] == 0):
                varZero = varZero + 1
        for y in range(0, len(c)):
            if (c[y] == 0):
                cZero = cZero + 1

        # compare size of b to size of c
        if varZero > cZero:
            var = c
            lenC.append(len(var))
            testSuite.append((fileName[index], testCase[index]))

        # discard
        testCase = popTuple(testCase, index)
        fileName = popTuple(fileName, index)

        count = count + 1

    return testSuite






def popTuple(fileName, index):
    fileList = list(fileName)
    fileList.pop(index)
    fileName2 = tuple(fileList)
    return fileName2

def editTuple(coverage, count2, c):
    coverage = list(coverage)
    coverage[count2] = c
    coverage2 = tuple(coverage)
    return coverage2

def filenameTestcaseCoverage(lines):
    filenameTestcaseCoverage = []
    secondLine = False
    coverage = ""
    for line in lines:
        if (secondLine == False):
            fileName = line.partition(": ")[0]
            testCase = line.partition(": ")[2]
            testCase = testCase[:len(testCase) - 1]   # remove \n
        elif (secondLine == True):
            coverage = line.partition(" : ")[2]
            coverage = coverage[:len(coverage) - 3]   # remove \n
            
        if (secondLine == True):
            filenameTestcaseCoverage.append((fileName, testCase, coverage))

        # set secondLine appropriately
        if (secondLine == True):
            secondLine = False
        elif (secondLine == False):
            secondLine = True

    return filenameTestcaseCoverage

main()