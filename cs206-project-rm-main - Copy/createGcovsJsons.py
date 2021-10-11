import json
import subprocess
import sys
import os
import gzip
import shutil
import time

# generalized strings for benchmark programs
universePathToFileGen = "benchmarks/general/universe.txt"
inputCommandGen = "./general "
compileCommandGen = "gcc -fprofile-arcs -ftest-coverage -Wno-return-type -g -o general general.c"
pathGen = 'benchmarks/general'
statementCoveragePathGen = "benchmarks/general/statementCoverage"
branchCoveragePathGen = "benchmarks/general/branchCoverage"
gcovCommandGen = "gcov general.c -m"
gcovPathToFileGen = "benchmarks/general/general.c.gcov"
gcovFileGen = "general.c.gcov"
gcovBranchCommandGen = "gcov -b -c general.c -m"
jsonCommandGen = "gcov --json-format general.c"
jsonGzPathToFileGen = "benchmarks/general/general.c.gcov.json.gz"
jsonPathToFileGen = "benchmarks/general/general.c.gcov.json"
jsonFileGen = "general.c.gcov.json"
gcdaFileGen = 'general.gcda'
tcasFileGen = 'general'
jsonGzFileGen = 'general.c.gcov.json.gz'
gcnoFileGen = 'general.gcno'


def main():
    start = time.time()

    benchmarks = ['tcas', 'totinfo', 'schedule', 'schedule2', 'printtokens', 'printtokens2', 'replace']

    for benchmark in benchmarks:
        universePathToFile = universePathToFileGen.replace("general", benchmark)
        inputCommand = inputCommandGen.replace("general", benchmark)
        compileCommand = compileCommandGen.replace("general", benchmark)
        path = pathGen.replace("general", benchmark)
        statementCoveragePath = statementCoveragePathGen.replace("general", benchmark)
        branchCoveragePath = branchCoveragePathGen.replace("general", benchmark)
        gcovCommand = gcovCommandGen.replace("general", benchmark)
        gcovPathToFile = gcovPathToFileGen.replace("general", benchmark)
        gcovFile = gcovFileGen.replace("general", benchmark)
        gcovBranchCommand = gcovBranchCommandGen.replace("general", benchmark)
        jsonCommand = jsonCommandGen.replace("general", benchmark)
        jsonGzPathToFile = jsonGzPathToFileGen.replace("general", benchmark)
        jsonPathToFile = jsonPathToFileGen.replace("general", benchmark)
        jsonFile = jsonFileGen.replace("general", benchmark)
        gcdaFile = gcdaFileGen.replace("general", benchmark)
        tcasFile = tcasFileGen.replace("general", benchmark)
        jsonGzFile = jsonGzFileGen.replace("general", benchmark)
        gcnoFile = gcnoFileGen.replace("general", benchmark)

        # special benchmark compile commands
        if (benchmark == 'totinfo' or benchmark == 'replace'):
            compileCommand = compileCommand + " -lm"

        # create directory for storing statement and branch coverage gcov and json files
        if (not(os.path.exists(statementCoveragePath) and os.path.isdir(statementCoveragePath))):
            os.mkdir(statementCoveragePath)
        if (not(os.path.exists(branchCoveragePath) and os.path.isdir(branchCoveragePath))):
            os.mkdir(branchCoveragePath)

        # statement coverage
        coverage(universePathToFile, inputCommand, compileCommand, path, statementCoveragePath, branchCoveragePath, gcovCommand, '', gcovPathToFile, gcovFile, jsonCommand, jsonGzPathToFile, jsonPathToFile, jsonFile, gcdaFile, tcasFile, jsonGzFile, gcnoFile)
        # branch coverage
        coverage(universePathToFile, inputCommand, compileCommand, path, statementCoveragePath, branchCoveragePath, gcovCommand, gcovBranchCommand, gcovPathToFile, gcovFile, jsonCommand, jsonGzPathToFile, jsonPathToFile, jsonFile, gcdaFile, tcasFile, jsonGzFile, gcnoFile)

        print("finished benchmark: " + str(benchmark) + ", elapsed time: ")
        print(time.time() - start)

    end = time.time()
    print("Total elapsed time: " + str(end - start))

    return

def coverage(universePathToFile, inputCommand, compileCommand, path, statementCoveragePath, branchCoveragePath, gcovCommand, gcovBranchCommand, gcovPathToFile, gcovFile, jsonCommand, jsonGzPathToFile, jsonPathToFile, jsonFile, gcdaFile, tcasFile, jsonGzFile, gcnoFile):
    # statement coverage
    testNum = 1
    # testing = 0
    testCases = universe(universePathToFile)

    for testCase in testCases:
        # if testing > 3:
        #     break
        inputTestCase = inputCommand + str(testCase)

        # compile/statement coverage with specified test case
        runCompile = subprocess.run([compileCommand], capture_output=True, shell=True, cwd=path)
        runTestCase = subprocess.run([inputTestCase], capture_output=True, shell=True, cwd=path)

        # gcda file was unable to be created
        if (not(os.path.exists(path) and os.path.isfile(path + "/" + gcdaFile))):
            print("Gcda file was not able to be created for test case: " + str(testNum))
            print("path + gcdaFile: " + path + "/" + gcdaFile)
            continue   # skip test case

        # gcov and json
        if (gcovBranchCommand == ''):   # statement coverage
            runGcov = subprocess.run([gcovCommand], capture_output=True, shell=True, cwd=path)
        elif (gcovBranchCommand != ''):   # branch coverage
            runGcov = subprocess.run([gcovBranchCommand], capture_output=True, shell=True, cwd=path)
        runJson = subprocess.run([jsonCommand], capture_output=True, shell=True, cwd=path)

        #  convert json.gz to json
        with gzip.open(jsonGzPathToFile, 'rb') as f_in:
            with open(jsonPathToFile, 'wb') as f_out:  # w also creates file
                shutil.copyfileobj(f_in, f_out)

        # rename json to reflect specified test case
        renameFile(testNum, path, jsonFile, gcovBranchCommand, statementCoveragePath, branchCoveragePath)

        # rename gcov to reflect specified test case
        renameFile(testNum, path, gcovFile, gcovBranchCommand, statementCoveragePath, branchCoveragePath)

        # parse json (FIXME: insert later)

        removeFiles(path, gcdaFile, tcasFile, gcovFile, jsonFile, jsonGzFile, gcnoFile)

        # update testNum to next test case num
        testNum = testNum + 1

        # testing = testing + 1

    return

def renameFile(testNum, path, file, gcovBranchCommand, statementCoveragePath, branchCoveragePath):
    origFile = file
    if (gcovBranchCommand == ''):   # statement coverage
        file = "statementCoverage_" + str(testNum) + "_" + origFile
        os.rename(os.path.join(path, origFile), os.path.join(statementCoveragePath, file))   # also moves file
    elif (gcovBranchCommand != ''):   # branch coverage
        file = "branchCoverage_" + str(testNum) + "_" + origFile
        os.rename(os.path.join(path, origFile), os.path.join(branchCoveragePath, file))   # also moves file

    return

def removeFiles(path, gcdaFile, tcasFile, gcovFile, jsonFile, jsonGzFile, gcnoFile):
    if (os.path.exists(path) and os.path.isfile(path + "/" + gcdaFile)):
        os.remove(os.path.join(path, gcdaFile))
    if (os.path.exists(path) and os.path.isfile(path + "/" + tcasFile)):
        os.remove(os.path.join(path, tcasFile))
    # os.remove(os.path.join(path, gcovFile))
    # os.remove(os.path.join(path, removeJson))
    if (os.path.exists(path) and os.path.isfile(path + "/" + jsonGzFile)):
        os.remove(os.path.join(path, jsonGzFile))
    if (os.path.exists(path) and os.path.isfile(path + "/" + gcnoFile)):
        os.remove(os.path.join(path, gcnoFile))

    return

## universe.txt --------------------------------------------------------------------------
def universe(file):
    with open(file) as f:
        testCases = f.readlines()
    return testCases

    
main()