##
# @file ninjadroid.py
# @brief Ninja Reverse Engineering of Android APK packages.
# @version 2.0
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
# 
# Example calls:
# > python ninjadroid.py MyPackage.apk
# > python ninjadroid.py /path/to/MyPackage.apk
# > python ninjadroid.py /path/to/MyPackage.apk --extract
# > python ninjadroid.py /path/to/MyPackage.apk --extract /dir/where/to/extract/
# > python ninjadroid.py --no-string-process /path/to/MyPackage.apk
# > python ninjadroid.py --no-string-process /path/to/MyPackage.apk --extract
#


VERSION = "2.0"


import argparse
from argparse import RawTextHelpFormatter
import json
import logging
import os
import re
import subprocess
import sys
from time import sleep

from lib.APK import APK, ErrorAPKParsing
from lib.File import ErrorFileParsing
from lib.Report import Report


# Initialise the logger:
logger = logging.getLogger("NinjaDroid")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()  # console handler for the logger
ch.setLevel(logging.INFO)
ch.setFormatter( logging.Formatter("  >> %(name)s: [%(levelname)s] %(message)s") )  # log message format
logger.addHandler(ch)  # add the handler to the logger


APKTOOL = "lib/apktool1.5.2/apktool.jar"
DEX2JAR = "lib/dex2jar-0.0.9.15/d2j-dex2jar.sh"


def main(argv=None):
    # Retrieve command-line parameters:
    parser = argparse.ArgumentParser(description="NinjaDroid description: \n"
                                                 "  >> %(prog)s /path/to/file.apk\n"
                                                 "  >> %(prog)s --no-string-processing /path/to/file.apk\n"
                                                 "  >> %(prog)s /path/to/file.apk --extract\n"
                                                 "  >> %(prog)s --no-string-processing /path/to/file.apk --extract\n"
                                                 "  >> %(prog)s /path/to/file.apk --extract /dir/where/to/save/APK/info/\n"
                                                 "  >> %(prog)s --version\n"
                                                 "  >> %(prog)s --help",
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument("target", metavar="TARGET_FILE", type=str, help="The targeted APK package to analyse.")
    parser.add_argument("-e", "--extract", type=str, nargs="?", const="./", action="store", dest="extract_to_directory", help="Extract and store all the APK entries as well as it info in a given folder (default: ./APK).")
    parser.add_argument("-ns", "--no-string-processing", action="store_false", dest="no_string_processing", help="If set the URLs and shell commands in the classes.dex will not be extracted. This will make the process faster.")
    parser.add_argument("-v", "--version", action="version", version="NinjaDroid " + VERSION, help="Show program's version and number.")

    args = parser.parse_args()

    # Read the target file:
    try:
        apk = APK(args.target, args.no_string_processing)
    except ErrorFileParsing:
        logger.error("The target file (i.e. '" + args.target + "') must be an existing, readable file!")
        sys.exit()
    except ErrorAPKParsing:
        logger.error("The target file (i.e. '" + args.target + "') must be an APK package!")
        sys.exit()

    # Extract the APK file name (without extension):
    filename = os.path.basename(args.target)
    if re.search("\.apk", args.target, re.IGNORECASE):
        filename = str(filename[0:-4])

    if args.extract_to_directory is not None:
        # Extract all the APK entries and info to a given directory:
        dir = args.extract_to_directory

        # Check whether no output directory was given (i.e. the default one):
        if args.extract_to_directory == "./":
            dir += filename

        extract_all(dir, args.target, filename, apk)
    else:
        # Print the APK info to STDOUT (in JSON format):
        print(json.dumps(apk.dump(), sort_keys=True, ensure_ascii=False, indent=4))


##
# Extract all APK entries and info to a given directory.
#
# @param output_dir  The directory where to save the APK entries and info.
# @param filepath  The target APK file path.
# @param filename  The target APK file name.
# @param apk  The APK class object.
#
def extract_all(output_dir, filepath, filename, apk):
    logger.info("Target: " + filepath)

    # Check whether the output folder exists:
    if not os.path.exists(output_dir):
        logger.info("Creating " + output_dir + "/...")
        os.makedirs(output_dir)

    # Launch apktool in order to extract the (decrypted) AndroidManifest.xml, the resources and to generate the disassembled smali files:
    logger.info("Creating " + output_dir + "/smali/...")
    logger.info("Creating " + output_dir + "/AndroidManifest.xml...")
    logger.info("Creating " + output_dir + "/res/...")
    logger.info("Creating " + output_dir + "/assets/...")
    subprocess.Popen("java -jar " + APKTOOL + " -q d -f " + filepath + " " + output_dir, stdout=subprocess.PIPE, stderr=None, shell=True)

    sleep(1)

    # Launch dex2jar in order to generate a jar file from the classes.dex:
    jarfile = filename + ".jar"
    logger.info("Creating " + output_dir + "/" + jarfile + "...")
    subprocess.Popen(DEX2JAR + " -f " + filepath + " -o " + output_dir + "/" + jarfile, stdout=subprocess.PIPE, stderr=None, shell=True)

    sleep(5)

    # Extract CERT.RSA/DSA and classes.dex file:
    logger.info("Creating " + output_dir + "/CERT.RSA...")
    apk.extract_cert_file(output_dir)
    logger.info("Creating " + output_dir + "/classes.dex...")
    apk.extract_dex_file(output_dir)

    report_file_name = "report-" + filename

    # Generate the JSON report file:
    logger.info("Creating " + output_dir + "/" + report_file_name + ".json...")
    fp = open(os.path.join(output_dir, report_file_name + ".json"), "w")
    fp.write(json.dumps(apk.dump(), sort_keys=True, ensure_ascii=False, indent=4))
    fp.close()

    # Generate the HTML report file:
    logger.info("Creating " + output_dir + "/" + report_file_name + ".html...")
    fp = open(os.path.join(output_dir, report_file_name + ".html"), "w")
    fp.write(Report.generate_html_report(apk))
    fp.close()


if __name__ == "__main__":
    sys.exit(main())
