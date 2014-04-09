#################################################################################################
# @file App.py																					#
# @brief The App class representing an Android app.												#
# @update 2014-02-02 19:59:00 (Sun Feb 2, 2014 at 7:59 PM)										#
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




#-------------------------------- BEGIN Import Classes: -----------------------------------#
from Author import *
from Certificate import *
#-------------------------------- END Import Classes. -------------------------------------#




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
	__author = None  # the author of the app
	__certificate = None  # the digital certificate of the app

	__name = ""  # name of the app
	__package = ""  # package of the app
	__version = ""  # version of the app
	__sdk = ""  # target SDK of the app
	__services = None  # Services declared by the app
	__activities = None  # Activities declared by the app
	__receivers = None  # BroadcastReceivers declared by the app
	__permissions = None  # premissions requested by the app
	__size = ""  # The app size
	__md5 = ""  # MD5 hash of the app
	__sha256 = ""  # SHA-256 hash of the app
	__sha512 = ""  # SHA-512 hash of the app
	__dexStrings = None  # strings hard-coded in the classes.dex file
	__dexURLs = None  # URLs hard-coded in the classes.dex file
	__dexShellCommands = None  # commands hard-coded in the classes.dex file




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
		self.__author = None
		self.__certificate = None
		self.__name = ""
		self.__package = ""
		self.__version = ""
		self.__sdk = ""
		self.__services = []
		self.__activities = []
		self.__receivers = []
		self.__permissions = []
		self.__dexStrings = []
		self.__dexURLs = []
		self.__dexShellCommands = []

		#Calculate the MD5 and SHA-256 hashes of the APK package:
		try:
			self.__size = os.path.getsize(apkAbsoluteDir)  # os.stat(apkAbsoluteDir).st_size
			apkFileContent = open(apkAbsoluteDir, 'rb').read()
		except:
			pass
		else:
			self.__md5 = hashlib.md5(apkFileContent).hexdigest()
			self.__sha256 = hashlib.sha256(apkFileContent).hexdigest()
			self.__sha512 = hashlib.sha512(apkFileContent).hexdigest()

		#Extract the certificate (META-INF/CERT.RSA) from the APK package and save it (temporarily):
		with zipfile.ZipFile(apkAbsoluteDir) as z:
			with z.open(os.path.join(certDir, certFile)) as zf, open(os.path.join(apkDir, os.path.basename(certFile)), 'wb') as f:
				shutil.copyfileobj(zf, f)

		#Extract the author and certificate information from the digital certificate file (META-INF/CERT.RSA):
		self.__author = Author(certFile)
		self.__certificate = Certificate(certFile)

		#Remove the (temp) created file:
		os.remove(certFile)

		#Extract the AndroidManifest.xml file info:
		self.extractManifestInfo(apkFile)




	##
	# Get the author of the app.
	#
	# @return the author of the app.
	##
	def getAuthor(self):
		return self.__author




	##
	# Get the digital certificate of the app.
	#
	# @return the digital certificate of the app.
	##
	def getCertificate(self):
		return self.__certificate




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
	# Get the size of the APK package.
	#
	# @return the size of the APK package.
	##
	def getSize(self):
		return self.__size




	##
	# Get the MD5 hash of the APK package.
	#
	# @return the MD5 hash of the APK package.
	##
	def getAppMD5(self):
		return self.__md5




	##
	# Get the SHA-256 hash of the APK package.
	#
	# @return the SHA-256 hash of the APK package.
	##
	def getAppSHA256(self):
		return self.__sha256




	##
	# Get the SHA-512 hash of the APK package.
	#
	# @return the SHA-512 hash of the APK package.
	##
	def getAppSHA512(self):
		return self.__sha512




	##
	# Get the classes.dex encoded URLs.
	#
	# @return the URLs hard-coded into the classes.dex file.
	##
	def getDexURLs(self):
		return self.__dexURLs




	##
	# Get the classes.dex encoded shell commands.
	#
	# @return the shell commands hard-coded into the classes.dex file.
	##
	def getDexShellCommands(self):
		return self.__dexShellCommands




	##
	# Get the classes.dex encoded strings.
	#
	# @return the strings hard-coded into the classes.dex file.
	##
	def getDexStrings(self):
		return self.__dexStrings




	##
	# Set the classes.dex encoded strings and URLs.
	#
	# @param strings  the strings and URLs hard-coded into the classes.dex file.
	##
	def setDexStrings(self, strings):
		for string in strings:
			if string != "":
				if "www" in string.lower() or "http://" in string.lower() or ".com" in string.lower() or ".net" in string.lower() or ".org" in string.lower() or ".eu" in string.lower() or ".co.uk" in string.lower() or ".es" in string.lower() or ".it" in string.lower() or ".de" in string.lower() or ".fr" in string.lower() or ".us" in string.lower() or ".ru" in string.lower() or ".biz" in string.lower() or ".info" in string.lower():
					self.__dexURLs.append(string)
				elif "su " in string.lower() or "su_" in string.lower() or "chmod" in string.lower() or "chown" in string.lower() or "mount" in string.lower() or "dexopt" in string.lower() or "dhcpcd" in string.lower() or "dmesg" in string.lower() or "dnsmasq" in string.lower() or "dumpstate" in string.lower() or "dumpsys" in string.lower() or "fsck" in string.lower() or "iptables" in string.lower() or "keystore" in string.lower() or "lsmod" in string.lower() or "kill" in string.lower() or "rmdir" in string.lower() or "exit" in string.lower() or "logcat" in string.lower() or string.lower() == "pm" or string.lower() == "am" or "apk" in string.lower():
					self.__dexShellCommands.append(string)
				else:
					self.__dexStrings.append(string)

		#Sort the lists:
		self.__dexURLs.sort()
		self.__dexStrings.sort()




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


		#Sort the lists of Activities, Services and BroadcastReceivers:
		self.__activities.sort()
		self.__services.sort()
		self.__receivers.sort()

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

		#Sort the list of permissions:
		self.__permissions.sort()

		#Debug:
		#print "App Permission: " + str(self.__permissions)
		#print "App Number of Permissions: " + str(len(self.__permissions))
