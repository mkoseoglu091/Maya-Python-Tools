import argparse
import re
import os
import shutil


def main():
    parser = argparse.ArgumentParser(description="This is a simple batch renaming tool to rename sequences of files",
                                     usage="To replace all files with hello with goodbye: python renamer.py hello goodbye")
    parser.add_argument('inString', help="The word or regex pattern to replace")
    parser.add_argument('outString',help="The word or regex pattern to replace it with")
    parser.add_argument('-d', '--duplicate', help="Should we duplicate or write over the original files", action='store_true')
    parser.add_argument('-r', '--regex', help="Whether the inputs will be using regex or not", action='store_true')

    parser.add_argument('-o', '--out', help="The location to deposit these files. Defaults to this directory")

    args = parser.parse_args()

    rename(args.inString, args.outString, duplicate=args.duplicate,
           outDir=args.out, regex=args.regex)


def rename(inString, outString, duplicate=True, inDir=None, outDir=None, regex=False):

    if not inDir:
        inDir = os.getcwd()

    if not outDir:
        outDir = inDir

    outDir = os.path.abspath(outDir)

    if not os.path.exists(outDir):
        raise IOError("%s does not exist!" % outDir)
    if not os.path.exists(inDir):
        raise IOError("%s does not exist!" % inDir)

    for f in os.listdir(inDir):
        if f.startswith('.'):
            continue

        if regex:
            name = re.sub(inString, outString, f)
        else:
            name = f.replace(inString, outString)

        if name == f:
            continue

        src = os.path.join(inDir, f)
        dest = os.path.join(outDir, name)

        if duplicate:
            shutil.copy2(src, dest)
        else:
            os.rename(src, dest)


if __name__ == '__main__':
    main()
