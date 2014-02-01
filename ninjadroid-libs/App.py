#################################################################################################
# @file App.py																					#
# @brief The App class representing an Android app.												#
# @update 2014-02-01 19:59:00 (Sun Feb 2, 2014 at 7:59 PM)										#
# @author Paolo Rovelli																			#
#################################################################################################




#-------------------------------- BEGIN Import Python types: ------------------------------#
import os
import subprocess
import sys
import fnmatch
import zipfile
import shutil
import hashlib
#-------------------------------- END Import Python types. --------------------------------#




#----------------------------------- BEGIN Configuration: ---------------------------------#
#Certificate file:
certDir = "META-INF/"
certFile = "CERT.RSA"
manifestFile = "AndroidManifest.xml"
#----------------------------------- END Configuration. -----------------------------------#




#----------------------------------- BEGIN Generic functions: ---------------------------------#
##
# Find a substring in a string, starting after a specified prefix and ended before a specified suffix.
# 
# @param s  the string.
# @param prefix  the prefix of the file name to be deleted.
# @param suffix  the suffix of the file name to be deleted.
# @return the substring starting after prefix and ended before suffix.
##
def findBetween(s, prefix, suffix):
	try:
		start = s.index(prefix) + len(prefix)
		end = s.index(suffix, start)
		return s[start:end]
	except ValueError:
		return ""


##
# Find all the substring starting position in a string.
# 
# @param haystack  the string.
# @param needle  the substring to be found.
# @return the substring starting after prefix and ended before suffix.
##
def findAll(haystack, needle):
	offs = -1
	while True:
		offs = haystack.find(needle, offs+1)
		if offs == -1:
			break
		else:
			yield offs
#------------------------------------ END Generic functions. ----------------------------------#




##
# App class.
# 
# @author Paolo Rovelli
##
class App():
	#-------- Class attributes: --------#
	__authorName = ""  # name of the developer
	__authorEmail = ""  # email address of the developer
	__authorCompany = ""  # company name of the developer
	__authorCountry = ""  # country of the developer

	__certificateMD5 = ""  # the MD5 fingerprint of the certificate of the App

	__name = ""  # name of the App
	__package = ""  # package of the App
	__version = ""  # version of the App
	__sdk = ""  # target SDK of the App
	__services = None  # Services declared by the App
	__activities = None  # Activities declared by the App
	__receivers = None  # BroadcastReceivers declared by the App
	__permissions = None  # premissions requested by the App
	__md5 = ""  # MD5 hash of the App
	__sha256 = ""  # SHA-256 hash of the App




	#-------- Class methods: --------#
	##
	# Class constructor.
	# 
	# @param apkDir  the complete path where APK package to be analyzed is stored.
	# @param apkFile  the name of the APK package to be analyzed.
	##
	def __init__(self, apkDir, apkFile):
		apkAbsoluteDir = os.path.join(apkDir, apkFile)

		#Attributes initialization:
		self.__authorName = ""
		self.__authorEmail = ""
		self.__authorCompany = ""
		self.__authorCountry = ""
		self.__certificateMD5 = ""
		self.__name = ""
		self.__package = ""
		self.__version = ""
		self.__sdk = ""
		self.__services = []
		self.__activities = []
		self.__receivers = []
		self.__permissions = []

		#Calculate the MD5 and SHA-256 hashes of the APK package:
		try:
			apkFileContent = open(apkAbsoluteDir, 'rb').read()
		except:
			pass
		else:
			self.__md5 = hashlib.md5(apkFileContent).hexdigest()
			self.__sha256 = hashlib.sha256(apkFileContent).hexdigest()

		#Extract the certificate (META-INF/CERT.RSA) from the APK package and save it (temporarily):
		with zipfile.ZipFile(apkAbsoluteDir) as z:
			with z.open(certDir+certFile) as zf, open(os.path.join(apkDir, os.path.basename(certFile)), 'wb') as f:
				shutil.copyfileobj(zf, f)

		#Extract the author information from the certificate file (META-INF/CERT.RSA):
		self.extractAuthorInfo(certFile)

		#Remove the (temp) created file:
		os.remove(certFile)

		#Extract the AndroidManifest.xml file info:
		self.extractManifestInfo(apkFile)




	##
	# Get the author name of the app.
	#
	# @return the author name of the app.
	##
	def getAuthorName(self):
		return self.__authorName




	##
	# Get the author's email address, if any.
	#
	# @return the author's email address.
	##
	def getAuthorEmail(self):
		return self.__authorEmail




	##
	# Get the author's company name.
	#
	# @return the author's company name.
	##
	def getAuthorCompany(self):
		return self.__authorCompany




	##
	# Get the author's country.
	#
	# @return the author's country.
	##
	def getAuthorCountry(self):
		return self.__authorCountry




	##
	# Get the author's certificate MD5 fingerprint.
	#
	# @return the author's certificate MD5 fingerprint.
	##
	def getCertificateMD5(self):
		return self.__certificateMD5




	##
	# Get the permissions requested by the app in its AndroidManifest.xml file.
	#
	# @return the permissions requested by the app.
	##
	def getPermissions(self):
		return self.__permissions




	##
	# Get the number of permissions requested by the app in its AndroidManifest.xml file.
	#
	# @return the number of permissions requested by the app.
	##
	def getNumberOfPermissions(self):
		return len(self.__permissions)




	##
	# Get the app package name.
	#
	# @return the app package name.
	##
	def getPackage(self):
		return self.__package




	##
	# Get the app name.
	#
	# @return the app name.
	##
	def getName(self):
		return self.__name




	##
	# Get the app version.
	#
	# @return the app version.
	##
	def getVersion(self):
		return self.__version




	##
	# Get the app Activities.
	#
	# @return the app Activities.
	##
	def getActivities(self):
		return self.__activities




	##
	# Get the app Services.
	#
	# @return the app Services.
	##
	def getServices(self):
		return self.__services




	##
	# Get the app BroadcastReceivers.
	#
	# @return the app BroadcastReceivers.
	##
	def getBroadcastReceivers(self):
		return self.__receivers




	##
	# Get the app version.
	#
	# @return the app version.
	##
	def getTargetSdk(self):
		return self.__sdk




	##
	# Get the MD5 hash of the APK package.
	#
	# @return the MD5 hash of the APK package.
	##
	def getApkMD5(self):
		return self.__md5




	##
	# Get the SHA-256 hash of the APK package.
	#
	# @return the SHA-256 hash of the APK package.
	##
	def getApkSHA256(self):
		return self.__sha256




	##
	# Extract the author information from the certificate file (META-INF/CERT.RSA).
	# 
	# @param certFile  the certificate file (META-INF/CERT.RSA)
	##
	def extractAuthorInfo(self, certFile):
		#Extract the author info from the certificate file (META-INF/CERT.RSA):
		shellcommand = "keytool -printcert -file " + certFile
		process = subprocess.Popen(shellcommand, stdout=subprocess.PIPE, stderr=None, shell=True)
		apkCertificate = process.communicate()[0].splitlines()  # apkPermissions.split('\n')

		#Debug:
		#print apkCertificate

		##
		# Example of DroidRoot.A:
		# -----------------------
		# Owner: CN=Android Debug, O=Android, C=US
		# Issuer: CN=Android Debug, O=Android, C=US
		# Serial number: 4ba340d1
		# Valid from: Fri Mar 19 10:16:01 CET 2010 until: Sat Mar 19 10:16:01 CET 2011
		# Certificate fingerprints:
		#	 MD5:  B1:C9:88:EB:7B:72:D2:04:3A:9D:1F:E4:74:0D:6F:78
		#	 SHA1: CD:82:17:48:51:61:85:75:EB:6E:08:E9:4F:DF:05:11:DD:38:63:CC
		#	 SHA256: A3:22:0F:2D:48:63:44:E3:F4:D9:4D:44:58:8A:CD:9A:F7:82:44:78:ED:32:77:7C:E2:3F:FF:55:97:32:33:CC
		#	 Signature algorithm name: SHA1withRSA
		#	 Version: 3
		##

		##################################
		# CERTIFICATE OWNER FIELDS :	 #
		# ------------------------------ #
		# CN: Common Name				#
		# E: Email address			   #
		# OU: Organization Unit		  #
		# O: Organization name		   #
		# L: Locality name			   #
		# ST: State or province Name	 #
		# C: Country					 #
		# DC: Domain Component		   #
		##################################

		for info in apkCertificate:
			#Debug
			#print "info: " + info

			#Owner info:
			pathPrefix = "Owner: "
			if info[0:len(pathPrefix)] == pathPrefix:
				authorInfo = info[len(pathPrefix):].split(", ")

				for field in authorInfo:
					pathPrefix = "CN="
					if field[0:len(pathPrefix)] == pathPrefix:
						self.__authorName = field[len(pathPrefix):]
						continue

					pathPrefix = "O="
					if field[0:len(pathPrefix)] == pathPrefix:
						self.__authorCompany = field[len(pathPrefix):]
						continue

					pathPrefix = "EMAILADDRESS="
					if field[0:len(pathPrefix)] == pathPrefix:
						self.__authorEmail = field[len(pathPrefix):]
						continue

					pathPrefix = "C="
					if field[0:len(pathPrefix)] == pathPrefix:
						self.__authorCountry = field[len(pathPrefix):]
						continue

				continue

			#Certificate fingerprints (MD5):
			pathPrefix = "\t MD5:"
			if info[0:len(pathPrefix)] == pathPrefix:
				self.__certificateMD5 = info[len(pathPrefix):]
				continue
				

		#Debug:
		#print "Author Name: " + self.__authorName
		#print "Author Email: " + self.__authorEmail
		#print "Author Company: " + self.__authorCompany
		#print "Author Country: " + self.__authorCountry
		#print "Certificate MD5: " + self.__certificateMD5




	##
	# Extract the permissions from the AndroidManifest.xml file.
	##
	def extractManifestInfo(self, apkFile):
		self.extractAppNameFromAPK(apkFile)
		self.extractAppDetailsFromAPK(apkFile)
		self.extractAppPermissionsFromManifest(apkFile)




	##
	# Extract the app name, version, package and targetted SDK from the AndroidManifest.xml file of a given APK package.
	# 
	# @param apkFile  the APK package to be analyzed.
	##
	def extractAppNameFromAPK(self, apkFile):
		#Extract the APK package info:
		shellcommand = "aapt dump badging " + apkFile  # ["aapt", "dump", "badging", apk]
		process = subprocess.Popen(shellcommand, stdout=subprocess.PIPE, stderr=None, shell=True)
		apkInfo = process.communicate()[0].splitlines()

		##
		# Example: aapt dump badging DroidRoot.A.apk
		# -----------------------------------------
		# package: name='com.corner23.android.universalandroot' versionCode='11' versionName='1.6.1'
		# application-label:'Universal Androot'
		# application-icon-160:'res/drawable/icon.png'
		# application: label='Universal Androot' icon='res/drawable/icon.png'
		# launchable-activity: name='com.corner23.android.universalandroot.UniversalAndroot' label='Universal Androot' icon=''
		# uses-permission:'android.permission.CHANGE_WIFI_STATE'
		# uses-permission:'android.permission.ACCESS_WIFI_STATE'
		# uses-permission:'android.permission.WAKE_LOCK'
		# uses-permission:'android.permission.WRITE_EXTERNAL_STORAGE'
		# uses-implied-permission:'android.permission.WRITE_EXTERNAL_STORAGE','targetSdkVersion < 4'
		# uses-permission:'android.permission.READ_PHONE_STATE'
		# uses-implied-permission:'android.permission.READ_PHONE_STATE','targetSdkVersion < 4'
		# uses-permission:'android.permission.READ_EXTERNAL_STORAGE'
		# uses-implied-permission:'android.permission.READ_EXTERNAL_STORAGE','requested WRITE_EXTERNAL_STORAGE'
		# uses-feature:'android.hardware.wifi'
		# uses-implied-feature:'android.hardware.wifi','requested android.permission.ACCESS_WIFI_STATE, android.permission.CHANGE_WIFI_STATE, or android.permission.CHANGE_WIFI_MULTICAST_STATE permission'
		# uses-feature:'android.hardware.touchscreen'
		# uses-implied-feature:'android.hardware.touchscreen','assumed you require a touch screen unless explicitly made optional'
		# uses-feature:'android.hardware.screen.portrait'
		# uses-implied-feature:'android.hardware.screen.portrait','one or more activities have specified a portrait orientation'
		# main
		# supports-screens: 'normal'
		# supports-any-density: 'false'
		# locales: '--_--'
		# densities: '160'
		##
		
		for info in apkInfo:
			#Debug
			#print "info: " + info

			#Package info:
			pathPrefix = "package:"
			if info[0:len(pathPrefix)] == pathPrefix:
				self.__package = findBetween(info, "name='", "'")
				self.__version = findBetween(info, "versionName='", "'")
				continue

			#Target SDK version:
			pathPrefix = "targetSdkVersion:"
			if info[0:len(pathPrefix)] == pathPrefix:
				self.__sdk = findBetween(info, "targetSdkVersion:'", "'")
				continue

			#App name:
			pathPrefix = "application:"
			if info[0:len(pathPrefix)] == pathPrefix:
				self.__name = findBetween(info, "label='", "'")
				continue

			#Main Activity:
			#pathPrefix = "launchable-activity:"
			#if info[0:len(pathPrefix)] == pathPrefix:
			#	self.__activities.append( findBetween(info, "name='", "'") )
			#	continue

		#Debug:
		#print "App Package: " + self.__package
		#print "App Name: " + self.__name
		#print "App Version: " + self.__version
		#print "Target SDK: " + self.__sdk
		#print "Main Activity: " + self.__activities[0]




	##
	# Extract some app details (e.g. Activities, Services, BroadcastReceivers, etc...) from the AndroidManifest.xml file of a given APK package.
	# 
	# @param apkFile  the APK package to be analyzed.
	##
	def extractAppDetailsFromAPK(self, apkFile):
		#Extract the AndroidManifest XML tree:
		shellcommand = "aapt dump xmltree " + apkFile + " AndroidManifest.xml"  # ["aapt", "dump", "xmltree", apk, "AndroidManifest.xml"]
		process = subprocess.Popen(shellcommand, stdout=subprocess.PIPE, stderr=None, shell=True)
		xmlTree = process.communicate()[0]

		##
		# Example: aapt dump xmltree DroidRoot.A.apk AndroidManifest.xml
		# -----------------------------------------
		# N: android=http://schemas.android.com/apk/res/android
		# E: manifest (line=2)
		#   A: android:versionCode(0x0101021b)=(type 0x10)0xb
		#   A: android:versionName(0x0101021c)="1.6.1" (Raw: "1.6.1")
		#   A: package="com.corner23.android.universalandroot" (Raw: "com.corner23.android.universalandroot")
		#   E: application (line=6)
		#	 A: android:label(0x01010001)=@0x7f050000
		#	 A: android:icon(0x01010002)=@0x7f020000
		#	 E: activity (line=7)
		#	   A: android:label(0x01010001)=@0x7f050000
		#	   A: android:name(0x01010003)=".UniversalAndroot" (Raw: ".UniversalAndroot")
		#	   A: android:screenOrientation(0x0101001e)=(type 0x10)0x1
		#	   E: intent-filter (line=10)
		#		 E: action (line=11)
		#		   A: android:name(0x01010003)="android.intent.action.MAIN" (Raw: "android.intent.action.MAIN")
		#		 E: category (line=12)
		#		   A: android:name(0x01010003)="android.intent.category.LAUNCHER" (Raw: "android.intent.category.LAUNCHER")
		#   E: uses-permission (line=16)
		#	 A: android:name(0x01010003)="android.permission.CHANGE_WIFI_STATE" (Raw: "android.permission.CHANGE_WIFI_STATE")
		#   E: uses-permission (line=17)
		#	 A: android:name(0x01010003)="android.permission.ACCESS_WIFI_STATE" (Raw: "android.permission.ACCESS_WIFI_STATE")
		#   E: uses-permission (line=18)
		#	 A: android:name(0x01010003)="android.permission.WAKE_LOCK" (Raw: "android.permission.WAKE_LOCK")
		##
		
		#Take only from the <application> TAG:
		xmlTree = xmlTree[xmlTree.index("application"):-1]

		#print "Number of Activities: " + str(xmlTree.count("activity"))
		#print "Number of Services: " + str(xmlTree.count("service"))
		#print "Number of BroadcastReceivers: " + str(xmlTree.count("receiver"))

		for offs in findAll(xmlTree, "activity"):
			activity = xmlTree[offs:-1]
			idx = findBetween(activity, "android:name(", ")=\"")
			self.__activities.append( findBetween(activity, "android:name(" + idx + ")=\"", "\"") )

		for offs in findAll(xmlTree, "service"):
			service = xmlTree[offs:-1]
			idx = findBetween(service, "android:name(", ")=\"")
			self.__services.append( findBetween(service, "android:name(" + idx + ")=\"", "\"") )

		for offs in findAll(xmlTree, "receiver"):
			receiver = xmlTree[offs:-1]
			idx = findBetween(receiver, "android:name(", ")=\"")
			self.__receivers.append( findBetween(receiver, "android:name(" + idx + ")=\"", "\"") )

		#Debug:
		#print "Activities: " + str(self.__activities)
		#print "Services: " + str(self.__services)
		#print "BroadcastReceivers: " + str(self.__receivers)




	##
	# Extract the permissions from the AndroidManifest.xml file.
	##
	def extractAppPermissionsFromManifest(self, apkFile):
		#Extract the AndroidManifest.xml permissions:
		shellcommand = "aapt dump permissions ./" + apkFile + " | sed 1d | awk '{ print $NF }'"  # ["aapt", "dump", "permissions", apk]
		process = subprocess.Popen(shellcommand, stdout=subprocess.PIPE, stderr=None, shell=True)
		self.__permissions = process.communicate()[0].splitlines()

		#Debug:
		#print "APK Permission: " + str(self.__permissions)
		#print "APK Number of Permissions: " + str(len(self.__permissions))
