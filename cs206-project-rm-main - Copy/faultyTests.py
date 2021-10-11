import os
import time
import subprocess

import os.path


statementCoveragePathGen = "benchmarks/general/statementCoverageLineNumbers"
branchCoveragePathGen = "benchmarks/general/branchCoverageLineNumbers"
faultyTestPathGen = "benchmarks/general/v"
compileCommandGen = "gcc -fprofile-arcs -ftest-coverage -Wno-return-type -g -o general general.c"
pathGen = 'benchmarks/general'
gcovCommandGen = "gcov general.c -m"
gcovBranchCommandGen = "gcov -b -c general.c -m"
inputCommandGen = "./general "
gcdaFileGen = 'general.gcda'
gcnoFileGen = 'general.gcno'
tcasFileGen = 'general'

def main():
    benchmarks = ['tcas', 'totinfo', 'schedule', 'schedule2', 'printtokens', 'printtokens2', 'replace']
    # benchmarks = ['schedule', 'schedule2', 'printtokens', 'printtokens2', 'replace']
    # benchmarks = ['tcas']

    for benchmark in benchmarks:
        print("benchmark")
        print(benchmark)
        statementCoveragePath = statementCoveragePathGen.replace("general", benchmark)
        branchCoveragePath = branchCoveragePathGen.replace("general", benchmark)
        faultyTestPath = faultyTestPathGen.replace("general", benchmark)
        compileCommand = compileCommandGen.replace("general", benchmark)
        path = pathGen.replace("general", benchmark)
        gcovCommand = gcovCommandGen.replace("general", benchmark)
        gcovBranchCommand = gcovBranchCommandGen.replace("general", benchmark)
        inputCommand = inputCommandGen.replace("general", benchmark)
        gcdaFile = gcdaFileGen.replace("general", benchmark)
        gcnoFile = gcnoFileGen.replace("general", benchmark)
        tcasFile = tcasFileGen.replace("general", benchmark)

        # special benchmark compile commands
        if (benchmark == 'totinfo' or benchmark == 'replace'):
            compileCommand = compileCommand + " -lm"

        # # statement ---------------------------------------------------------------------------------
        with open(statementCoveragePath + "/randomizedStatementTestSuite.txt") as f:
            lines = f.readlines()

        statementFileNames = []
        statementTestCases = []
        for line in lines:
            statementFileNames.append(line.partition(": ")[0])
            statementTestCases.append(line.partition(": ")[2])

        randomizedStatementFails = determineFaults(statementFileNames, statementTestCases, statementCoveragePath, faultyTestPath, compileCommand, path, inputCommand, gcdaFile, gcnoFile, tcasFile)

        with open(statementCoveragePath + "/totalStatementTestSuite.txt") as f:
            lines = f.readlines()

        statementFileNames = []
        statementTestCases = []
        for line in lines:
            statementFileNames.append(line.partition(": ")[0])
            statementTestCases.append(line.partition(": ")[2])

        totalStatementFails = determineFaults(statementFileNames, statementTestCases, statementCoveragePath, faultyTestPath, compileCommand, path, inputCommand, gcdaFile, gcnoFile, tcasFile)

        with open(statementCoveragePath + "/additionalStatementTestSuite.txt") as f:
            lines = f.readlines()

        statementFileNames = []
        statementTestCases = []
        for line in lines:
            statementFileNames.append(line.partition(": ")[0])
            statementTestCases.append(line.partition(": ")[2])

        additionalStatementFails = determineFaults(statementFileNames, statementTestCases, statementCoveragePath, faultyTestPath, compileCommand, path, inputCommand, gcdaFile, gcnoFile, tcasFile)

        # branch -------------------------------------------------------------------------------------
        with open(branchCoveragePath + "/randomizedBranchTestSuite.txt") as f:
            lines = f.readlines()

        branchFileNames = []
        branchTestCases = []
        for line in lines:
            branchFileNames.append(line.partition(": ")[0])
            branchTestCases.append(line.partition(": ")[2])

        randomizedBranchFails = determineFaults(branchFileNames, branchTestCases, branchCoveragePath, faultyTestPath, compileCommand, path, inputCommand, gcdaFile, gcnoFile, tcasFile)

        with open(branchCoveragePath + "/totalBranchTestSuite.txt") as f:
            lines = f.readlines()

        branchFileNames = []
        branchTestCases = []
        for line in lines:
            branchFileNames.append(line.partition(": ")[0])
            branchTestCases.append(line.partition(": ")[2])

        totalBranchFails = determineFaults(branchFileNames, branchTestCases, branchCoveragePath, faultyTestPath, compileCommand, path, inputCommand, gcdaFile, gcnoFile, tcasFile)

        with open(branchCoveragePath + "/additionalBranchTestSuite.txt") as f:
            lines = f.readlines()

        branchFileNames = []
        branchTestCases = []
        for line in lines:
            branchFileNames.append(line.partition(": ")[0])
            branchTestCases.append(line.partition(": ")[2])

        additionalBranchFails = determineFaults(branchFileNames, branchTestCases, branchCoveragePath, faultyTestPath, compileCommand, path, inputCommand, gcdaFile, gcnoFile, tcasFile)


        # fails
        f = open(statementCoveragePath + "/randomizedFails.txt","w+")
        f.write("randomizedStatementFails: " + str(randomizedStatementFails))
        f.close()

        f = open(statementCoveragePath + "/totalFails.txt","w+")
        f.write("totalStatementFails: " + str(totalStatementFails))
        f.close()

        f = open(statementCoveragePath + "/additionalFails.txt","w+")
        f.write("additionalStatementFails: " + str(additionalStatementFails))
        f.close()

        f = open(branchCoveragePath + "/randomizedFails.txt","w+")
        f.write("randomizedBranchFails: " + str(randomizedBranchFails))
        f.close()

        f = open(branchCoveragePath + "/totalFails.txt","w+")
        f.write("totalBranchFails: " + str(totalBranchFails))
        f.close()

        f = open(branchCoveragePath + "/additionalFails.txt","w+")
        f.write("additionalBranchFails: " + str(additionalBranchFails))
        f.close()


    return

def determineFaults(fileNames, testCases,statementCoveragePath, faultyTestPath, compileCommand, path, inputCommand, gcdaFile, gcnoFile, tcasFile):
    # statement
    i = 1   # start at 1 for faulty folders
    index = 0
    fails = 0
    while (os.path.exists(faultyTestPath + str(i))):
        print("in while, i: " + str(i))
        # run benchmark program with input i
        for testCase in testCases:
            testCase = testCase[:len(testCase) - 1]  # remove "\n"
            inputTestCase = inputCommand + str(testCase)
            runCompile1 = subprocess.run([compileCommand], capture_output=True, shell=True, cwd=path)
            runTestCase1 = subprocess.run([inputTestCase], capture_output=True, shell=True, cwd=path)
            
            # run v1 with input i
            runCompile2 = subprocess.run([compileCommand], capture_output=True, shell=True, cwd=faultyTestPath + str(i))
            runTestCase2 = subprocess.run([inputTestCase], capture_output=True, shell=True, cwd=faultyTestPath + str(i))

            # print("Testcase")
            # print(testCase)
            # print("runTestCase1.stdout")
            # print(runTestCase1.stdout)
            # print("runTestCase2.stdout")
            # print(runTestCase2.stdout)

            if (runTestCase1.stdout != runTestCase2.stdout): # and ("Error" not in str(runTestCase1.stdout) or "Error" not in str(runTestCase2.stdout)
                f = open(faultyTestPath + str(i) + "/faultyTest.txt","w+")
                f.write("V" + str(i) + " failed on test case: " + testCase + " with file: " + fileNames[index])
                fails = fails + 1
                # print("FAILED FAILED FAILED FAILED test case: " + str(testCase))

                removeFiles(path, -1, gcdaFile, gcnoFile, tcasFile)
                removeFiles(faultyTestPath, i, gcdaFile, gcnoFile, tcasFile)

                break   # (only needs to find one mutant, only if one input breaks it not how many inputs break it)

            removeFiles(path, -1, gcdaFile, gcnoFile, tcasFile)
            removeFiles(faultyTestPath, i, gcdaFile, gcnoFile, tcasFile)

            index = index + 1

        index = 0

        # removes benchmark files after breaking
        # remove benchmark .gcda
        if (os.path.exists(path) and os.path.isfile(path + "/" + gcdaFile)):
            os.remove(os.path.join(path, gcdaFile))
        # remove benchmark gcno
        if (os.path.exists(path) and os.path.isfile(path + "/" + gcnoFile)):
            os.remove(os.path.join(path, gcnoFile))
        # remove benchmark
        if (os.path.exists(path) and os.path.isfile(path + "/" + tcasFile)):
            os.remove(os.path.join(path, tcasFile))

        i = i + 1

    print("fails: " + str(fails))

    return fails

def total():


    return

def removeFiles(path, i, gcdaFile, gcnoFile, tcasFile):
    if i != -1:   # faulty files
        # remove faulty .gcda
        if (os.path.exists(path + str(i)) and os.path.isfile(path + str(i) + "/" + gcdaFile)):
            os.remove(os.path.join(path + str(i), gcdaFile))
        # remove faulty gcno
        if (os.path.exists(path + str(i)) and os.path.isfile(path + str(i) + "/" + gcnoFile)):
            os.remove(os.path.join(path + str(i), gcnoFile))
        # remove faulty
        if (os.path.exists(path + str(i)) and os.path.isfile(path + str(i) + "/" + tcasFile)):
            os.remove(os.path.join(path + str(i), tcasFile))
    else:   # benchmark files
        # remove faulty .gcda
        if (os.path.exists(path) and os.path.isfile(path + "/" + gcdaFile)):
            os.remove(os.path.join(path, gcdaFile))
        # remove faulty gcno
        if (os.path.exists(path) and os.path.isfile(path + "/" + gcnoFile)):
            os.remove(os.path.join(path, gcnoFile))
        # remove faulty
        if (os.path.exists(path) and os.path.isfile(path + "/" + tcasFile)):
            os.remove(os.path.join(path, tcasFile))

    return

main()