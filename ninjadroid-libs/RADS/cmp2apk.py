###########################################################################################################################
# @file cmp2apk.py 		                                                                                                  #
# @brief Extract all the information from two APK packages and comapare them.                           				  #
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
outputFilePrefix = "rads-"
outputFileExtension = ".html"
#outputFileName = outputFilePrefix + outputFileExtension  # "rads-[APKNAME].html"
#----------------------------------- END Configuration. -----------------------------------#



#-------------------------------- BEGIN Retrieving parameters: ------------------------------#
#Example Call: python printApkInfo.py -d /Users/paolo/Development/ninjadroid/ -t DroidRoot.A.apk

#Folders:
apkDir = os.path.dirname( os.path.realpath(__file__) )  # the scanned directory (if not specified it will be the current directory)

#Retrieve the user's parameters:
opts, extraparams = getopt.getopt(sys.argv[1:], "d:o:r:") 
for o,p in opts:
	if o in ['-d', '--dir']:
		apkDir = p
	if o in ['-o', '--original']:
		apkFile1 = p
	if o in ['-r', '--repackaged']:
		apkFile2 = p

#Debug:
print "Directory: " + apkDir
print "Target 1: " + apkFile1
print "Target 2: " + apkFile2

apkName1 = apkFile1[0:len(apkFile1)-4]  # the APK file name without the ".apk" extension (that is also the name of the folder we will create)
apkName2 = apkFile2[0:len(apkFile2)-4]  # the APK file name without the ".apk" extension (that is also the name of the folder we will create)
#-------------------------------- END Retrieving parameters. --------------------------------#



if not os.path.isfile(os.path.join(apkDir, apkFile1)):
	#Debug:
	print apkFile1 + " does NOT exist!"
elif not os.path.isfile(os.path.join(apkDir, apkFile2)):
	#Debug:
	print apkFile2 + " does NOT exist!"
else:  # os.path.isfile(apkFile1) && os.path.isfile(apkFile2)
	#Customize the file name:
	outputFileName = outputFilePrefix + apkName1 + "-" + apkName2 + outputFileExtension  # "rads-[APKNAME].html"


	#Move to the scanned directory:
	os.chdir(apkDir)


	app1 = App(apkDir, apkFile1)
	app2 = App(apkDir, apkFile2)


	#Compare the two apps:
	if app1.getAuthorName() != app2.getAuthorName():
		print "> Different author name!"

	if app1.getCertificateMD5() != app2.getCertificateMD5():
		print "> Different certificate MD5 fingerprint!"

	if app1.getPackage() != app2.getPackage():
		print "> Different package name!"

	if app1.getName() != app2.getName():
		print "> Different app name!"

	if app1.getVersion() != app2.getVersion():
		print "> Different app version!"

	#Debug:
	#print "Author Name: " + app1.getAuthorName()
	#print "Author Email: " + app1.getAuthorEmail()
	#print "Author Company: " + app1.getAuthorCompany()
	#print "Author Country: " + app1.getAuthorCountry()
	#print "Certificate MD5: " + app1.getCertificateMD5()
	#print "App Package: " + app1.getPackage()
	#print "App Name: " + app1.getName()
	#print "App Version: " + app1.getVersion()
	#print "Target SDK: " + app1.getTargetSdk()
	#print "Activities (" + str(len(app1.getActivities())) + "): " + str(app1.getActivities())
	#print "Services (" + str(len(app1.getServices())) + "): " + str(app1.getServices())
	#print "BroadcastReceivers (" + str(len(app1.getBroadcastReceivers())) + "): " + str(app1.getBroadcastReceivers())
	#print "Permissions (" + str(app1.getNumberOfPermissions()) + "): " + str(app1.getPermissions())



	#-------------------------------- BEGIN Table header: ------------------------------#
	table = "<html>" + "\n"
	table += "\t<table border=\"1\" cellspacing=\"0\" cellpadding=\"10\">" + "\n"
	table += "\t\t<tr style='font-size: 150%; font-weight: bold;'>" + "\n"
	table += "\t\t\t<td colspan=\"2\" style=\"text-align: center;\">" + apkFile1 + "</td>" + "\n"
	table += "\t\t\t<td colspan=\"2\" style=\"text-align: center;\">" + apkFile2 + "</td>" + "\n"
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
	table += "\t\t\t<td style=\"font-weight: bold;\">" + app1.getName() + "</td>" + "\n"
	if app1.getName() != app2.getName():
		table += "\t\t\t<td style=\"font-weight: bold; color: #FF0000;\">"
	else:  # app1.getName() == app2.getName()
		table += "\t\t\t<td style=\"font-weight: bold;\">"
	table += app2.getName() + "</td>" + "\n"
	table += "\t\t</tr>" + "\n"

	table += "\t\t<tr>" + "\n"
	table += "\t\t\t<td>Package:</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">" + app1.getPackage() + "</td>" + "\n"
	if app1.getPackage() != app2.getPackage():
		table += "\t\t\t<td style=\"font-weight: bold; color: #FF0000;\">"
	else:  # app1.getPackage() == app2.getPackage()
		table += "\t\t\t<td style=\"font-weight: bold;\">"
	table += app2.getPackage() + "</td>" + "\n"
	table += "\t\t</tr>" + "\n"

	table += "\t\t<tr>" + "\n"
	table += "\t\t\t<td>Version:</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">" + app1.getVersion() + "</td>" + "\n"
	if app1.getVersion() != app2.getVersion():
		table += "\t\t\t<td style=\"font-weight: bold; color: #FF0000;\">"
	else:  # app1.getVersion() == app2.getVersion()
		table += "\t\t\t<td style=\"font-weight: bold;\">"
	table += app2.getVersion() + "</td>" + "\n"
	table += "\t\t</tr>" + "\n"

	table += "\t\t<tr>" + "\n"
	table += "\t\t\t<td>Target SDK:</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">" + app1.getTargetSdk() + "</td>" + "\n"
	if app1.getTargetSdk() != app2.getTargetSdk():
		table += "\t\t\t<td style=\"font-weight: bold; color: #FF0000;\">"
	else:  # app1.getTargetSdk() == app2.getTargetSdk()
		table += "\t\t\t<td style=\"font-weight: bold;\">"
	table += app2.getTargetSdk() + "</td>" + "\n"
	table += "\t\t</tr>" + "\n"

	table += "\t\t<tr>" + "\n"
	table += "\t\t\t<td>Author:</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">\n"
	if app1.getAuthorName() != "":
		table += "\t\t\t\t" + app1.getAuthorName() + "<br />\n"
	if app1.getAuthorEmail() != "":
		table += "\t\t\t\t" + app1.getAuthorEmail() + "<br />\n"
	if app1.getAuthorCompany() != "":
		table += "\t\t\t\t" + app1.getAuthorCompany() + "<br />\n"
	if app1.getAuthorCountry() != "":
		table += "\t\t\t\t" + app1.getAuthorCountry() + "\n"
	table += "\t\t\t</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">\n"
	if app1.getAuthorName() != app2.getAuthorName():  # different author name...
		table += "\t\t\t\t<span style=\"color: #FF0000;\">" + app1.getAuthorName() + "</span><br />\n"
	else:  # app1.getAuthorName() == app2.getAuthorName()
		table += "\t\t\t\t" + app1.getAuthorName() + "<br />\n"
	if app1.getAuthorEmail() != app2.getAuthorEmail():  # different author email...
		table += "\t\t\t\t<span style=\"color: #FF0000;\">" + app1.getAuthorEmail() + "</span><br />\n"
	else:  # app1.getAuthorEmail() == app2.getAuthorEmail()
		table += "\t\t\t\t" + app1.getAuthorEmail() + "<br />\n"
	if app1.getAuthorCompany() != app2.getAuthorCompany():  # different author company name...
		table += "\t\t\t\t<span style=\"color: #FF0000;\">" + app1.getAuthorCompany() + "</span><br />\n"
	else:  # app1.getAuthorCompany() == app2.getAuthorCompany()
		table += "\t\t\t\t" + app1.getAuthorCompany() + "<br />\n"
	if app1.getAuthorCountry() != app2.getAuthorCountry():  # different author country...
		table += "\t\t\t\t<span style=\"color: #FF0000;\">" + app1.getAuthorCountry() + "</span><br />\n"
	else:  # app1.getAuthorCountry() == app2.getAuthorCountry()
		table += "\t\t\t\t" + app1.getAuthorCountry() + "<br />\n"
	table += "\t\t\t</td>" + "\n"
	table += "\t\t</tr>" + "\n"

	table += "\t\t<tr>" + "\n"
	table += "\t\t\t<td>Author Certificate MD5:</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">" + app1.getCertificateMD5() + "</td>" + "\n"
	if app1.getCertificateMD5() != app2.getCertificateMD5():  # different author certificate MD5 fingerprints...
		table += "\t\t\t<td style=\"font-weight: bold; color: #FF0000;\">"
	else:  # app1.getCertificateMD5() == app2.getCertificateMD5()
		table += "\t\t\t<td style=\"font-weight: bold;\">"
	table += app2.getCertificateMD5() + "</td>" + "\n"
	table += "\t\t</tr>" + "\n"

	table += "\t\t<tr>" + "\n"
	table += "\t\t\t<td>Permissions:</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">\n"
	for permission in app1.getPermissions():
		table += "\t\t\t\t" + permission + "<br />\n"
	table += "\t\t\t</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">\n"
	app1Permissions = app1.getPermissions()
	for permission in app2.getPermissions():
		if permission not in app1Permissions:  # the permission has been added later on...
			table += "\t\t\t\t<span style=\"color: #FF0000;\">" + permission + "</span><br />\n"
		else:  # permission in app1Permissions
			table += "\t\t\t\t" + permission + "<br />\n"
	table += "\t\t\t</td>" + "\n"
	table += "\t\t</tr>" + "\n"

	table += "\t\t<tr>" + "\n"
	table += "\t\t\t<td>Activities:</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">\n"
	for activity in app1.getActivities():
		table += "\t\t\t\t" + activity + "<br />\n"
	table += "\t\t\t</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">\n"
	app1Activities = app1.getActivities()
	for activity in app2.getActivities():
		if activity not in app1Activities:  # the Activity has been added later on...
			table += "\t\t\t\t<span style=\"color: #FF0000;\">" + activity + "</span><br />\n"
		else:  # activity in app1Activities
			table += "\t\t\t\t" + activity + "<br />\n"
	table += "\t\t\t</td>" + "\n"
	table += "\t\t</tr>" + "\n"

	table += "\t\t<tr>" + "\n"
	table += "\t\t\t<td>Services:</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">\n"
	for service in app1.getServices():
		table += "\t\t\t\t" + service + "<br />\n"
	table += "\t\t\t</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">\n"
	app1Services = app1.getServices()
	for service in app2.getServices():
		if service not in app1Services:  # the Service has been added later on...
			table += "\t\t\t\t<span style=\"color: #FF0000;\">" + service + "</span><br />\n"
		else:  # service in app1Services
			table += "\t\t\t\t" + service + "<br />\n"
	table += "\t\t\t</td>" + "\n"
	table += "\t\t</tr>" + "\n"

	table += "\t\t<tr>" + "\n"
	table += "\t\t\t<td>BroadcastReceivers:</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">\n"
	for receiver in app1.getBroadcastReceivers():
		table += "\t\t\t\t" + receiver + "<br />\n"
	table += "\t\t\t</td>" + "\n"
	table += "\t\t\t<td style=\"font-weight: bold;\">\n"
	app1BroadcastReceivers = app1.getBroadcastReceivers()
	for receiver in app2.getBroadcastReceivers():
		if receiver not in app1BroadcastReceivers:  # the Service has been added later on...
			table += "\t\t\t\t<span style=\"color: #FF0000;\">" + receiver + "</span><br />\n"
		else:  # receiver in app1BroadcastReceivers
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
