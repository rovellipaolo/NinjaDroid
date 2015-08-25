NinjaDroid
==========

NinjaDroid is a simple tool to reverse engineering Android APK packages.

NinjaDroid uses a modified version of the Androguard AXMLParser (by Anthony Desnos) together with a series of other Python scripts (by Paolo Rovelli) based on aapt, keytool, string and such to extract a series of information from a given APK package, such as:

- APK file info (i.e. file size, MD5, SHA-1, SHA-256 and SHA-512);
- App info (e.g. app name, package name, version, lists of permissions, list of Activities/Services/BroadcastReceivers, etc...);
- Digital certificate info (e.g. validity, serial number, fingerprint MD5, SHA-1, SHA-256 and signture), including certificate issuer/owner info (e.g. name, email, company, country, etc...);
- All the strings hard-coded into the classes.dex file;
- The URLs and shell commands hard-coded into the classes.dex file;
- AndroidManifest file info (i.e. file size, MD5, SHA-1, SHA-256 and SHA-512);
- classes.dex file info (i.e. file size, MD5, SHA-1, SHA-256 and SHA-512);
- CERT.RSA/DSA file info (i.e. file size, MD5, SHA-1, SHA-256 and SHA-512);
- List of file entries (i.e. file name, file size, MD5, SHA-1, SHA-256 and SHA-512) in the APK package.

Furthermore, NinjaDroid uses apktool (https://code.google.com/p/android-apktool/) and dex2jar (https://code.google.com/p/dex2jar/), together with other Python scripts in order to extract from an APK package:

- classes.dex file;
- translated .jar file (thanks to dex2jar);
- disassembled smali files (thanks to apktool);
- AndroidManifest.xml file (thanks to apktool);
- CERT.RSA file;
- assets/ and res/ folders together with their content (thanks to apktool);
- JSON and HTML report files, which contains all the extracted APK metadata.


Configuration:
=============
After cloning the NinjaDroid repository, or downloading the source code, make sure that 'lib/aapt/aapt', 'lib/apktool1.5.2/apktool.jar' and 'lib/dex2jar-0.0.9.15/d2j-dex2jar.sh' have execute permission.

If you have the Android SDK installed, instead of the included version of aapt, you can use the SDK version. In order to do so, you need to change the aapt location in 'lib/Aapt.py' (i.e. __AAPT_EXEC_PATH = "lib/aapt/aapt").

Linux:
Due to aapt dependencies, on Linux, you may need to install some additional libraries. In particular: 'lib32z1', 'lib32z1-dev' and 'lib32stdc++6'.-

OS X:
If you use NinjaDroid on OS X, you will need to change the 'lib/aapt/aapt' binary with the 'lib/aapt/aapt_osx' one (just rename 'aapt_osx' into 'aapt').


Use:
=============
To use NinjaDroid you just need to copy the APK package you want to analyse into the NinjaDroid directory. Then, launch the command:

$ python ninjadroid.py myPackage.apk

This will produce as output a JSON containing all the extracted APK metadata.

If you want to store the extracted files and info, use the "--extract" option:

$ python ninjadroid.py myPackage.apk --extract

A folder named as the APK package (e.g. 'myPackage/') will be created inside the current working directory (e.g. the NinjaDroid folder). Inside this folder you will find the JSON and HTML report files (e.g. report-myPackage.json and report-myPackage.html), the .jar file (e.g. myPackage.jar) and all the rest of the APK content.

NOTE: The information contained in the HTML report file are a subset of the ones contained in the JSON report file.

It is also possible to launch NinjaDroid on an APK package which is not in the NinjaDroid directory, as well as storing the information in another directory, as follow:

$ python ninjadroid.py /path/to/MyPackage.apk --extract /dir/where/to/extract/

Some APKs which contains many strings may require a considerable amount of time to be processed. You can speed up the process by avoiding to extract URLs and shell commands as follows:

$ python ninjadroid.py --no-string-process myPackage.apk

NOTE: You can of course mix the use of "--no-string-process" and "--export".


Licence:
========
NinjaDroid is licensed under the GNU General Public License v3.0 (http://www.gnu.org/licenses/gpl-3.0.html).
