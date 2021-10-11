import os
import json
import time

# generalized strings for benchmark programs
listDirStatementGen = "benchmarks/general/statementCoverage"
openStatementGen = "benchmarks/general/statementCoverage/"
listDirBranchGen = "benchmarks/general/branchCoverage"
openBranchGen = "benchmarks/general/branchCoverage/"
statementCoveragePathGen = "benchmarks/general/statementCoverageLineNumbers"
branchCoveragePathGen = "benchmarks/general/branchCoverageLineNumbers"
statementLineNumberFileGen = "benchmarks/general/statementCoverageLineNumbers/lineNumbers.txt"
branchLineNumberFileGen = "benchmarks/general/branchCoverageLineNumbers/lineNumbers.txt"

def main2():
    start = time.time()
    benchmarks = ['tcas', 'totinfo', 'schedule', 'schedule2', 'printtokens', 'printtokens2', 'replace']
    allLineNumbersStatement = []
    allTakenNumbersBranch = []

    for benchmark in benchmarks:
        listDirStatement = listDirStatementGen.replace("general", benchmark)
        openStatement = openStatementGen.replace("general", benchmark)
        listDirBranch = listDirBranchGen.replace("general", benchmark)
        openBranch = openBranchGen.replace("general", benchmark)
        statementCoveragePath = statementCoveragePathGen.replace("general", benchmark)
        branchCoveragePath = branchCoveragePathGen.replace("general", benchmark)
        statementLineNumberFile = statementLineNumberFileGen.replace("general", benchmark)
        branchLineNumberFile = branchLineNumberFileGen.replace("general", benchmark)

        # create directory for storing statement and branch coverage gcov and json files
        if (not(os.path.exists(statementCoveragePath) and os.path.isdir(statementCoveragePath))):
            os.mkdir(statementCoveragePath)
        if (not(os.path.exists(branchCoveragePath) and os.path.isdir(branchCoveragePath))):
            os.mkdir(branchCoveragePath)

        allLineNumbersStatement = statementCoverage(listDirStatement, openStatement)
        # print("allLineNumbersStatement")
        # print(allLineNumbersStatement)

        with open(statementLineNumberFile, 'w') as f:
            # print("statementLineNumberFile")
            # print(statementLineNumberFile)
            for key, values in allLineNumbersStatement.items():
                f.write(key)
                f.write(": ")
                for value in values:
                    f.write(value)
                    f.write(", ")    # will put comma after last value
                f.write("\n")
                # print("key, value")
                # print(key, value)

        allTakenNumbersBranch = branchCoverage(listDirBranch, openBranch)

        with open(branchLineNumberFile, 'w') as f:
            # print("branchLineNumberFile")
            # print(branchLineNumberFile)
            for key, values in allTakenNumbersBranch.items():
                f.write(key)
                f.write(": ")
                for value in values:
                    f.write(value)
                    f.write(", ")    # will put comma after last value
                f.write("\n")
                # print("key, value")
                # print(key, value)

        print("finished benchmark: " + str(benchmark) + ", elapsed time: ")
        print(time.time() - start)

    # print("\nallLineNumbersStatement")
    # for doing in allLineNumbersStatement:
    #     print(doing)
    #     print()

    # print("\nallTakenNumbersBranch")
    # for doing in allTakenNumbersBranch:
    #     print(doing)
    #     print()

    end = time.time()
    print("Total elapsed time: " + str(end - start))

    return

def statementCoverage(listDir, openBenchmark):
    # statement coverage -------------------------------------------------------------------------------------------------
    arr = os.listdir(listDir)
    lineNumbersStatement = []
    allLineNumbersStatement = dict()
    # testing = 0
    for file in arr:    # starts at 1000 file?
        # if testing > 20:
        #         break
        if "json" not in file:
            with open(openBenchmark + file) as f:
                lines = f.readlines()

            for line in lines:
                if ("#####" in line):
                    if (line[10] == " " and line[11] == " " and line[12] == " " and line[13] == " " and line[14] != " "):
                        lineNumbersStatement.append(str(line[14]))   # line number after hashtags (single number)
                    elif (line[10] == " " and line[11] == " " and line[12] == " " and line[13] != " " and line[14] != " "):
                        lineNumbersStatement.append(str(line[13]) + str(line[14]))   # line number after hashtags (tens)
                    elif (line[10] == " " and line[11] == " " and line[12] != " " and line[13] != " " and line[14] != " "):
                        lineNumbersStatement.append(str(line[12]) + str(line[13]) + str(line[14]))   # line number after hashtags (hundredds)
                    elif (line[10] == " " and line[11] != " " and line[12] != " " and line[13] != " " and line[14] != " "):
                        lineNumbersStatement.append(str(line[11]) + str(line[12]) + str(line[13]) + str(line[14]))   # line number after hashtags (thousands)
                    elif (line[10] != " " and line[11] != " " and line[12] != " " and line[13] != " " and line[14] != " "):
                        lineNumbersStatement.append(str(line[10]) + str(line[11]) + str(line[12]) + str(line[13]) + str(line[14]))   # line number after hashtags (ten thousands)
                        
                    allLineNumbersStatement[openBenchmark + file] = lineNumbersStatement
                    
        lineNumbersStatement = []   # reset lineNumbers for next file

        # testing = testing + 1

    return allLineNumbersStatement

def branchCoverage(listDir, openBenchmark):
    # branch coverage --------------------------------------------------------------------------------------------------
    arrBranch = os.listdir(listDir)
    takenNumbersBranch = []
    allTakenNumbersBranch = dict()
    # testingBranch = 0
    # branch
    for fileBranch in arrBranch:    # starts at 1000 file?
        # if testingBranch > 20:
        #         break
        if "json" not in fileBranch:
            with open(openBenchmark + fileBranch) as f:
                lines = f.readlines()

            for line in lines:
                if ("branch" in line):
                    if ("taken" in line):
                        # check if taken is multiple digits or not
                        valid16 = False
                        valid17 = False
                        valid18 = False
                        valid19 = False
                        valid20 = False
                        numLine16 = False
                        numLine17 = False
                        numLine18 = False
                        numLine19 = False
                        numLine20 = False

                        if (16 < len(line)):
                            valid16 = True
                        if (17 < len(line)):
                            valid17 = True
                        if (18 < len(line)):
                            valid18 = True
                        if (19 < len(line)):
                            valid19 = True
                        if (20 < len(line)):
                            valid20 = True

                        if (valid16):
                            if (line[16] == '0' or line[16] == '1' or line[16] == '2' or line[16] == '3' or line[16] == '4' or line[16] == '5' or line[16] == '6' or line[16] == '7' or line[16] =='8' or line[16] == '9'):
                                numLine16 = True
                        if (valid17):
                            if (line[17] == '0' or line[17] == '1' or line[17] == '2' or line[17] == '3' or line[17] == '4' or line[17] == '5' or line[17] == '6' or line[17] == '7' or line[17] =='8' or line[17] == '9'):
                                numLine17 = True
                        if (valid18):
                            if (line[18] == '0' or line[18] == '1' or line[18] == '2' or line[18] == '3' or line[18] == '4' or line[18] == '5' or line[18] == '6' or line[18] == '7' or line[18] =='8' or line[18] == '9'):
                                numLine18 = True
                        if (valid19):
                            if (line[19] == '0' or line[19] == '1' or line[19] == '2' or line[19] == '3' or line[19] == '4' or line[19] == '5' or line[19] == '6' or line[19] == '7' or line[19] =='8' or line[19] == '9'):
                                numLine19 = True
                        if (valid20):
                            if (line[20] == '0' or line[20] == '1' or line[20] == '2' or line[20] == '3' or line[20] == '4' or line[20] == '5' or line[20] == '6' or line[20] == '7' or line[20] =='8' or line[20] == '9'):
                                numLine20 = True

                        if (numLine16 and not numLine17 and not numLine18 and not numLine19 and not numLine20):
                            takenNumbersBranch.append(str(line[16]))   # number after taken (single number)
                            # print("append1")
                        elif (numLine16 and numLine17 and not numLine18 and not numLine19 and not numLine20):
                            takenNumbersBranch.append(str(line[16]) + str(line[17]))   # number after taken  (tens)
                            # print("append2")
                        elif (numLine16 and numLine17 and numLine18 and not numLine19 and not numLine20):
                            takenNumbersBranch.append(str(line[16]) + str(line[17]) + str(line[18]))   # number after taken  (hundredds)
                            # print("append3")
                        elif (numLine16 and numLine17 and numLine18 and numLine19 and not numLine20):
                            takenNumbersBranch.append(str(line[16]) + str(line[17]) + str(line[18]) + str(line[19]))   # number after taken  (thousands)
                            # print("append4")
                        elif (numLine16 and numLine17 and numLine18 and numLine19 and numLine20):
                            takenNumbersBranch.append(str(line[16]) + str(line[17]) + str(line[18]) + str(line[19]) + str(line[20]))   # number after taken  (ten thousands)
                            # print("append5")
                        # takenNumbersBranch.append(str(line[16]))   # taken number

                        # reset numLines
                        numLine16 = False
                        numLine17 = False
                        numLine18 = False
                        numLine19 = False
                        numLine20 = False
                        valid16 = False
                        valid17 = False
                        valid18 = False
                        valid19 = False
                        valid20 = False
                    elif ("never executed" in line):
                        takenNumbersBranch.append(str(0))   # never executed = 0

                    allTakenNumbersBranch[openBenchmark + fileBranch] = takenNumbersBranch

        takenNumbersBranch = []

        # testingBranch = testingBranch + 1

    return allTakenNumbersBranch

# def main():
#     print("bye")
#     testing = 0
#     # tcas
#     import os
#     arr = os.listdir("benchmarks/tcas/statementCoverage")
#     for file in arr:
#         if testing > 3:
#             break
#         if "json" in file:
#             jsonDict = getJsonFormatInfo("benchmarks/tcas/statementCoverage/" + file)
#             linesNotExecuted = []
#             for key, value in jsonDict.items():
#                 print(key, value)
#                 if (key == 'unexecuted_block'):
#                     if (value == True):
#                         linesNotExecuted.append(jsonDict['line_number'])
#                     # print(linesNotExecuted)
#         testing = testing + 1

#     print(linesNotExecuted)

            

#     # for file in os.listdir("benchmarks/tcas/statementCoverage"):
#     #     if (os.path.basename)
#     #     filename = os.path.basename("path/to/file/sample.txt")

#     return

# ## prioritization methods ------------------------------------------------------------------
# def randomize(benchmark):
#     import random

#     random.shuffle(benchmark)

#     return benchmark

# def total(testCases):
    

#     return

# def additional(testCases):
#     return

# def isRedundantTestCase(testCase, testCases):
#     finalList = testCases
#     if not (testCase in testCases):   # needs further testing
#         finalList.append(testCase)

#     return finalList

## -json-format info (rn working using --coverage option only) ---------------------------------------------------------------
# def getJsonFormatInfo(file):
#     #  convert json.gz to json
#     # import gzip
#     # import shutil
#     # with gzip.open(file, 'rb') as f_in:   #rb
#     #     with open('benchmarks/tcas/tcas.c.gcov.json', 'wb') as f_out:   #wb   # w also creates file
#     #         shutil.copyfileobj(f_in, f_out)

#     # get coverage info from json
#     with open(file) as f:   # with open('example.cpp.gcov.json') as f:
#             data = json.load(f)

#     # lines
#     branches = []
#     count = []
#     line_number = []
#     unexecuted_block = []
#     function_name = []

#     # functions
#     blocks = []
#     end_column = []
#     start_line = []
#     name = []
#     blocks_executed = []
#     execution_count = []
#     demangled_name = []
#     start_column = []
#     end_line = []

#     # file
#     filePath = []

#     # format_version, current_working_directory, data_file
#     format_version = []
#     current_working_directory = []
#     data_file = []

#     for key, value in data.items():
#         if (key == "files"):   # lines, functions, file
#             # print("\n found files")
#             if (value != []):
#                 for i in range(len(value)):
#                     for linesFunctionsFile, allPairs in value[i].items():
#                         # print("linesFunctionsFile")
#                         # print(linesFunctionsFile)
#                         if (linesFunctionsFile == "lines"):
#                             for pair in allPairs:
#                                 for key2, value2 in pair.items():
#                                     if (key2 == "branches"):
#                                         branches.append(value2)
#                                         # print("branchKey, branchVal")
#                                         # print(key2, value2)
#                                     elif (key2 == "count"):
#                                         count.append(value2)
#                                         # print("countKey, countVal")
#                                         # print(key2, value2)
#                                     elif (key2 == "line_number"):
#                                         line_number.append(value2)
#                                         # print("lineNumKey, lineNumVal")
#                                         # print(key2, value2)
#                                     elif (key2 == "unexecuted_block"):
#                                         unexecuted_block.append(value2)
#                                         # print("UnexecKey, UnexecVal")
#                                         # print(key2, value2)
#                                     elif (key2 == "function_name"):
#                                         function_name.append(value2)
#                                         # print("funcNameKey, funcNameVal")
#                                         # print(key2, value2)
#                                     # print()
#                         elif (linesFunctionsFile == "functions"):
#                             for pair in allPairs:
#                                 for key2, value2 in pair.items():
#                                     if (key2 == "blocks"):
#                                         blocks.append(value2)
#                                         # print("blocksKey, blocksVal")
#                                         # print(key2, value2)
#                                     elif (key2 == "end_column"):
#                                         end_column.append(value2)
#                                         # print("endColKey, endColVal")
#                                         # print(key2, value2)
#                                     elif (key2 == "start_line"):
#                                         start_line.append(value2)
#                                         # print("startLineKey, startLineVal")
#                                         # print(key2, value2)
#                                     elif (key2 == "name"):
#                                         name.append(value2)
#                                         # print("nameKey, nameVal")
#                                         # print(key2, value2)
#                                     elif (key2 == "blocks_executed"):
#                                         blocks_executed.append(value2)
#                                         # print("blocksExecKey, blocksExecVal")
#                                         # print(key2, value2)
#                                     elif (key2 == "execution_count"):
#                                         execution_count.append(value2)
#                                         # print("execCountKey, execCountVal")
#                                         # print(key2, value2)
#                                     elif (key2 == "demangled_name"):
#                                         demangled_name.append(value2)
#                                         # print("demangKey, demangVal")
#                                         # print(key2, value2)
#                                     elif (key2 == "start_column"):
#                                         start_column.append(value2)
#                                         # print("startColKey, startColVal")
#                                         # print(key2, value2)
#                                     elif (key2 == "end_line"):
#                                         end_line.append(value2)
#                                         # print("endLineKey, endColVal")
#                                         # print(key2, value2)
#                                     # print()
#                         elif (linesFunctionsFile == "file"):
#                             singleValue = allPairs
#                             filePath.append(singleValue)
#                             # print("singleValue")
#                             # print(singleValue)
#                         # print("\n")
#         else:   # format_version, current_working_directory, data_file
#             if (key == "format_version"):
#                 format_version.append(value)
#             elif (key == "current_working_directory"):
#                 current_working_directory.append(value)
#             elif (key == "data_file"):
#                 data_file.append(value)

#     # lines
#     # print("\n")
#     # print("branches")
#     # print(branches)
#     # print("count")
#     # print(count)
#     # print("line_number")
#     # print(line_number)
#     # print("unexecuted_block")
#     # print(unexecuted_block)
#     # print("function_name")
#     # print(function_name)

#     # # functions
#     # print("\n")
#     # print("blocks")
#     # print(blocks)
#     # print("len(blocks): " + str(len(blocks)))
#     # print("end_column")
#     # print(end_column)
#     # print("len(end_column): " + str(len(end_column)))
#     # print("start_line")
#     # print(start_line)
#     # print("len(start_line): " + str(len(start_line)))
#     # print("name")
#     # print(name)
#     # print("len(name): " + str(len(name)))
#     # print("blocks_executed")
#     # print(blocks_executed)
#     # print("len(blocks_executed): " + str(len(blocks_executed)))
#     # print("execution_count")
#     # print(execution_count)
#     # print("len(execution_count): " + str(len(execution_count)))
#     # print("demangled_name")
#     # print(demangled_name)
#     # print("len(demangled_name): " + str(len(demangled_name)))
#     # print("start_column")
#     # print(start_column)
#     # print("len(start_column): " + str(len(start_column)))
#     # print("end_line")
#     # print(end_line)
#     # print("len(end_line): " + str(len(end_line)))

#     # # file
#     # print("\n")
#     # print("filePath")
#     # print(filePath)
#     # print("len(filePath): " + str(len(filePath)))

#     # # format_version, current_working_directory, data_file
#     # print("\n")
#     # print("format_version")
#     # print(format_version)
#     # print("len(format_version): " + str(len(format_version)))
#     # print("current_working_directory")
#     # print(current_working_directory)
#     # print("len(current_working_directory): " + str(len(current_working_directory)))
#     # print("data_file")
#     # print(data_file)
#     # print("len(data_file): " + str(len(data_file)))

#     # return dict that contains all parsed info
#     d = dict(); 
#     d['branches'] = branches
#     d['count']   = count
#     d['line_number']   = line_number
#     d['unexecuted_block']   = unexecuted_block
#     d['function_name']   = function_name

#     d['blocks']   = blocks
#     d['end_column']   = end_column
#     d['start_line']   = start_line
#     d['name']   = name
#     d['blocks_executed']   = blocks_executed
#     d['execution_count']   = execution_count
#     d['demangled_name']   = demangled_name
#     d['start_column']   = start_column
#     d['end_line']   = end_line

#     d['filePath']   = filePath
    
#     d['format_version']   = format_version
#     d['current_working_directory']   = current_working_directory
#     d['data_file']   = data_file

#     return d

# main()
main2()