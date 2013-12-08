###########################################################################################################################
# @file printApkInfo.py                                                                                                   #
# @brief Print all the retrieved information about a particular APK.                                                      #
# @update 2013-11-20 19:59:00 (Wed Nov 20, 2013 at 7:59 PM)                                                               #
# @author Paolo Rovelli                                                                                                   #
###########################################################################################################################


#-------------------------------- BEGIN Import Python types: ------------------------------#
import os
import getopt
#-------------------------------- END Import Python types. --------------------------------#


#-------------------------------- BEGIN Import Classes: -----------------------------------#
from App import *
#-------------------------------- END Import Classes. -------------------------------------#



#-------------------------------- BEGIN Retrieving parameters: ------------------------------#
#Example Call: python printApkInfo.py -d /Users/paolo/Development/ninjadroid/ -t DroidRoot.A.apk

#Folders:
apkDir = os.path.dirname( os.path.realpath(__file__) )  # the scanned directory (if not specified it will be the current directory)

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
#-------------------------------- END Retrieving parameters. --------------------------------#
	


#Move to the scanned directory:
os.chdir(apkDir)


app = App(apkDir, apkFile)


#Debug:
print "Author Name: " + app.getAuthorName()
print "Author Email: " + app.getAuthorEmail()
print "Author Company: " + app.getAuthorCompany()
print "Author Country: " + app.getAuthorCountry()
print "Certificate MD5: " + app.getCertificateMD5()
print "App Package: " + app.getPackage()
print "App Name: " + app.getName()
print "App Version: " + app.getVersion()
print "Target SDK: " + app.getTargetSdk()
print "Activities (" + str(len(app.getActivities())) + "): " + str(app.getActivities())
print "Services (" + str(len(app.getServices())) + "): " + str(app.getServices())
print "BroadcastReceivers (" + str(len(app.getBroadcastReceivers())) + "): " + str(app.getBroadcastReceivers())
print "Permissions (" + str(app.getNumberOfPermissions()) + "): " + str(app.getPermissions())
