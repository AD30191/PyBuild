import os
import re
import sys

# DISCLAIMER: This is a toy-project. I'm using Windows 10, x64 on a pre-built acer and
# ubuntu by using wsl2.
# This is a very strict build script using the most basic way to build an app
# or library without any useful or even potentially needed compiler/linker options
# This is essentially built for toy-projects that aren't meant to be in a
# production / commercial setting. There are many, many other great build tools for
# those purposes.

# P.S. I realize I could refactor a bunch of functions (and the code therein) out of this main fuction 
# and then actually be able to unit-test them but I have a bunch of other projects I want to get to :P.

# P.S.2. No testing at the moment has been done for this script on a Linux environment. So, it likely doesn't work on Linux.


def main():
    # I'm using compiler as a catch-all term
    operating_system = ""
    gcc_compiler = ""
    msvc_compiler = ""
    formatted_files = ""

    # To link with libraries the build process needs to be broken down into
    # it's individual phases for gcc
    formatted_s_files = ""
    formatted_o_files = ""
    formatted_sl_files = ""
    formatted_dl_files = ""

    # Get os
    if sys.platform.startswith("linux"):
        operating_system = operating_system + "linux"
    elif sys.platform.startswith("win32"):
        operating_system = operating_system + "win32"

    # gcc can, obviously, be used on windows - but after some digging on how to
    # create static/dynamic libraries for gcc on windows I realized I was better
    # off sticking to msvc for windows and gcc for linux strictly.
    # May add gcc option for windows later as compiling and linking already created
    # libraries shouldn't be too difficult
    if operating_system == "linux":
        gcc_compiler = "gcc"
    elif operating_system == "win32":
        msvc_compiler = "msvc"
    elif operating_system == "":
        exit("Invalid operating system use windows or linux to run this script.")

    # Self-explanatory
    app_or_lib = input("Build an application[0] or library[1]: ")

    # Get src directory
    directory = input("Enter path to src folder: ")
    print("OK")

    # Change directory to source directory
    os.chdir(directory)

    # formatted_files are going to have a few variants as file
    # extensions are different depending on the language and compiler used
    if msvc_compiler == "msvc":
        # msvc C++ on windows variant
        # Put files at directory into string formatted correctly
        for file in os.listdir(directory):
            if re.search(".cpp", file) or re.search(".lib", file) is not None:
                formatted_files = formatted_files + file
                formatted_files = formatted_files + " "
            else:
                continue
        print(formatted_files)
        print("OK")
    elif gcc_compiler == "gcc":
        # gcc on linux variant
        # Put files at directory into string formatted correctly
        for file in os.listdir(directory):
            if re.search(".cpp", file) is not None:
                formatted_s_files = formatted_s_files + file
                formatted_s_files = formatted_s_files + " "
            else:
                continue

            if re.search(".a", file) is not None:
                formatted_sl_files = formatted_sl_files + file
                formatted_sl_files = formatted_sl_files + " "
            else:
                continue

            if re.search(".so", file) is not None:
                formatted_dl_files = formatted_dl_files + file
                formatted_dl_files = formatted_dl_files + " "
            else:
                continue
        print(formatted_files)
        print("OK")

    # Generate command to compile and link depending on compiler
    if msvc_compiler == "msvc" and app_or_lib == 0:
        # Generate command to compile and link src directory for Windows msvc
        os.system("cl /W4 /EHsc " + formatted_files + " /link /out:app.exe")
        print("OK")
    elif gcc_compiler == "gcc":
        # This command needs MAJOR testing
        # Generate command to compile and link src directory for linux gcc g++
        os.system("g++ -c " + formatted_s_files)
        
        # .o files only available after compilation has occurred... so I put them in a string right after they become available
        for file in os.listdir(directory):
            if re.search(".o", file) is not None:
                formatted_o_files = formatted_o_files + file
                formatted_o_files = formatted_o_files + " "

        os.system("g++ " + formatted_o_files + " -o app -Wl,-Bstatic " + formatted_sl_files + " -Wl,-Bdynamic " + formatted_dl_files)


if __name__ == "__main__":
    main()
