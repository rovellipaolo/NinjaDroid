#############################################################################################
# @file ninjadroid.py																		#
# @brief Ninja Reverse Engineering on Android APK packages. 								#
# @license GPLv3 License. 									 								#
# @update 2013-12-07 23:10:00 (Sat Dec 7, 2013 at 11:10 PM)									#
# @author Paolo Rovelli																		#
#############################################################################################


#-------------------------------- BEGIN Import Python types: ------------------------------#
import getopt
import os
import subprocess
import sys
import string
import zipfile
import shutil
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



#------------------------------- BEGIN Retrieving parameters: -----------------------------#
#Example Call: python ninjadroid.py -t DroidRoot.A.apk
#Example Call: python ninjadroid.py -d /Users/paolo/Development/NinjaDroid/ -t DroidRoot.A.apk

#Folders:
curpath = os.path.dirname( os.path.realpath(__file__) )  # the scanned directory (if not specified it will be the current directory)
apkDir = curpath

#Retrieve the user's parameters:
opts, extraparams = getopt.getopt(sys.argv[1:], "d:t:") 
for o,p in opts:
	if o in ['-d', '--dir']:
		apkDir = p
	if o in ['-t', '--target']:
		apkFile = p


#Debug:
print "Directory: " + apkDir
print "Target: " + apkFile

apkExtractedDir = str(apkFile[0:len(apkFile)-4])  # the APK file name without the ".apk" extension (that is also the name of the folder we will create)
apkAbsolutPath = os.path.join(apkDir, apkFile)  # the APK absolute path (from the root)
#------------------------------- END Retrieving parameters. -------------------------------#



if not os.path.isfile(apkFile):
	#Debug:
	print apkAbsolutPath + " does NOT exist!"
else:  # os.path.isfile(apkFile)
	#Move to the scanned directory:
	#os.chdir(apkDir)



	#Launch apktool in order to extract the decrypted AndroidManifest.xml, the resources and to generate the smali code (e.g. DroidRoot.A.apk -> DroidRoot.A/):
	shellcommand = "java -jar ninjadroid-libs/apktool1.5.2/apktool.jar d -f " + apkAbsolutPath + " " + apkExtractedDir
	process = subprocess.Popen(shellcommand, stdout=subprocess.PIPE, stderr=None, shell=True)
	xmlTree = process.communicate()[0]



	#Launch dex2jar in order to generate a jar file from the classes.dex (e.g. DroidRoot.A.apk -> DroidRoot.A.jar):
	shellcommand = "./ninjadroid-libs/dex2jar-0.0.9.13/d2j-dex2jar.sh --force " + apkAbsolutPath + " -o " + apkExtractedDir + "/" + apkExtractedDir + ".jar"
	process = subprocess.Popen(shellcommand, stdout=subprocess.PIPE, stderr=None, shell=True)
	xmlTree = process.communicate()[0]



	#Extract the META-INF/CERT.RSA certificate from the APK package and the classes.dex to the new created folder (e.g. for DroidRoot.A.apk -> DroidRoot.A/):
	with zipfile.ZipFile(apkAbsolutPath) as z:
		with z.open(dexFile) as zf, open(os.path.join(apkExtractedDir, os.path.basename(dexFile)), 'wb') as f:
			shutil.copyfileobj(zf, f)
		with z.open(certDir+certFile) as zf, open(os.path.join(apkExtractedDir, os.path.basename(certFile)), 'wb') as f:
			shutil.copyfileobj(zf, f)



	#Launch RADS (Repackage App Detection System) in order to generate an HTML file with the app details:
	shellcommand = "python ./ninjadroid-libs/RADS/evaluateApk.py -n " + os.path.join(curpath, apkExtractedDir) + " -d " + apkDir + " -t " + apkFile
	process = subprocess.Popen(shellcommand, stdout=subprocess.PIPE, stderr=None, shell=True)
	xmlTree = process.communicate()[0]

