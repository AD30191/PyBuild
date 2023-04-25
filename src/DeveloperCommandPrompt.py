import os

# A shortcut to the Developer Command Prompt for runnings msvc C++ tools on the command line
# Was initially going to do this along with the build process but had no idea how to return control to the script
# after the prompt was opened.

# So, just run this and then run the Build.py script inside the opened terminal.

# It should work for a fresh intstall of visual studio or the build tools.

def main():
    os.chdir("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio 2022\\Visual Studio Tools\\VC")
    os.system('"x64 Native Tools Command Prompt for VS 2022.lnk"')


if __name__ == "__main__":
    main()
