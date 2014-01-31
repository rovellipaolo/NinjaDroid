#############################################################################################
# @file ninjadroid.py																		#
# @brief Ninja Reverse Engineering on Android APK packages. 								#
# @license GPLv3 License. 									 								#
# @update 2014-01-31 23:10:00 (Fri Jan 31, 2013 at 11:10 PM)								#
# @author Paolo Rovelli																		#
#############################################################################################




#Example Call:
# $ python ninjadroid.py -t DroidRoot.A.apk
# $ python ninjadroid.py -t /Users/paolo/Development/NinjaDroid/DroidRoot.A.apk




#-------------------------------- BEGIN Import Python types: ------------------------------#
import getopt
import os
import subprocess
import sys
from zipfile import ZipFile
import shutil
import logging
#-------------------------------- END Import Python types. --------------------------------#




#----------------------------------- BEGIN Configuration: ---------------------------------#
#Certificate file:
certDir = "META-INF/"
certFile = "CERT.RSA"

#Manifest file:
manifestFile = "AndroidManifest.xml"

#Android Dalvik EXecutable file:
dexFile = "classes.dex"

#Output HTML file:
outputFileExtension = ".html"
#outputFileName = outputFilePrefix + outputFileExtension  # "[APKNAME].html"
#----------------------------------- END Configuration. -----------------------------------#




#-------------------------------- BEGIN Logging Configuration: ----------------------------#
#Create logger:
logger = logging.getLogger("NinjaDroid")
logger.setLevel(logging.DEBUG)

#Create a console handler for the logger:
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)  # log only until warning messages (no debug)
ch.setFormatter( logging.Formatter("  > %(name)s: %(message)s") )  # log message format
logger.addHandler(ch)  # add the handler to the logger
#-------------------------------- END Logging Configuration. ------------------------------#




#------------------------------- BEGIN Retrieving parameters: -----------------------------#
#Current path:
curpath = os.path.dirname( os.path.realpath(__file__) )  # the current directory


#Retrieve the target APK package:
target = ""
try:
	opts, extraparams = getopt.getopt(sys.argv[1:], "t:") 
except:
	pass
else:
	for o,p in opts:
		if o in ['-t', '--target']:
			target = p


#Check whether the target APK package has been inserted or not:
if target == "":
	#Debug:
	logger.error("No target APK package selected!")

	#Terminate the script:
	sys.exit()


#Check whether the target file is an APK package (it has a ".apk" extension):
targetNameLen = len(target)  # the length of the name of the APK package
if targetNameLen < 5:
	#Debug:
	logger.error("The target APK package must have a \".apk\" extension!")

	#Terminate the script:
	sys.exit()

targetExtension = str( target[targetNameLen-4:targetNameLen] )  # the file extension (simply the last 4 characters)
if targetExtension.lower() != ".apk":
	#Debug:
	logger.error("The target APK package must have a \".apk\" extension!")

	#Terminate the script:
	sys.exit()


#Retrieve the target APK package file and directory:
apkDir = ""  # the APK package directory
apkFile = ""  # the APK package file

try:
	lastIndexOfASlash = target.rindex("/") + 1
except ValueError:  # the "/" has not been found in the target APK package name...
	apkDir = curpath
	apkFile = target
else:
	apkDir = str( target[0:lastIndexOfASlash] )
	apkDir = os.path.join(curpath, apkDir)
	apkFile = str( target[lastIndexOfASlash:targetNameLen] )

apkAbsPath = os.path.join(apkDir, apkFile)  # the APK package absolute path (from the root)

#Debug:
logger.debug(apkAbsPath)


#Check whether the target APK package exists or not:
if not os.path.isfile(apkFile):
	#Debug:
	logger.error(apkAbsPath + " does NOT exist!")

	#Terminate the script:
	sys.exit()


#Retrieve the output folder name and path:
outputDirectory = str( apkFile[0:targetNameLen-4] )  # the name of the output folder in which copy the extracted files and the analysis results (i.e. the APK package name without the ".apk" extension - e.g. for DroidRoot.A.apk -> DroidRoot.A/)
#------------------------------- END Retrieving parameters. -------------------------------#




#Check whether the output folder exists or not:
if not os.path.exists(outputDirectory):
	#Create the output folder:
	os.makedirs(outputDirectory)

	#Debug:
	logger.info("Creating " + outputDirectory + "/...")




#Launch apktool in order to extract the (decrypted) AndroidManifest.xml, the resources and to generate the disassembled smali files:
shellcommand = "java -jar ninjadroid-libs/apktool1.5.2/apktool.jar -q d -f " + apkAbsPath + " " + outputDirectory
process = subprocess.Popen(shellcommand, stdout=subprocess.PIPE, stderr=None, shell=True)
#result = process.communicate()

#Debug:
logger.info("Creating " + outputDirectory + "/smali/...")
logger.info("Creating " + outputDirectory + "/AndroidManifest.xml...")
logger.info("Creating " + outputDirectory + "/res/...")
logger.info("Creating " + outputDirectory + "/assets/...")




#TODO: UPDATE dex2jar to version 0.0.9.15!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#Launch dex2jar in order to generate a jar file from the classes.dex:
jarFile = outputDirectory + ".jar"
shellcommand = "./ninjadroid-libs/dex2jar-0.0.9.15/d2j-dex2jar.sh -f " + apkAbsPath + " -o " + outputDirectory + "/" + jarFile
process = subprocess.Popen(shellcommand, stdout=subprocess.PIPE, stderr=None, shell=True)
#result = process.communicate()

#Debug:
#logger.info("Creating " + outputDirectory + "/" + jarFile + "...")




#Extract the META-INF/CERT.RSA certificate from the APK package and the classes.dex:
with ZipFile(apkAbsPath) as z:
	with z.open(dexFile) as zf, open(os.path.join(outputDirectory, os.path.basename(dexFile)), 'wb') as f:
		shutil.copyfileobj(zf, f)

		#Debug:
		logger.info("Creating " + outputDirectory + "/classes.dex...")
	with z.open(certDir+certFile) as zf, open(os.path.join(outputDirectory, os.path.basename(certFile)), 'wb') as f:
		shutil.copyfileobj(zf, f)

		#Debug:
		logger.info("Creating " + outputDirectory + "/CERT.RSA...")



#Launch the NinjaDroid statical analysis:
shellcommand = "python ./ninjadroid-libs/evaluateApk.py -n " + os.path.join(curpath, outputDirectory) + " -d " + apkDir + " -t " + apkFile
process = subprocess.Popen(shellcommand, stdout=subprocess.PIPE, stderr=None, shell=True)
result = process.communicate()

#Debug:
logger.info("Creating " + outputDirectory + "/dogwar.html...")
