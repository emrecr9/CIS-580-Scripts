import subprocess
import os
import git
import pandas as pd

fileContent = subprocess.run("ls", capture_output=True, text=True)

listFiles = str(fileContent.stdout).split("\n")

changedFilesContent = subprocess.run("git diff --numstat head", capture_output=True, text=True)

fileLinesChanges = [line for line in str(changedFilesContent.stdout).strip().split("\n")]

fileChangedDirectories = [directory[2] for directory in [line.split("\t") for line in fileLinesChanges]]

numTestFiles = 0

for fileChanged in fileChangedDirectories:
    diffContent = subprocess.run("git diff head %s" % fileChanged, capture_output=True, text=True)

    if str(diffContent.stdout).__contains__("@Test"):
        numTestFiles += 1


def runEvosuite(repository_directory, classdirectory):

    if not (os.path.isfile("runGradle.cmd")):
        cmdf = open("runGradle.cmd", "w+")
        cmdf.write("gradlew build\n")
        cmdf.close()
        subprocess.call([r'runGradle.cmd'])

    cmd = open("runEvosuite.cmd", "w+")
    cmd.write("cd \"" + ".git\CIS-580-Scripts-main\Tools" + "\"\n")
    cmd.write("java -jar evosuite.jar -target " + " \"" + repository_directory + classdirectory + "\"")
    cmd.close()

    subprocess.call([r'runEvosuite.cmd'])

    if os.path.isfile("runEvosuite.cmd"):
        os.remove("runEvosuite.cmd")


def checkCoverage(repository_directory, classdirectory):
    coverage = 0.0
    #   repository_directory = git.Repo('.', search_parent_directories=True).working_tree_dir

    if not (os.path.isfile("runGradle.cmd")):
        cmdf = open("runGradle.cmd", "w+")
        cmdf.write("gradlew build\n")
        cmdf.close()

    cmd = open("runCoverage.cmd", "w+")
    cmd.write("cd \"" + ".git\CIS-580-Scripts-main\Tools" + "\"\n")
    cmd.write(
        "java -jar jacococli.jar report --classfiles " + " \"" + repository_directory + classdirectory + "\" --csv \""
        + repository_directory + "\\coverageReport.csv\"")
    cmd.close()

    subprocess.call([r'runGradle.cmd'])
    subprocess.call([r'runCoverage.cmd'])

    if os.path.isfile("runCoverage.cmd"):
        os.remove("runCoverage.cmd")
        os.remove("runGradle.cmd")

        if os.path.isfile("coverageReport.csv"):
            cf = pd.read_csv(repository_directory + '\\coverageReport.csv')
            coverageList = cf.BRANCH_COVERED.tolist()

            for c in coverageList:
                coverage = c + coverage

            if (len(coverageList) > 0):
                coverage = coverage / len(coverageList)

        else:
            print("Unable to determine the coverage")

    return coverage


repository_directory = git.Repo('.', search_parent_directories=True).working_tree_dir

if os.path.exists('./src'):
    path = '\\src'
else:
    path = ''

if numTestFiles == 0:
    print("Your changes do not contain any tests\nTests will now be automatically generated")
    runEvosuite(repository_directory, path)
    checkCoverage(repository_directory, path)
else:
    print("The changes have been tested")

    if checkCoverage(repository_directory, path) < 50:
        print('The code coverage test is low (below 50)\nTest cases will now be automatically generated')
        runEvosuite(repository_directory, path)
