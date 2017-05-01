"""
Ninja Reverse Engineering of Android APK packages.

:author: Paolo Rovelli
:copyright: GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
"""

import argparse
from argparse import RawTextHelpFormatter
import json
import logging
import os
import re
import sys

from ninjadroid.use_cases.generate_apk_html_report import GenerateApkHtmlReport
from ninjadroid.use_cases.generate_apk_json_report import GenerateApkJsonReport
from ninjadroid.use_cases.extract_apk_entries import ExtractApkEntries
from ninjadroid.errors.apk_parsing_error import APKParsingError
from ninjadroid.errors.parsing_error import ParsingError
from ninjadroid.parsers.apk import APK


VERSION = "2.5"


# Initialise the logger:
logger = logging.getLogger("NinjaDroid")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter( logging.Formatter("  >> %(name)s: [%(levelname)s] %(message)s") )
logger.addHandler(ch)


def main():
    args = retrieve_commandline_parameters()
    apk = read_target_file(args.target, args.no_string_processing)
    if apk is not None:
        filename = get_apk_filename_without_extension(args.target)
        if args.extract_to_directory is None:
            dumps_apk_info(apk)
        else:
            extract_apk_info_to_directory(apk, args.target, filename, args.extract_to_directory)


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


def read_target_file(filepath: str, no_string_processing: bool):
    apk = None
    try:
        apk = APK(filepath, no_string_processing)
    except APKParsingError:
        logger.error("The target file (i.e. '" + filepath + "') must be an APK package!")
    except ParsingError:
        logger.error("The target file (i.e. '" + filepath + "') must be an existing, readable file!")
    return apk


def get_apk_filename_without_extension(filepath: str) -> str:
    filename = os.path.basename(filepath)
    if re.search("\.apk", filepath, re.IGNORECASE):
        filename = str(filename[0:-4])
    return filename


def extract_apk_info_to_directory(apk: APK, filepath: str, filename: str, output_directory: str):
    """
    Extract all the APK entries and info to a given directory.

    :param apk: The APK class object.
    :param filepath: The target APK file path.
    :param filename: The target APK file name.
    :param output_directory: The directory where to save the APK entries and info.
    """
    if output_directory == "./":
        output_directory += filename
    logger.info("Target: " + filepath)
    extract_apk_entries(apk, filepath, filename, output_directory)
    generate_apk_reports(apk, filename, output_directory)


def extract_apk_entries(apk: APK, filepath: str, filename: str, output_directory: str):
    ExtractApkEntries(apk, filepath, filename, output_directory, logger).execute()


def generate_apk_reports(apk: APK, filename: str, output_directory: str):
    GenerateApkHtmlReport(apk, filename, output_directory, logger).execute()
    GenerateApkJsonReport(apk, filename, output_directory, logger).execute()


def dumps_apk_info(apk: APK):
    apk_info = json.dumps(apk.dump(), sort_keys=True, ensure_ascii=False, indent=4)
    print(apk_info)


if __name__ == "__main__":
    sys.exit(main())
