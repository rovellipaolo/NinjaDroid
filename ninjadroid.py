##
# Ninja Reverse Engineering of Android APK packages.
#
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#

import argparse
from argparse import RawTextHelpFormatter
import json
import logging
import os
import re
import subprocess
import sys
from time import sleep

from lib.errors.APKParsingError import APKParsingError
from lib.errors.ParsingError import ParsingError
from lib.parsers.APK import APK
from lib.Report import Report


VERSION = "2.5"


# Initialise the logger:
logger = logging.getLogger("NinjaDroid")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter( logging.Formatter("  >> %(name)s: [%(levelname)s] %(message)s") )
logger.addHandler(ch)


APKTOOL = "lib/apktool1.5.2/apktool.jar"
DEX2JAR = "lib/dex2jar-0.0.9.15/d2j-dex2jar.sh"


def main(argv=None):
    args = retrieve_commandline_parameters()
    apk = read_target_file(args.target, args.no_string_processing)
    if apk is not None:
        filename = get_apk_filename_without_extension(args.target)
        if args.extract_to_directory is None:
            dumps_apk_info(apk)
        else:
            extract_apk_info_to_directory(args.extract_to_directory, args.target, filename, apk)


def retrieve_commandline_parameters():
    parser = argparse.ArgumentParser(description="NinjaDroid description: \n"
                                                 "  >> %(prog)s /path/to/file.apk\n"
                                                 "  >> %(prog)s --no-string-processing /path/to/file.apk\n"
                                                 "  >> %(prog)s /path/to/file.apk --extract\n"
                                                 "  >> %(prog)s --no-string-processing /path/to/file.apk --extract\n"
                                                 "  >> %(prog)s /path/to/file.apk --extract /dir/where/to/store/info/\n"
                                                 "  >> %(prog)s --version\n"
                                                 "  >> %(prog)s --help",
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument("target", metavar="TARGET_FILE", type=str,
                        help="The targeted APK package to analyse.")
    parser.add_argument("-e", "--extract", type=str, nargs="?", const="./", action="store", dest="extract_to_directory",
                        help="Extract and store all the APK entries and info in a given folder (default: ./APK).")
    parser.add_argument("-ns", "--no-string-processing", action="store_false", dest="no_string_processing",
                        help="If set the URLs and shell commands in the classes.dex will not be extracted.")
    parser.add_argument("-v", "--version", action="version", version="NinjaDroid " + VERSION,
                        help="Show program's version and number.")
    return parser.parse_args()


def read_target_file(filepath, no_string_processing):
    apk = None
    try:
        apk = APK(filepath, no_string_processing)
    except APKParsingError:
        logger.error("The target file (i.e. '" + filepath + "') must be an APK package!")
    except ParsingError:
        logger.error("The target file (i.e. '" + filepath + "') must be an existing, readable file!")
    return apk


def get_apk_filename_without_extension(filepath):
    filename = os.path.basename(filepath)
    if re.search("\.apk", filepath, re.IGNORECASE):
        filename = str(filename[0:-4])
    return filename


##
# Extract all the APK entries and info to a given directory.
#
# @param output_dir  The directory where to save the APK entries and info.
# @param filepath  The target APK file path.
# @param filename  The target APK file name.
# @param apk  The APK class object.
#
def extract_apk_info_to_directory(output_dir, filepath, filename, apk):
    if output_dir == "./":
        output_dir += filename
    logger.info("Target: " + filepath)
    create_output_directory_if_needed(output_dir)
    launch_apktool(output_dir, filepath)
    # Give apktool some time:
    sleep(1)
    launch_dex2jar(output_dir, filepath, filename)
    # Give dex2jar some time:
    sleep(5)
    extract_certificate_file(output_dir, apk)
    extract_dex_file(output_dir, apk)
    generate_report(output_dir, filename, apk)


def create_output_directory_if_needed(output_dir):
    if not os.path.exists(output_dir):
        logger.info("Creating " + output_dir + "/...")
        os.makedirs(output_dir)


##
# Launch apktool.
# Apktool will extract the (decrypted) AndroidManifest.xml, the resources and to generate the disassembled smali files.
#
def launch_apktool(output_dir, filepath):
    logger.info("Creating " + output_dir + "/smali/...")
    logger.info("Creating " + output_dir + "/AndroidManifest.xml...")
    logger.info("Creating " + output_dir + "/res/...")
    logger.info("Creating " + output_dir + "/assets/...")
    command = "java -jar " + APKTOOL + " -q d -f " + filepath + " " + output_dir
    launch_shell_command(command)


##
# Launch dex2jar.
# Dex2jar will generate a jar file from the classes.dex.
#
def launch_dex2jar(output_dir, filepath, filename):
    jarfile = filename + ".jar"
    logger.info("Creating " + output_dir + "/" + jarfile + "...")
    command = DEX2JAR + " -f " + filepath + " -o " + output_dir + "/" + jarfile
    launch_shell_command(command)


def launch_shell_command(command):
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)


##
# Extract CERT.RSA/DSA file.
#
def extract_certificate_file(output_dir, apk):
    logger.info("Creating " + output_dir + "/CERT.RSA...")
    apk.extract_cert_file(output_dir)


##
# Extract classes.dex file.
#
def extract_dex_file(output_dir, apk):
    logger.info("Creating " + output_dir + "/classes.dex...")
    apk.extract_dex_file(output_dir)


##
# Generate the JSON and HTML report files.
#
def generate_report(output_dir, filename, apk):
    report_filename = "report-" + filename
    generate_json_report(output_dir, report_filename, apk)
    generate_html_report(output_dir, report_filename, apk)


def generate_json_report(output_dir, filename, apk):
    logger.info("Creating " + output_dir + "/" + filename + ".json...")
    fp = open(os.path.join(output_dir, filename + ".json"), "w")
    apk_info = get_apk_info_in_json_format()
    fp.write(apk_info)
    fp.close()


def generate_html_report(output_dir, filename, apk):
    logger.info("Creating " + output_dir + "/" + filename + ".html...")
    fp = open(os.path.join(output_dir, filename + ".html"), "w")
    apk_info = Report.generate_html_report(apk)
    fp.write(apk_info)
    fp.close()


def dumps_apk_info(apk):
    apk_info = get_apk_info_in_json_format(apk)
    print(apk_info)


def get_apk_info_in_json_format(apk):
    return json.dumps(apk.dump(), sort_keys=True, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    sys.exit(main())
