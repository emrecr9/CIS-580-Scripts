import subprocess

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

def runEvosuite():
    import os
    import git

def checkCoverage():
    import os

if numTestFiles == 0:
    print("Your changes do not contain any tests\nTests will now be automatically generated")
    runEvosuite()
else:
    print("The changes have been tested")

checkCoverage()


