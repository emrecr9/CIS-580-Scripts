import os

with open("./.git/hooks/pre-commit","w") as file:
    file.write("#!/bin/bash\n")
    file.write("python ./.git/CIS-580-Scripts-main/pre-commit/code_smells.py\n")
    file.write("python ./.git/CIS-580-Scripts-main/pre-commit/test_script.py\n")
