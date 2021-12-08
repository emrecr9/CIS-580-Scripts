import os
import git
import subprocess

repository_directory= git.Repo('.', search_parent_directories=True).working_tree_dir

cmd = open("runDesignite.cmd","w+")
cmd.write("cd \"" + ".git\CIS-580-Scripts-main\Tools" + "\"\n")
cmd.write("java -jar DesigniteJava.jar -i " +" \"" + repository_directory + "\"  -o " + " \"" + repository_directory + "\\codeSmellsResults\"\n")
cmd.close()

subprocess.call([r'runDesignite.cmd'])

if os.path.isfile("runDesignite.cmd"):
    os.remove("runDesignite.cmd")
