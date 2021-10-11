

statementCoveragePathGen = "benchmarks/general/statementCoverageLineNumbers"
branchCoveragePathGen = "benchmarks/general/branchCoverageLineNumbers"


def main():
    benchmarks = ['tcas', 'totinfo', 'schedule', 'schedule2', 'printtokens', 'printtokens2', 'replace']
    # benchmarks = ['schedule', 'schedule2', 'printtokens', 'printtokens2', 'replace']

    for benchmark in benchmarks:
        statementCoveragePath = statementCoveragePathGen.replace("general", benchmark)
        branchCoveragePath = branchCoveragePathGen.replace("general", benchmark)


        # # RANDOMIZED ----------------------------------------------------------------------
        with open(statementCoveragePath + "/randomizedStatementTestSuite.txt") as f:
            randomizedStatementTestSuite = f.readlines()

        randomizedStatementListTestSuite = filenameTestcase(randomizedStatementTestSuite)

        print("randomizedStatementListTestSuite")
        print(randomizedStatementListTestSuite)

        randomizedStatementTestSuiteSize = len(randomizedStatementListTestSuite)

        print()
        print("randomizedStatementTestSuiteSize")
        print(randomizedStatementTestSuiteSize)

        with open(statementCoveragePath + "/randomizedFails.txt") as f:
            randomizedStatementFails = f.readlines()

        randomizedStatementFails = getFails(randomizedStatementFails)

        # print()
        # print("randomizedStatementFails")
        # print(randomizedStatementFails)

        f = open(statementCoveragePath + "/randomizedStatementDatatable.txt","w+")
        f.write("Test Suite: \n")
        for key, value in randomizedStatementListTestSuite:
            f.write(key)
            f.write(": ")
            f.write(value)
            f.write("\n")
        f.write("\n")
        f.write("Size of Test Suite: ")
        f.write(str(randomizedStatementTestSuiteSize))
        f.write("\n")
        f.write("\n")
        f.write("Number of Faults Exposed: ")
        f.write(str(randomizedStatementFails))
        f.close()

        # TOTAL ----------------------------------------------------------------------
        with open(statementCoveragePath + "/totalStatementTestSuite.txt") as f:
            totalStatementTestSuite = f.readlines()

        totalStatementListTestSuite = filenameTestcase(totalStatementTestSuite)

        print("totalStatementListTestSuite")
        print(totalStatementListTestSuite)

        totalStatementTestSuiteSize = len(totalStatementListTestSuite)

        print()
        print("totalStatementTestSuiteSize")
        print(totalStatementTestSuiteSize)

        with open(statementCoveragePath + "/totalFails.txt") as f:
            totalStatementFails = f.readlines()

        totalStatementFails = getFails(totalStatementFails)

        # print()
        # print("totalStatementFails")
        # print(totalStatementFails)

        f = open(statementCoveragePath + "/totalStatementDatatable.txt","w+")
        f.write("Test Suite: \n")
        for key, value in totalStatementListTestSuite:
            f.write(key)
            f.write(": ")
            f.write(value)
            f.write("\n")
        f.write("\n")
        f.write("Size of Test Suite: ")
        f.write(str(totalStatementTestSuiteSize))
        f.write("\n")
        f.write("\n")
        f.write("Number of Faults Exposed: ")
        f.write(str(totalStatementFails))
        f.close()

        # ADDITIONAL ----------------------------------------------------------------------
        with open(statementCoveragePath + "/additionalStatementTestSuite.txt") as f:
            additionalStatementTestSuite = f.readlines()

        additionalStatementListTestSuite = filenameTestcase(additionalStatementTestSuite)

        print("additionalStatementListTestSuite")
        print(additionalStatementListTestSuite)

        additionalStatementTestSuiteSize = len(additionalStatementListTestSuite)

        print()
        print("additionalStatementTestSuiteSize")
        print(additionalStatementTestSuiteSize)

        with open(statementCoveragePath + "/additionalFails.txt") as f:
            additionalStatementFails = f.readlines()

        additionalStatementFails = getFails(additionalStatementFails)

        print()
        print("additionalStatementFails")
        print(additionalStatementFails)

        f = open(statementCoveragePath + "/additionalStatementDatatable.txt","w+")
        f.write("Test Suite: \n")
        for key, value in additionalStatementListTestSuite:
            f.write(key)
            f.write(": ")
            f.write(value)
            f.write("\n")
        f.write("\n")
        f.write("Size of Test Suite: ")
        f.write(str(additionalStatementTestSuiteSize))
        f.write("\n")
        f.write("\n")
        f.write("Number of Faults Exposed: ")
        f.write(str(additionalStatementFails))
        f.close()








        # # BRANCHHHH

         # RANDOMIZED ----------------------------------------------------------------------
        with open(branchCoveragePath + "/randomizedBranchTestSuite.txt") as f:
            randomizedBranchTestSuite = f.readlines()

        randomizedBranchListTestSuite = filenameTestcase(randomizedBranchTestSuite)

        print("randomizedBranchListTestSuite")
        print(randomizedBranchListTestSuite)

        randomizedBranchTestSuiteSize = len(randomizedBranchListTestSuite)

        print()
        print("randomizedBranchTestSuiteSize")
        print(randomizedBranchTestSuiteSize)

        with open(branchCoveragePath + "/randomizedFails.txt") as f:
            randomizedBranchFails = f.readlines()

        randomizedBranchFails = getFails(randomizedBranchFails)

        f = open(branchCoveragePath + "/randomizedBranchDatatable.txt","w+")
        f.write("Test Suite: \n")
        for key, value in randomizedBranchListTestSuite:
            f.write(key)
            f.write(": ")
            f.write(value)
            f.write("\n")
        f.write("\n")
        f.write("Size of Test Suite: ")
        f.write(str(randomizedBranchTestSuiteSize))
        f.write("\n")
        f.write("\n")
        f.write("Number of Faults Exposed: ")
        f.write(str(randomizedBranchFails))
        f.close()

        # TOTAL ----------------------------------------------------------------------
        with open(branchCoveragePath + "/totalBranchTestSuite.txt") as f:
            totalBranchTestSuite = f.readlines()

        totalBranchListTestSuite = filenameTestcase(totalBranchTestSuite)

        print("totalBranchListTestSuite")
        print(totalBranchListTestSuite)

        totalBranchTestSuiteSize = len(totalBranchListTestSuite)

        with open(branchCoveragePath + "/totalFails.txt") as f:
            totalBranchFails = f.readlines()

        totalBranchFails = getFails(totalBranchFails)

        # print()
        # print("totalStatementFails")
        # print(totalStatementFails)

        f = open(branchCoveragePath + "/totalBranchDatatable.txt","w+")
        f.write("Test Suite: \n")
        for key, value in totalBranchListTestSuite:
            f.write(key)
            f.write(": ")
            f.write(value)
            f.write("\n")
        f.write("\n")
        f.write("Size of Test Suite: ")
        f.write(str(totalBranchTestSuiteSize))
        f.write("\n")
        f.write("\n")
        f.write("Number of Faults Exposed: ")
        f.write(str(totalBranchFails))
        f.close()

        # ADDITIONAL ----------------------------------------------------------------------
        with open(branchCoveragePath + "/additionalBranchTestSuite.txt") as f:
            additionalBranchTestSuite = f.readlines()

        additionalBranchListTestSuite = filenameTestcase(additionalBranchTestSuite)

        print("additionalbranchListTestSuite")
        print(additionalBranchListTestSuite)

        additionalBranchTestSuiteSize = len(additionalBranchListTestSuite)


        with open(branchCoveragePath + "/additionalFails.txt") as f:
            additionalBranchFails = f.readlines()

        additionalBranchFails = getFails(additionalBranchFails)

        # print()
        # print("additionalStatementFails")
        # print(additionalBranchFails)

        f = open(branchCoveragePath + "/additionalBranchDatatable.txt","w+")
        f.write("Test Suite: \n")
        for key, value in additionalBranchListTestSuite:
            f.write(key)
            f.write(": ")
            f.write(value)
            f.write("\n")
        f.write("\n")
        f.write("Size of Test Suite: ")
        f.write(str(additionalBranchTestSuiteSize))
        f.write("\n")
        f.write("\n")
        f.write("Number of Faults Exposed: ")
        f.write(str(additionalBranchFails))
        f.close()

    return

def getFails(lines):
    for line in lines:
        fails = line.partition(": ")[2]

    return fails

def filenameTestcase(lines):
    filenameTestcase = []
    for line in lines:
        fileName = line.partition(": ")[0]
        testCase = line.partition(": ")[2]
        testCase = testCase[:len(testCase) - 1]   # remove \n

        filenameTestcase.append((fileName, testCase))

    return filenameTestcase

main()