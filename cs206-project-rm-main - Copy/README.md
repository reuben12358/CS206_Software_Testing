# cs206-project-rm
cs206-project-rm created by GitHub Classroom

I used Python 3 for this project.

Please download the natsort library.
- sudo apt-get install python3-pip
- pip install natsort

Please copy paste any necessary folders that a benchmark needs into each faulty benchmark folder.
For example, for printtokens, please copy paste the "inputs" folder into folders v1, v2, v3, v4, v5, v6, and v7.

Location of test suites: "benchmarks/[benchmark]/[randomized/total/additiona][Statement/Branch]TestSuite.txt"


Please run the following files in the order given:

createGcovsJsons.py: creates gcov and json files for each benchmark in folder “benchmarks/[benchmark]/[statement/branch]Coverage”
- python3 createGcovsJsons.py

statementBranchCoverage.py: lists test cases with associated coverage for each benchmark in folder “benchmarks/[benchmark]/[statement/branch]CoverageLineNumbers/lineNumbers.txt”
- python3 statementBranchCoverage.py

orderedLineNumberTestCases.py: lists test cases with associated test case and associated coverage in folder “benchmarks/[benchmark]/[statement/branch]CoverageLineNumbers/2ordered[Statement/Branch]LineNumberTestCases.txt”
- python3 orderedLineNumberTestCases.py

testSuites.py: lists coverage for random, total, and additional test prioritization methods in folder “benchmarks/[benchmark]/[statement/branch]CoverageLineNumbers/[randomized/total/additional][Statement/Branch]TestSuite.txt”
- python3 testSuites.py

faultyTests.py: lists number of faults exposed by a test suite in folder “benchmarks/[benchmark]/[statement/branch]CoverageLineNumbers/[randomized/total/additional]Fails.txt”
- python3 faultyTests.py

datatable.py: lists the test cases, the size of the test suite, and the number of faults exposed for each test suite in folder “benchmarks/[benchmark]/[statement/branch]CoverageLineNumbers/[randomized/total/additional][Statement/Branch]Datatable.txt”
- python3 datatable.py
