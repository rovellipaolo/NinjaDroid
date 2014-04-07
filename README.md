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

Finally it creates an HTML report file containing a review of the APK package.
This HTML file contains a simple table with a list of useful information that characterise the app, such as:
- APK package info (e.g. file size, MD5, SHA-256 and SHA-512);
- App info (e.g. package, name, version, lists of permissions, list of Activities/Services/BroadcastReceivers, ecc...)
- Author info (e.g. name, email, company, country, ecc...)
- Digital certificate info (e.g. validity, serial number, MD5, SHA-1, SHA-256 and signture).


Installation:
=============
To use NinjaDroid you just need to copy the APK package you want to reverse engineering into the NinjaDroid directory. Then, launch the command:

python ninjadroid.py -t MyPackage.apk

A folder named as the APK package (e.g. MyPackage/) will be created inside the NinjaDroid directory. Inside this folder you will find the HTML report file (e.g. report-MyPackage.html), the .jar file (e.g. MyPackage.jar) and all the rest of the APK content.

It is also possible to launch NinjaDroid on an APK package which is not in the NinjaDroid directory using the following command:

python ninjadroid.py -t /[AbsolutePathToTheApkFolder]/MyPackage.apk

Please, note that you need to have the Android SDK and Python installed on your computer.


Licence:
========
NinjaDroid is licensed under the GNU General Public License v3.0 (http://www.gnu.org/licenses/gpl-3.0.html).
