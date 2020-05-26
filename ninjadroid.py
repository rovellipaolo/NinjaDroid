#!/usr/bin/env python3

"""
Ninja Reverse Engineering of Android APK packages.

:author: Paolo Rovelli
:copyright: GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
"""

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
import json
import logging
import os
import re
import sys
from typing import Optional

from ninjadroid.use_cases.extract_certificate_file import ExtractCertificateFile
from ninjadroid.use_cases.extract_dex_file import ExtractDexFile
from ninjadroid.use_cases.get_apk_info_in_html import GetApkInfoInHtml
from ninjadroid.use_cases.get_apk_info_in_json import GetApkInfoInJson
from ninjadroid.use_cases.launch_apk_tool import LaunchApkTool
from ninjadroid.use_cases.launch_dex2jar import LaunchDex2Jar
from ninjadroid.errors.apk_parsing_error import APKParsingError
from ninjadroid.errors.parsing_error import ParsingError
from ninjadroid.parsers.apk import APK


VERSION = "3.0"


logging.basicConfig(
    format="  >> %(name)s: [%(levelname)s] %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("NinjaDroid")


def main():
    args = get_args()
    apk = read_target_file(args.target, args.no_string_processing)

    if apk is None:
        sys.exit(1)

    filename = get_apk_filename_without_extension(args.target)
    if args.extract_to_directory is None:
        print_apk_info(apk)
    else:
        extract_apk_info_to_directory(apk, args.target, filename, args.extract_to_directory)


def get_args() -> Namespace:
    parser = ArgumentParser(
        description="examples: \n"
                    "  >> %(prog)s /path/to/input.apk\n"
                    "  >> %(prog)s /path/to/input.apk --no-string-processing\n"
                    "  >> %(prog)s /path/to/input.apk --extract\n"
                    "  >> %(prog)s /path/to/input.apk --extract /path/to/output/\n"
                    "  >> %(prog)s /path/to/input.apk --extract /path/to/output/ --no-string-processing\n"
                    "  >> %(prog)s --version\n"
                    "  >> %(prog)s --help",
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        "target",
        metavar="TARGET_FILE",
        type=str,
        help="The targeted APK package to analyse."
    )
    parser.add_argument(
        "-e",
        "--extract",
        type=str,
        nargs="?",
        const="./",
        action="store",
        dest="extract_to_directory",
        help="Extract and store all the APK entries and info in a given folder (default: ./APK)."
    )
    parser.add_argument(
        "-ns",
        "--no-string-processing",
        action="store_false",
        dest="no_string_processing",
        help="If set the URLs and shell commands in the classes.dex will not be extracted."
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="NinjaDroid " + VERSION,
        help="Show program's version and number."
    )
    return parser.parse_args()


def read_target_file(filepath: str, no_string_processing: bool) -> Optional[APK]:
    apk = None
    logger.info("Reading %s...", filepath)
    try:
        apk = APK(filepath, no_string_processing)
    except APKParsingError:
        logger.error("The target file ('%s') must be an APK package!", filepath)
    except ParsingError:
        logger.error("The target file ('%s') must be an existing, readable file!", filepath)
    return apk


def get_apk_filename_without_extension(filepath: str) -> str:
    filename = os.path.basename(filepath)
    if re.search("\\.apk", filepath, re.IGNORECASE):
        filename = str(filename[0:-4])
    return filename


def print_apk_info(apk: APK):
    apk_info = json.dumps(apk.dump(), sort_keys=True, ensure_ascii=False, indent=4)
    print(apk_info)


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
    create_output_directory_if_needed(output_directory)
    LaunchApkTool(logger).execute(input_filepath=filepath, output_directory=output_directory)
    LaunchDex2Jar(logger).execute(input_filepath=filepath, input_filename=filename, output_directory=output_directory)
    ExtractCertificateFile(logger).execute(apk=apk, output_directory=output_directory)
    ExtractDexFile(logger).execute(apk=apk, output_directory=output_directory)
    GetApkInfoInHtml(logger).execute(apk=apk, input_filename=filename, output_directory=output_directory)
    GetApkInfoInJson(logger).execute(apk=apk, input_filename=filename, output_directory=output_directory)


def create_output_directory_if_needed(output_directory: str):
    if not os.path.exists(output_directory):
        logger.info("Creating %s/...", output_directory)
        os.makedirs(output_directory)


if __name__ == "__main__":
    sys.exit(main())
