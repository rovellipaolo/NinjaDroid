#!/usr/bin/env python3

"""
Ninja Reverse Engineering of Android APK packages.

:author: Paolo Rovelli
:copyright: GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
"""

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
import logging
import os
import re
import sys
from typing import Optional

from ninjadroid.use_cases.extract_certificate_file import ExtractCertificateFile
from ninjadroid.use_cases.extract_dex_file import ExtractDexFile
from ninjadroid.use_cases.generate_apk_info_report import GenerateApkInfoReport
from ninjadroid.use_cases.launch_apk_tool import LaunchApkTool
from ninjadroid.use_cases.launch_dex2jar import LaunchDex2Jar
from ninjadroid.use_cases.print_apk_info import PrintApkInfo
from ninjadroid.errors.apk_parsing_error import APKParsingError
from ninjadroid.errors.parsing_error import ParsingError
from ninjadroid.parsers.apk import APK


VERSION = "4.0"


logging.basicConfig(
    format="  >> %(name)s: [%(levelname)s] %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("NinjaDroid")


def main():
    args = get_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    apk = read_file(args.target, args.extended_processing)
    if apk is None:
        return 1

    filename = get_filename_without_extension(args.target)
    if args.output_directory is None:
        PrintApkInfo().execute(apk, as_json=args.json)
    else:
        output_directory = setup_output_directory(args.output_directory, filename)
        LaunchApkTool(logger).execute(args.target, output_directory)
        LaunchDex2Jar(logger).execute(args.target, filename, output_directory)
        ExtractCertificateFile(logger).execute(apk, output_directory)
        ExtractDexFile(logger).execute(apk, output_directory)
        GenerateApkInfoReport(logger).execute(apk, filename, output_directory)
    return 0


def get_args() -> Namespace:
    parser = ArgumentParser(
        description="examples: \n"
                    "  >> %(prog)s /path/to/file.apk\n"
                    "  >> %(prog)s /path/to/file.apk --all\n"
                    "  >> %(prog)s /path/to/file.apk --all --json\n"
                    "  >> %(prog)s /path/to/file.apk --all --extract\n"
                    "  >> %(prog)s /path/to/file.apk --all --extract /path/to/output/directory/\n",
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        "target",
        metavar="TARGET_FILE",
        type=str,
        help="the APK package to analyse"
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        dest="extended_processing",
        help="retrieve and show all the information, only a summary otherwise"
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        dest="json",
        help="show the output in JSON format"
    )
    parser.add_argument(
        "-e",
        "--extract",
        type=str,
        nargs="?",
        const="./",
        action="store",
        dest="output_directory",
        help="extract and store all the APK entries and information retrieved into a given folder (default: './')\n"
             "NOTE: this will automatically force the -j / --json option"
    )
    parser.add_argument(
        "-d",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="show verbose logs"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="NinjaDroid {0}".format(VERSION),
        help="show version"
    )
    return parser.parse_args()


def read_file(filepath: str, extended_processing: bool) -> Optional[APK]:
    apk = None
    logger.debug("Reading %s...", filepath)
    try:
        apk = APK(filepath, extended_processing, logger)
    except APKParsingError:
        logger.error("The target file ('%s') must be an APK package!", filepath)
    except ParsingError:
        logger.error("The target file ('%s') must be an existing, readable file!", filepath)
    return apk


def get_filename_without_extension(filepath: str) -> str:
    filename = os.path.basename(filepath)
    if re.search("\\.apk", filepath, re.IGNORECASE):
        filename = str(filename[0:-4])
    return filename


def setup_output_directory(filepath: str, filename: str) -> str:
    if filepath == "./":
        filepath += filename
    else:
        filepath = filepath.rstrip("/")
    if not os.path.exists(filepath):
        logger.info("Creating %s/...", filepath)
        os.makedirs(filepath)
    return filepath


if __name__ == "__main__":
    sys.exit(main())
