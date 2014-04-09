#####################################################################################################
# @file Report.py																					#
# @brief Generate a report of a specific app.														#
# @update 2014-02-09 19:59:00 (Sun Feb 9, 2014 at 7:59 PM)											#
# @author Paolo Rovelli																				#
#####################################################################################################




#-------------------------------- BEGIN Import Python types: ------------------------------#
import getopt
import os
import logging
from zipfile import ZipFile
#-------------------------------- END Import Python types. --------------------------------#




#-------------------------------- BEGIN Logging Configuration: ----------------------------#
#Retrieve logger:
logger = logging.getLogger("NinjaDroid")
#-------------------------------- END Logging Configuration. ------------------------------#




##
# Report class.
# 
# @author Paolo Rovelli
##
class Report():
	#-------- Class attributes: --------#
	__inputDir = ""  # the APK original file directory
	__inputFile = ""  # the APK original file name
	__outputFile = ""  # the report file path
	__app = ""  # the app
	__appAuthor = ""  # the app developer
	__appCertificate = ""  # the app certificate




	#-------- Class methods: --------#
	##
	# Class constructor.
	# 
	# @param apkDir  the original APK file directory.
	# @param apkFile  the original APK file name.
	# @param filePath  the report file complete path.
	# @param app  the App instantiation.
	##
	def __init__(self, apkDir, apkFile, filePath, app):
		#Attributes initialization:
		self.__inputDir = apkDir
		self.__inputFile = apkFile
		self.__outputFile = filePath
		self.__app = app
		self.__appAuthor = app.getAuthor()
		self.__appCertificate = app.getCertificate()

		#Debug:
		#logger.info("App Package: " + self.__app.getPackage())
		#logger.info("App Name: " + self.__app.getName())
		#logger.info("App Version: " + self.__app.getVersion())
		#logger.info("APK Size: " + str(self.__app.getSize()) + " Bytes")
		#logger.info("APK package MD5: " + self.__app.getAppMD5())
		#logger.info("APK package SHA-256: " + self.__app.getAppSHA256())
		#logger.info("APK package SHA-512: " + self.__app.getAppSHA512())
		#logger.info("Target SDK: " + self.__app.getTargetSdk())
		#logger.info("Activities (" + str(len(self.__app.getActivities())) + "): " + str(self.__app.getActivities()))
		#logger.info("Services (" + str(len(self.__app.getServices())) + "): " + str(self.__app.getServices()))
		#logger.info("BroadcastReceivers (" + str(len(self.__app.getBroadcastReceivers())) + "): " + str(self.__app.getBroadcastReceivers()))
		#logger.info("Permissions (" + str(self.__app.getNumberOfPermissions()) + "): " + str(self.__app.getPermissions()))
		#logger.info("Author Name: " + self.__appAuthor.getName())
		#logger.info("Author Email: " + self.__appAuthor.getEmail())
		#logger.info("Author Company Unit: " + self.__appAuthor.getCompanyUnit())
		#logger.info("Author Company: " + self.__appAuthor.getCompany())
		#logger.info("Author Locality: " + self.__appAuthor.getLocality())
		#logger.info("Author State: " + self.__appAuthor.getState())
		#logger.info("Author Country: " + self.__appAuthor.getCountry())
		#logger.info("Author Domain Component: " + self.__appAuthor.getDomainComponent())
		#logger.info("Certificate Validity: " + self.__appCertificate.getValidity())
		#logger.info("Certificate Serial Number: " + self.__appCertificate.getSerialNumber())
		#logger.info("Certificate MD5: " + self.__appCertificate.getMD5())
		#logger.info("Certificate SHA-1: " + self.__appCertificate.getSHA1())
		#logger.info("Certificate SHA-256: " + self.__appCertificate.getSHA256())
		#logger.info("Certificate Signature: " + self.__appCertificate.getSignature())

		#Extract the information of the static analysis:
		report = self.generateHTMLReport()

		#Save the static analysis report in an HTML file:
		self.createFile(report)




	##
	# Generate the static analysis report in an HTML file format.
	##
	def generateHTMLReport(self):
		#Header:
		report = "<html>" + "\n"
		report += "\t<table border=\"0\" cellspacing=\"0\" cellpadding=\"5\">" + "\n"

		#Summary:
		report += "\t\t<tr style='font-size: 120%; font-weight: bold;'>" + "\n"
		report += "\t\t\t<td colspan=\"2\" style=\"background: #2F2F2F; color: #FFFFFF; text-align: center;\">SUMMARY</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>File:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">" + self.__inputFile + "</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>Size:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">" + str(self.__app.getSize()) + " Bytes</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>MD5:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">" + self.__app.getAppMD5() + "</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>SHA-256:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">" + self.__app.getAppSHA256() + "</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>SHA-512:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">" + self.__app.getAppSHA512() + "</td>" + "\n"
		report += "\t\t</tr>" + "\n"

		#App Info:
		report += "\t\t<tr style='font-size: 120%; font-weight: bold;'>" + "\n"
		report += "\t\t\t<td colspan=\"2\" style=\"background: #2F2F2F; color: #FFFFFF; text-align: center;\">APP INFO</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>Package:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">" + self.__app.getPackage() + "</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>Name:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">" + self.__app.getName() + "</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>Version:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">" + self.__app.getVersion() + "</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>Target SDK:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">" + self.__app.getTargetSdk() + "</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td style=\"vertical-align: top;\">Permissions (" + str(self.__app.getNumberOfPermissions()) + "):</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">\n"
		for permission in self.__app.getPermissions():
			if permission == "android.permission.SEND_SMS" or permission == "android.permission.RECEIVE_SMS" or permission == "android.permission.RECEIVE_MMS" or permission == "android.permission.CALL_PHONE" or permission == "android.permission.CALL_PRIVILEGED" or permission == "android.permission.PROCESS_OUTGOING_CALLS" or permission == "android.permission.INSTALL_PACKAGES" or permission == "android.permission.MOUNT_FORMAT_FILESYSTEMS" or permission == "android.permission.MOUNT_UNMOUNT_FILESYSTEMS":
				report += "\t\t\t\t<span style=\"color: #FF0000;\">" + permission + "</span><br />\n"
			else:
				report += "\t\t\t\t" + permission + "<br />\n"
		report += "\t\t\t</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		appActivities = self.__app.getActivities()
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td style=\"vertical-align: top;\">Activities (" + str(len(appActivities)) + "):</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">\n"
		for activity in appActivities:
			report += "\t\t\t\t" + activity + "<br />\n"
		report += "\t\t\t</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		appServices = self.__app.getServices()
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td style=\"vertical-align: top;\">Services (" + str(len(appServices)) + "):</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">\n"
		for service in appServices:
			report += "\t\t\t\t" + service + "<br />\n"
		report += "\t\t\t</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		appBroadcastReceivers = self.__app.getBroadcastReceivers()
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td style=\"vertical-align: top;\">BroadcastReceivers (" + str(len(appBroadcastReceivers)) + "):</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">\n"
		for receiver in appBroadcastReceivers:
			report += "\t\t\t\t" + receiver + "<br />\n"
		report += "\t\t\t</td>" + "\n"
		report += "\t\t</tr>" + "\n"

		#Author Info:
		report += "\t\t<tr style='font-size: 120%; font-weight: bold;'>" + "\n"
		report += "\t\t\t<td colspan=\"2\" style=\"background: #2F2F2F; color: #FFFFFF; text-align: center;\">AUTHOR INFO</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		appAuthorName = self.__appAuthor.getName()
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>Name:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">\n"
		if "debug" in appAuthorName.lower() or "unknown" in appAuthorName.lower():
			report += "\t\t\t\t<span style=\"color: #FF0000;\">" + appAuthorName + "</span><br />\n"
		else:
			report += "\t\t\t\t" + appAuthorName + "<br />\n"
		report += "\t\t\t</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>Email:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">" + self.__appAuthor.getEmail() + "</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>Company Unit:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">" + self.__appAuthor.getCompanyUnit() + "</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		appAuthorCompany = self.__appAuthor.getCompany()
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>Company:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">\n"
		if "debug" in appAuthorCompany.lower() or "unknown" in appAuthorCompany.lower():
			report += "\t\t\t\t<span style=\"color: #FF0000;\">" + appAuthorCompany + "</span><br />\n"
		else:
			report += "\t\t\t\t" + appAuthorCompany + "<br />\n"
		report += "\t\t\t</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>Locality:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">" + self.__appAuthor.getLocality() + "</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>State:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">" + self.__appAuthor.getState() + "</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>Country:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">" + self.__appAuthor.getCountry() + "</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>Domain Component:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">" + self.__appAuthor.getDomainComponent() + "</td>" + "\n"
		report += "\t\t</tr>" + "\n"

		#Certificate Info:
		report += "\t\t<tr style='font-size: 120%; font-weight: bold;'>" + "\n"
		report += "\t\t\t<td colspan=\"2\" style=\"background: #2F2F2F; color: #FFFFFF; text-align: center;\">CERTIFICATE INFO</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>Validity:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">" + self.__appCertificate.getValidity() + "</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>Serial Number:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">" + self.__appCertificate.getSerialNumber() + "</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>MD5:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">" + self.__appCertificate.getMD5() + "</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>SHA-1:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">" + self.__appCertificate.getSHA1() + "</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>SHA-256:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">" + self.__appCertificate.getSHA256() + "</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td>Signature:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">" + self.__appCertificate.getSignature() + "</td>" + "\n"
		report += "\t\t</tr>" + "\n"

		#Classes.dex strings:
		report += "\t\t<tr style='font-size: 120%; font-weight: bold;'>" + "\n"
		report += "\t\t\t<td colspan=\"2\" style=\"background: #2F2F2F; color: #FFFFFF; text-align: center;\">classes.dex</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td style=\"vertical-align: top;\">URLs:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">\n"
		for string in self.__app.getDexURLs():
			if "xxx" in string.lower() or "porn" in string.lower():
				report += "\t\t\t\t<span style=\"color: #FF0000;\">" + str(string) + "</span><br />\n"
			else:
				report += "\t\t\t\t" + str(string) + "<br />\n"
		report += "\t\t\t</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td style=\"vertical-align: top;\">Shell Commands:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">\n"
		for string in self.__app.getDexShellCommands():
			if "su" in string.lower() or "chmod" in string.lower() or "mount" in string.lower() or "kill" in string.lower() or "rmdir" in string.lower():
				report += "\t\t\t\t<span style=\"color: #FF0000;\">" + str(string) + "</span><br />\n"
			else:
				report += "\t\t\t\t" + str(string) + "<br />\n"
		report += "\t\t\t</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td style=\"vertical-align: top;\">Strings:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">\n"
		for string in self.__app.getDexStrings():
			if "xxx" in string.lower() or "porn" in string.lower() or "bin" in string.lower() or "install" in string.lower() or "/system" in string.lower() or "/data" in string.lower() or "root" in string.lower() or "shell" in string.lower() or "exploit" in string.lower() or "hack" in string.lower():
				report += "\t\t\t\t<span style=\"color: #FF0000;\">" + str(string) + "</span><br />\n"
			else:
				report += "\t\t\t\t" + str(string) + "<br />\n"
		report += "\t\t\t</td>" + "\n"
		report += "\t\t</tr>" + "\n"

		#List of Files:
		report += "\t\t<tr style='font-size: 120%; font-weight: bold;'>" + "\n"
		report += "\t\t\t<td colspan=\"2\" style=\"background: #2F2F2F; color: #FFFFFF; text-align: center;\">LIST OF FILES</td>" + "\n"
		report += "\t\t</tr>" + "\n"
		#Print all the entries of the APK package:
		apkAbsPath = os.path.join(self.__inputDir, self.__inputFile)  # the APK package absolute path (from the root)
		zipFile = ZipFile(apkAbsPath)
		report += "\t\t<tr>" + "\n"
		report += "\t\t\t<td style=\"vertical-align: top;\">APK Entries:</td>" + "\n"
		report += "\t\t\t<td style=\"font-weight: bold;\">\n"
		for fileName in zipFile.namelist():
			if "raw/su" in fileName.lower() or "superuser" in fileName.lower() or "exploit" in fileName.lower() or "exploid" in fileName.lower() or "hack" in fileName.lower() or ".so" in fileName.lower() or ".c" in fileName.lower() or ".apk" in fileName.lower():
				report += "\t\t\t\t<span style=\"color: #FF0000;\">" + fileName + "</span><br />\n"
			else:
				report += "\t\t\t\t" + fileName + "<br />\n"
		report += "\t\t\t</td>" + "\n"
		report += "\t\t</tr>" + "\n"

		#Footer:
		report += "\t</table>" + "\n"
		report += "</html>" + "\n"

		return report




	##
	# Create the report file and write the report.
	# 
	# @param report  the report (HTML) string.
	##
	def createFile(self, report):
		#Open file and append the instance:
		fp = open(self.__outputFile, "w")  # b: write only (overwrites the file or creates a new one)

		#Write to the file:
		fp.write(report)

		#Close file:
		fp.close()
	