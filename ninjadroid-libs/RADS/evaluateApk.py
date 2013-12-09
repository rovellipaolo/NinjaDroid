###########################################################################################################################
# @file evaluateApk.py                                                                                                    #
# @brief Extract all the information from an APK package and save all into an HTML output file.                           #
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



#----------------------------------- BEGIN Configuration: ---------------------------------#
#Output HTML file:
outputFilePrefix = ""
outputFileExtension = ".html"
#outputFileName = outputFilePrefix + outputFileExtension  # "rads-[APKNAME].html"
#----------------------------------- END Configuration. -----------------------------------#



#-------------------------------- BEGIN Retrieving parameters: ------------------------------#
#Example Call: python printApkInfo.py -d /Users/paolo/Development/ninjadroid/ -t DroidRoot.A.apk

#Folders:
apkDir = os.path.dirname( os.path.realpath(__file__) )  # the scanned directory (if not specified it will be the current directory)
ninjadroidDir = apkDir

#Retrieve the user's parameters:
opts, extraparams = getopt.getopt(sys.argv[1:], "n:d:t:") 
for o,p in opts:
	if o in ['-n', '--ninjadroid']:
		ninjadroidDir = p
	if o in ['-d', '--dir']:
		apkDir = p
	if o in ['-t', '--target']:
		apkFile = p

#Debug:
print "Directory: " + apkDir
print "Target: " + apkFile

apkName = apkFile[0:len(apkFile)-4]  # the APK file name without the ".apk" extension (that is also the name of the folder we will create)
#-------------------------------- END Retrieving parameters. --------------------------------#



if not os.path.isfile(apkFile):
	#Debug:
	print apkFile + " does NOT exist!"
else:  # os.path.isfile(apkFile)
	#Customize the file name:
	outputFileName = outputFilePrefix + apkName + outputFileExtension  # "rads-[APKNAME].html"


	#Move to the scanned directory:
	os.chdir(apkDir)


	app = App(apkDir, apkFile)


	#Debug:
	#print "Author Name: " + app.getAuthorName()
	#print "Author Email: " + app.getAuthorEmail()
	#print "Author Company: " + app.getAuthorCompany()
	#print "Author Country: " + app.getAuthorCountry()
	#print "Certificate MD5: " + app.getCertificateMD5()
	#print "App Package: " + app.getPackage()
	#print "App Name: " + app.getName()
	#print "App Version: " + app.getVersion()
	#print "Target SDK: " + app.getTargetSdk()
	#print "Activities (" + str(len(app.getActivities())) + "): " + str(app.getActivities())
	#print "Services (" + str(len(app.getServices())) + "): " + str(app.getServices())
	#print "BroadcastReceivers (" + str(len(app.getBroadcastReceivers())) + "): " + str(app.getBroadcastReceivers())
	#print "Permissions (" + str(app.getNumberOfPermissions()) + "): " + str(app.getPermissions())

	#Move to the directory in which to save the output path:
	os.chdir(ninjadroidDir)

	#-------------------------------- BEGIN Table header: ------------------------------#
	table = "<html>" + "\n"
	table += "\t<table border=\"1\" cellspacing=\"0\" cellpadding=\"10\">" + "\n"
	table += "\t\t<tr style='font-size: 150%; font-weight: bold;'>" + "\n"
	table += "\t\t\t<td colspan=\"2\" style=\"text-align: center;\">" + apkFile + "</td>" + "\n"
	table += "\t\t</tr>" + "\n"


	#Open file and append the instance:
	fp = open(outputFileName, "w")  # b: write only (overwrites the file or creates a new one)

	#Write to the file:
	#fp.write(table)

	#Close file:
	#fp.close()
	#-------------------------------- END Table header. --------------------------------#



	#Open file and append the instance:
	#fp = open(outputFileName, "a")  # a: open for appending

	table += "\t\t<tr>" + "\n"
	table += "\t\t\t<td>App Name:</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">" + app.getName() + "</td>" + "\n"
	table += "\t\t</tr>" + "\n"

	table += "\t\t<tr>" + "\n"
	table += "\t\t\t<td>Package:</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">" + app.getPackage() + "</td>" + "\n"
	table += "\t\t</tr>" + "\n"

	table += "\t\t<tr>" + "\n"
	table += "\t\t\t<td>Version:</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">" + app.getVersion() + "</td>" + "\n"
	table += "\t\t</tr>" + "\n"

	table += "\t\t<tr>" + "\n"
	table += "\t\t\t<td>Target SDK:</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">" + app.getTargetSdk() + "</td>" + "\n"
	table += "\t\t</tr>" + "\n"

	table += "\t\t<tr>" + "\n"
	table += "\t\t\t<td>Author:</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">\n"
	if app.getAuthorName() != "":
		table += "\t\t\t\t" + app.getAuthorName() + "<br />\n"
	if app.getAuthorEmail() != "":
		table += "\t\t\t\t" + app.getAuthorEmail() + "<br />\n"
	if app.getAuthorCompany() != "":
		table += "\t\t\t\t" + app.getAuthorCompany() + "<br />\n"
	if app.getAuthorCountry() != "":
		table += "\t\t\t\t" + app.getAuthorCountry() + "\n"
	table += "\t\t\t</td>" + "\n"
	table += "\t\t</tr>" + "\n"

	table += "\t\t<tr>" + "\n"
	table += "\t\t\t<td>Author Certificate MD5:</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">" + app.getCertificateMD5() + "</td>" + "\n"
	table += "\t\t</tr>" + "\n"

	table += "\t\t<tr>" + "\n"
	table += "\t\t\t<td>Permissions:</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">\n"
	for permission in app.getPermissions():
		table += "\t\t\t\t" + permission + "<br />\n"
	table += "\t\t\t</td>" + "\n"
	table += "\t\t</tr>" + "\n"

	table += "\t\t<tr>" + "\n"
	table += "\t\t\t<td>Activities:</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">\n"
	for activity in app.getActivities():
		table += "\t\t\t\t" + activity + "<br />\n"
	table += "\t\t\t</td>" + "\n"
	table += "\t\t</tr>" + "\n"

	table += "\t\t<tr>" + "\n"
	table += "\t\t\t<td>Services:</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">\n"
	for service in app.getServices():
		table += "\t\t\t\t" + service + "<br />\n"
	table += "\t\t\t</td>" + "\n"
	table += "\t\t</tr>" + "\n"

	table += "\t\t<tr>" + "\n"
	table += "\t\t\t<td>BroadcastReceivers:</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">\n"
	for receiver in app.getBroadcastReceivers():
		table += "\t\t\t\t" + receiver + "<br />\n"
	table += "\t\t\t</td>" + "\n"
	table += "\t\t</tr>" + "\n"


	#Append to the file:
	#fp.write(instance)

	#Close file:
	#fp.close()



	#-------------------------------- BEGIN Table footer: ------------------------------#
	table += "\t</table>" + "\n"
	table += "</html>" + "\n"


	#Open file and append the instance:
	#fp = open(outputFileName, "a")  # a: open for appending

	#Write to the file:
	fp.write(table)

	#Close file:
	fp.close()
	#-------------------------------- END Table footer. --------------------------------#

	#Debug:
	print outputFileName + " was created!"
