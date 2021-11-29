import sys
import urllib.request as request
import shutil
import zipfile
import os
import subprocess

if len(sys.argv) != 2:
    print("----- Usage: python install <Directory of your project> --------")
    exit(0)

path = sys.argv[1]

os.chdir(path)

print("Downloading scripts from github......")
url = "https://github.com/emrecr9/CIS-580-Scripts/archive/refs/heads/main.zip"
file_name = "main.zip"

request.urlretrieve(url,file_name)

print("Unzipping files......")
shutil.unpack_archive("main.zip",".git")
os.remove("main.zip")
print("Installing scripts......")
exec(open(".git/CIS-580-Scripts-main/scripts_installer.py").read())
