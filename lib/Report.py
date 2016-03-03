##
# @file Report.py
# @brief Generate n HTML report of a specific app.
# @version 2.0
# @author Paolo Rovelli
# @copyright GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl.html).
#


class Report(object):
    ##
    # Generate the analysis report in HTML format.
    #
    # @param apk  The APK instance.
    #
    @staticmethod
    def generate_html_report(apk):
        man = apk.get_manifest()
        cert = apk.get_cert()
        dex = apk.get_dex()

        # Header:
        report = "<html>" + "\n"
        report += "\t<table border=\"0\" cellspacing=\"0\" cellpadding=\"2\">" + "\n"

        # APK file summary:
        report += "\t\t<tr style='font-size: 120%; font-weight: bold;'>" + "\n"
        report += "\t\t\t<td colspan=\"2\" style=\"background: #2F2F2F; color: #FFFFFF; text-align: center;\">SUMMARY</td>" + "\n"
        report += "\t\t</tr>" + "\n"
        report += "\t\t<tr>" + "\n"
        report += "\t\t\t<td>File:</td>" + "\n"
        report += "\t\t\t<td style=\"font-weight: bold;\">" + apk.get_file_name() + "</td>" + "\n"
        report += "\t\t</tr>" + "\n"
        report += "\t\t<tr>" + "\n"
        report += "\t\t\t<td>File size:</td>" + "\n"
        report += "\t\t\t<td style=\"font-weight: bold;\">" + str(apk.get_size()) + " Bytes</td>" + "\n"
        report += "\t\t</tr>" + "\n"
        report += "\t\t<tr>" + "\n"
        report += "\t\t\t<td>File MD5:</td>" + "\n"
        report += "\t\t\t<td style=\"font-weight: bold;\">" + apk.get_md5() + "</td>" + "\n"
        report += "\t\t</tr>" + "\n"
        report += "\t\t<tr>" + "\n"
        report += "\t\t\t<td>File SHA-1:</td>" + "\n"
        report += "\t\t\t<td style=\"font-weight: bold;\">" + apk.get_sha1() + "</td>" + "\n"
        report += "\t\t</tr>" + "\n"
        report += "\t\t<tr>" + "\n"
        report += "\t\t\t<td>File SHA-256:</td>" + "\n"
        report += "\t\t\t<td style=\"font-weight: bold;\">" + apk.get_sha256() + "</td>" + "\n"
        report += "\t\t</tr>" + "\n"
        report += "\t\t<tr>" + "\n"
        report += "\t\t\t<td>File SHA-512:</td>" + "\n"
        report += "\t\t\t<td style=\"font-weight: bold;\">" + apk.get_sha512() + "</td>" + "\n"
        report += "\t\t</tr>" + "\n"

        # App Info:
        report += "\t\t<tr style='font-size: 120%; font-weight: bold;'>" + "\n"
        report += "\t\t\t<td colspan=\"2\" style=\"background: #2F2F2F; color: #FFFFFF; text-align: center;\">APP INFO</td>" + "\n"
        report += "\t\t</tr>" + "\n"
        if man is not None:
            # Package name:
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>Package:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + man.get_package_name() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
        # App name:
        report += "\t\t<tr>" + "\n"
        report += "\t\t\t<td>Name:</td>" + "\n"
        report += "\t\t\t<td style=\"font-weight: bold;\">" + apk.get_app_name() + "</td>" + "\n"
        report += "\t\t</tr>" + "\n"
        if man is not None:
            # App version:
            version = man.get_version()
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>Version:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + version["name"] + " (code: " + str(version["code"]) + ")" + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"

            # App SDK version:
            sdk = man.get_sdk_version()
            if "target" in sdk:
                target = sdk["target"]
            else:
                target = ""
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>Target SDK:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + target + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"

            # App permissions:
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td style=\"vertical-align: top;\">Permissions (" + str(man.get_number_of_permissions()) + "):</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">\n"
            for permission in man.get_permissions():
                if permission == "android.permission.SEND_SMS" or permission == "android.permission.RECEIVE_SMS" or permission == "android.permission.RECEIVE_MMS" or permission == "android.permission.CALL_PHONE" or permission == "android.permission.CALL_PRIVILEGED" or permission == "android.permission.PROCESS_OUTGOING_CALLS" or permission == "android.permission.INSTALL_PACKAGES" or permission == "android.permission.MOUNT_FORMAT_FILESYSTEMS" or permission == "android.permission.MOUNT_UNMOUNT_FILESYSTEMS":
                    report += "\t\t\t\t<span style=\"color: #FF0000;\">" + permission + "</span><br />\n"
                else:
                    report += "\t\t\t\t" + permission + "<br />\n"
            report += "\t\t\t</td>" + "\n"
            report += "\t\t</tr>" + "\n"

            # App Activities:
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td style=\"vertical-align: top;\">Activities (" + str(man.get_number_of_activities()) + "):</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">\n"
            for activity in man.get_activities():
                report += "\t\t\t\t" + activity["name"] + "<br />\n"
            report += "\t\t\t</td>" + "\n"
            report += "\t\t</tr>" + "\n"

            # App Services:
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td style=\"vertical-align: top;\">Services (" + str(man.get_number_of_services()) + "):</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">\n"
            for service in man.get_services():
                report += "\t\t\t\t" + service["name"] + "<br />\n"
            report += "\t\t\t</td>" + "\n"
            report += "\t\t</tr>" + "\n"

            # App BroadcastReceivers:
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td style=\"vertical-align: top;\">BroadcastReceivers (" + str(man.get_number_of_broadcast_receivers()) + "):</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">\n"
            for receiver in man.get_broadcast_receivers():
                report += "\t\t\t\t" + receiver["name"] + "<br />\n"
            report += "\t\t\t</td>" + "\n"
            report += "\t\t</tr>" + "\n"

        # Author Info:
        report += "\t\t<tr style='font-size: 120%; font-weight: bold;'>" + "\n"
        report += "\t\t\t<td colspan=\"2\" style=\"background: #2F2F2F; color: #FFFFFF; text-align: center;\">AUTHOR INFO</td>" + "\n"
        report += "\t\t</tr>" + "\n"
        if cert is not None:
            # Author name:
            author = cert.get_owner()
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>Name:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">\n"
            if "debug" in author["name"].lower() or "unknown" in author["name"].lower():
                report += "\t\t\t\t<span style=\"color: #FF0000;\">" + author["name"] + "</span><br />\n"
            else:
                report += "\t\t\t\t" + author["name"] + "<br />\n"
            report += "\t\t\t</td>" + "\n"
            report += "\t\t</tr>" + "\n"

            # Author email:
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>Email:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + author["email"] + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"

            # Author company unit:
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>Company Unit:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + author["unit"] + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"

            # Author organization:
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>Company:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">\n"
            if "debug" in author["organization"].lower() or "unknown" in author["organization"].lower():
                report += "\t\t\t\t<span style=\"color: #FF0000;\">" + author["organization"] + "</span><br />\n"
            else:
                report += "\t\t\t\t" + author["organization"] + "<br />\n"
            report += "\t\t\t</td>" + "\n"
            report += "\t\t</tr>" + "\n"

            # Author location:
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>Locality:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + author["city"] + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>State:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + author["state"] + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>Country:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + author["country"] + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>Domain Component:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + author["domain"] + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"

        # Certificate Info:
        report += "\t\t<tr style='font-size: 120%; font-weight: bold;'>" + "\n"
        report += "\t\t\t<td colspan=\"2\" style=\"background: #2F2F2F; color: #FFFFFF; text-align: center;\">CERTIFICATE INFO</td>" + "\n"
        report += "\t\t</tr>" + "\n"
        if cert is not None:
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>File:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + cert.get_file_name() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>File size:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + str(cert.get_size()) + " Bytes</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>File MD5:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + cert.get_md5() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>File SHA-1:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + cert.get_sha1() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>File SHA-256:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + cert.get_sha256() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>File SHA-512:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + cert.get_sha512() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            validity = cert.get_validity()
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>Validity:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">From: " + validity["from"] + " - Until: " + validity["until"] + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>Serial Number:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + cert.get_serial_number() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>Fingerprint MD5:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + cert.get_fingerprint_md5() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>Fingerprint SHA-1:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + cert.get_fingerprint_sha1() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>Fingerprint SHA-256:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + cert.get_fingerprint_sha256() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>Fingerprint Signature:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + cert.get_fingerprint_signature() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>Fingerprint Version:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + cert.get_fingerprint_version() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"

        # Manifest Info:
        report += "\t\t<tr style='font-size: 120%; font-weight: bold;'>" + "\n"
        report += "\t\t\t<td colspan=\"2\" style=\"background: #2F2F2F; color: #FFFFFF; text-align: center;\">ANDROIDMANIFEST.XML INFO</td>" + "\n"
        report += "\t\t</tr>" + "\n"
        if man is not None:
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>File:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + man.get_file_name() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>File size:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + str(man.get_size()) + " Bytes</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>File MD5:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + man.get_md5() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>File SHA-1:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + man.get_sha1() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>File SHA-256:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + man.get_sha256() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>File SHA-512:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + man.get_sha512() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"

        # Classes.dex info:
        report += "\t\t<tr style='font-size: 120%; font-weight: bold;'>" + "\n"
        report += "\t\t\t<td colspan=\"2\" style=\"background: #2F2F2F; color: #FFFFFF; text-align: center;\">CLASSES.DEX INFO</td>" + "\n"
        report += "\t\t</tr>" + "\n"
        if dex is not None:
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>File:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + dex.get_file_name() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>File size:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + str(dex.get_size()) + " Bytes</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>File MD5:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + dex.get_md5() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>File SHA-1:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + dex.get_sha1() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>File SHA-256:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + dex.get_sha256() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td>File SHA-512:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">" + dex.get_sha512() + "</td>" + "\n"
            report += "\t\t</tr>" + "\n"

            # URLs:
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td style=\"vertical-align: top;\">URLs:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">\n"
            for url in dex.get_urls():
                report += "\t\t\t\t" + url + "<br />\n"
            report += "\t\t\t</td>" + "\n"
            report += "\t\t</tr>" + "\n"

            # Shell commands:
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td style=\"vertical-align: top;\">Shell Commands:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">\n"
            for command in dex.get_shell_commands():
                report += "\t\t\t\t" + command + "<br />\n"
            report += "\t\t\t</td>" + "\n"
            report += "\t\t</tr>" + "\n"

            # Strings:
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td style=\"vertical-align: top;\">Strings:</td>" + "\n"
            report += "\t\t\t<td style=\"font-weight: bold;\">\n"
            for string in dex.get_strings():
                report += "\t\t\t\t" + str(string) + "<br />\n"
            report += "\t\t\t</td>" + "\n"
            report += "\t\t</tr>" + "\n"

        # List of files:
        report += "\t\t<tr style='font-size: 120%; font-weight: bold;'>" + "\n"
        report += "\t\t\t<td colspan=\"2\" style=\"background: #2F2F2F; color: #FFFFFF; text-align: center;\">OTHER FILES</td>" + "\n"
        report += "\t\t</tr>" + "\n"
        for entry in apk.get_file_list():
            report += "\t\t<tr>" + "\n"
            report += "\t\t\t<td style=\"vertical-align: top; font-weight: bold;\">" + entry.get_file_name() + "</td>" + "\n"
            report += "\t\t\t<td>\n"
            report += "\t\t\t\tFile size: " + str(entry.get_size()) + "<br />\n"
            report += "\t\t\t\tFile MD5: " + entry.get_md5() + "<br />\n"
            report += "\t\t\t\tFile SHA-1: " + entry.get_sha1() + "<br />\n"
            report += "\t\t\t\tFile SHA-256: " + entry.get_sha256() + "<br />\n"
            report += "\t\t\t\tFile SHA-512: " + entry.get_sha512() + "<br />\n"
            report += "\t\t\t</td>" + "\n"
            report += "\t\t</tr>" + "\n"

        # Footer:
        report += "\t</table>" + "\n"
        report += "</html>" + "\n"

        return report
