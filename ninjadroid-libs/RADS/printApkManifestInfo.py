###########################################################################################################################
# @file printApkManifestInfo.py                                                                                           #
# @brief Print an APK AndroidManifest's information.                                                                      #
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
#Example Call: python printApkManifestInfo.py -d /Users/paolo/Development/ninjadroid/ -t DroidRoot.A.apk

#Folders:
directory = os.path.dirname( os.path.realpath(__file__) )  # the scanned directory (if not specified it will be the current directory)

#Retrieve the user's parameters:
opts, extraparams = getopt.getopt(sys.argv[1:], "d:t:") 
for o,p in opts:
	if o in ['-d', '--dir']:
		directory = p
	if o in ['-t', '--target']:
		apkfile = p

#Debug:
print "Directory: " + directory
print "Target: " + apkfile
#-------------------------------- END Retrieving parameters. --------------------------------#



#Move to the scanned directory:
os.chdir(directory)


app = App(directory, apkfile)


#Debug:
print "App Package: " + app.getPackage()
print "App Name: " + app.getName()
print "App Version: " + app.getVersion()
print "Target SDK: " + app.getTargetSdk()
print "Activities (" + str(len(app.getActivities())) + "): " + str(app.getActivities())
print "Services (" + str(len(app.getServices())) + "): " + str(app.getServices())
print "BroadcastReceivers (" + str(len(app.getBroadcastReceivers())) + "): " + str(app.getBroadcastReceivers())
print "Permissions (" + str(app.getNumberOfPermissions()) + "): " + str(app.getPermissions())
