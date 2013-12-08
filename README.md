NinjaDroid
==========

NinjaDroid is a simple tool to reverse engineering Android APK packages.

NinjaDroid uses apktool (https://code.google.com/p/android-apktool/) and dex2jar (https://code.google.com/p/dex2jar/), together with other Python scripts in order to extract from an APK package:

- the classes.dex file
- the translated .jar file (thanks to dex2jar)
- the disassembled smali files (thanks to apktool);
- the AndroidManifest.xml file (thanks to apktool);
- the CERT.RSA file;
- the assets/ and res/ folders together with their content (thanks to apktool);

Finally it creates an HTML report file containing a review of the APK package. This HTML file contains a simple table with a list of useful information that characterize the app (e.g. its name, package, version and author, together with the lists of permissions, Activities, Services and BroadcastReceiver).
Use NinjaDroid


Installation:
=============
To use NinjaDroid you just need to copy the APK package you want to reverse engineering into the NinjaDroid directory. Then, launch the command:

python ninjadroid.py -t MyPackage.apk

A folder named as the APK package (e.g. MyPackage/) will be created inside the NinjaDroid directory. Inside this folder you will find the HTML report file (e.g. MyPackage.html), the .jar file (e.g. MyPackage.jar) and all the rest of the APK content.

It is also possible to launch NinjaDroid on an APK package which is not in the NinjaDroid directory using the following command:

python ninjadroid.py -d /[AbsolutePathToTheApkFolder]/ -t MyPackage.apk


Licence:
========
NinjaDroid is licensed under the GNU General Public License v3.0 (http://www.gnu.org/licenses/gpl-3.0.html).
