NinjaDroid
==========

NinjaDroid is a simple tool to reverse engineering Android APK packages.

## Overview:

NinjaDroid uses a modified version of the Androguard `AXMLParser` (by Anthony Desnos) together with a series of other Python scripts (by Paolo Rovelli) based on `aapt`, `keytool`, string and such to extract a series of information from a given APK package, such as:

- APK file info (i.e. file size, MD5, SHA-1, SHA-256 and SHA-512);
- App info (e.g. app name, package name, version, lists of permissions, list of Activities/Services/BroadcastReceivers, etc...);
- Digital certificate info (e.g. validity, serial number, fingerprint MD5, SHA-1, SHA-256 and signture), including certificate issuer/owner info (e.g. name, email, company, country, etc...);
- All the strings hard-coded into the classes.dex file;
- The URLs and shell commands hard-coded into the classes.dex file;
- AndroidManifest file info (i.e. file size, MD5, SHA-1, SHA-256 and SHA-512);
- classes.dex file info (i.e. file size, MD5, SHA-1, SHA-256 and SHA-512);
- CERT.RSA/DSA file info (i.e. file size, MD5, SHA-1, SHA-256 and SHA-512);
- List of file entries (i.e. file name, file size, MD5, SHA-1, SHA-256 and SHA-512) in the APK package.

Furthermore, NinjaDroid uses apktool (https://github.com/iBotPeaches/Apktool) and dex2jar (https://github.com/pxb1988/dex2jar), together with other Python scripts in order to extract from an APK package:

- classes.dex file;
- translated .jar file (thanks to `dex2jar`);
- disassembled smali files (thanks to `apktool`);
- AndroidManifest.xml file (thanks to `apktool`);
- CERT.RSA file;
- assets/ and res/ folders together with their content (thanks to `apktool`);
- JSON and HTML report files, which contains all the extracted APK metadata.


## Docker:

There's a dockerfile to package up all the requisite things. To use it:

Have an APK to analyze, and move it to `./apks`.

Print out the JSON analysis:

```sh
docker build -t ninjadroid:latest .
docker run -it --rm -v $(pwd)/apks:/apks ninjadroid:latest json /apks/my-app.apk
```


**To create all output files:**

```sh
docker run --rm -v $(pwd)/apks:/apks -v $(pwd)/output:/output ninjadroid:latest ninjadroid -e /output /apks/my-app.apk
```

Open up the `./output` folder and find your JSON and HTML analyses.


## Configuration:
After cloning the NinjaDroid repository, or downloading the source code, make sure that `aapt`, `apktool` and `dex2jar` have execute permission.

```
$ sudo chmod 755 ninjadroid/aapt/aapt
$ sudo chmod 755 ninjadroid/apktool/apktool.jar
$ sudo chmod 755 ninjadroid/dex2jar/d2j-dex2jar.sh
```

If you have the Android SDK installed, instead of the included version of aapt, you can use the SDK version. In order to do so, you need to change the aapt location in 'ninjadroid/aapt/Aapt.py' (i.e. __AAPT_EXEC_PATH = "ninjadroid/aapt/aapt").

*MacOS:*

No particular operation needed.

*Linux:*

If you use NinjaDroid on Linux, you will need to change the 'aapt' binary with the 'aapt_linux' one in ninjadroid/aapt/ (just change the aapt location in 'ninjadroid/aapt/Aapt.py', or simply rename 'aapt_linux' into 'aapt').

Due to `aapt` dependencies, on Linux, you may need to install some additional libraries such as: 'lib32z1', 'lib32z1-dev' and 'lib32stdc++6'.

For example, in Ubuntu:

```
$ sudo apt-get install lib32z1 lib32z1-dev lib32stdc++6
```

## Run:
To execute NinjaDroid, you need `Python 3.5` or higher.

To use NinjaDroid you just need to copy the APK package you want to analyse into the NinjaDroid directory. Then, launch the command:

```
$ python ninjadroid.py myPackage.apk
```

This will produce as output a JSON containing all the extracted APK metadata.

If you want to store the extracted files and info, use the "--extract" option:

```
$ python ninjadroid.py myPackage.apk --extract
```

A folder named as the APK package (e.g. 'myPackage/') will be created inside the current working directory (e.g. the NinjaDroid folder). Inside this folder you will find the JSON and HTML report files (e.g. report-myPackage.json and report-myPackage.html), the .jar file (e.g. myPackage.jar) and all the rest of the APK content.

NOTE: The information contained in the HTML report file are a subset of the ones contained in the JSON report file.

It is also possible to launch NinjaDroid on an APK package which is not in the NinjaDroid directory, as well as storing the information in another directory, as follow:

```
$ python ninjadroid.py /path/to/MyPackage.apk --extract /dir/where/to/extract/
```

Some APKs which contains many strings may require a considerable amount of time to be processed. You can speed up the process by avoiding to extract URLs and shell commands as follows:

```
$ python ninjadroid.py --no-string-process myPackage.apk
```

NOTE: You can of course mix the use of `--no-string-process` and `--export`.


## Run Tests:
To run tests, launch the command:
```
$ python -m unittest -v tests.test
```

The Docker image can also be used for testing:

```
$ make build
Sending build context to Docker daemon  84.12MB
Step 1/24 : FROM openjdk:8u212-jre-slim-stretch
[...]
Successfully built 0993636e7d79

$ make docker-test
test_get_app_name (tests.test_apk.TestAPK) ... ok
test_get_file_list (tests.test_apk.TestAPK) ... ok
[...]

----------------------------------------------------------------------
Ran 75 tests in 4.372s

OK
```

To test changes to the code (or test files) without rebuilding the docker image:

```
$ docker run -w /opt/NinjaDroid/ -v $(pwd)/ninjadroid/parsers:/opt/NinjaDroid/ninjadroid/parsers -v $(pwd)/tests:/opt/NinjaDroid/tests --rm -it ninjadroid:latest python3 -m unittest tests.test
...........................................................................
----------------------------------------------------------------------
Ran 75 tests in 4.325s

OK
```

## Licence:

NinjaDroid is licensed under the GNU General Public License v3.0 (http://www.gnu.org/licenses/gpl-3.0.html).


## Sample JSON output

I truncated some of the massively repeated sections, but here's what the structure of the output looks like:

```json
{
    "app_name": "Fun Checkers",
    "cert": {
        "file": "META-INF/GOOGPLAY.RSA",
        "fingerprint": {
            "md5": "12:7B:5F:F4:18:B3:B6:27:2D:87:09:A2:18:11:89:37",
            "sha1": "7A:8C:D8:D2:18:35:0A:83:9E:FE:90:BF:A7:9B:6C:9E:FE:98:7B:22",
            "sha256": "CF:A8:82:8B:31:AD:E2:7C:0E:2C:01:D4:B3:B2:98:51:35:4A:90:95:63:B6:B7:BD:2B:DF:D2:9F:9B:EA:F3:39",
            "signature": "SHA256withRSA",
            "version": "3"
        },
        "issuer": {
            "city": "Mountain View",
            "country": "US",
            "domain": "",
            "email": "",
            "label": "",
            "name": "Android",
            "organization": "Google Inc.",
            "state": "California",
            "unit": "Android"
        },
        "md5": "b9113e21310c36a310290c776c7b4981",
        "owner": {
            "city": "Mountain View",
            "country": "US",
            "domain": "",
            "email": "",
            "label": "",
            "name": "Android",
            "organization": "Google Inc.",
            "state": "California",
            "unit": "Android"
        },
        "serial_number": "8d7eb2379feba7eead0385e0283fdd884660382d",
        "sha1": "605bf5f0c6ee0902d71d4a01417aef04a4f4678c",
        "sha256": "688720c8812cc079373a9c998400e1e5b5b100cc275057428a65c8f492fd18d2",
        "sha512": "01a1da0bb9462a435a2a0b6af8e10724d94ecc7d96102b6c0e89f1f20d1a516e13ce7772c0c2eb97907083f34174b17941a672325731bf06f81b38c76e9321c6",
        "size": 2172,
        "validity": {
            "from": "2018-12-06 09:50:27Z",
            "until": "2048-12-06 09:50:27Z"
        }
    },
    "dex": {
        "file": "classes.dex",
        "md5": "1ddd9fbafb57c87bb8c0a015e9868c88",
        "sha1": "59bc17a9c64c9b362cf4c73b2a7faf76bd6a4bda",
        "sha256": "098f32d4ad99e8a6862db6c231dba39e82d95c347157518d002a8b4beb1fb3a4",
        "sha512": "24141708c62ece196060003f3dd2b4cb3e749aedfb3f05f8b77e37ff39681aa1b095e70bc4871c863d8143773b34e08d2b7df1df82e764ea59b1e8e791db73f0",
        "shell_commands": [
            "\"Landroid/database/ContentObserver;",
            "\"Landroid/database/DataSetObserver;",
            "#SH",
            "#Sh",
            "(Landroid/arch/persistence/room/Database;",
            "(Landroid/database/sqlite/SQLiteDatabase;",
            // <snip>
            "tc",
            "toP",
            "top",
            "top must be nonnegative",
            "uptime",
            "vDC"
        ],
        "size": 4225184,
        "strings": [
            "3?",
            "mState=",
            "(extras=",
            "header:",
            // <snip>
            "~The Google Play services resources were not found. Check your project configuration to ensure that the resources are included.",
            "~Y\\\\\\D3A",
            "~Y|jK",
            "~_n0"
        ],
        "urls": [
            "0android.bluetooth.device.action.AC",
            "0android.support.customtabs.extra.SH",
            "0android.support.v4.media.session.ac",
            "0com.facebook.platform.action.request.LI",
            "1.2.2.142",
            // <snip>
            "https://www.googleapis.com/auth/plus.login",
            "https://www.googleapis.com/auth/plus.me",
            "icon.pn",
            "id.li",
            "vnd.crashlytics.android.events",
            "window.AF",
            "www.google.com"
        ]
    },
    "file": "/apks/0040344becfad6fbada8aea0a628c0883f9aaa29db2c2ed632452cf6a8a2d8b1.apk",
    "manifest": {
        "activities": [
            {
                "configChanges": "0x00000FB0",
                "name": "com.google.android.gms.ads.AdActivity",
                "theme": "@android:0103000F"
            },
            {
                "name": "com.tmgames.checkers.statistics.StatisticsActivity"
            },
            {
                "name": "com.google.android.gms.ads.purchase.InAppPurchaseActivity",
                "theme": "@7F0C014B"
            },
            {
                "exported": "true",
                "intent-filter": [
                    {
                        "action": [
                            "com.google.android.gms.appinvite.ACTION_PREVIEW"
                        ],
                        "category": [
                            "android.intent.category.DEFAULT"
                        ]
                    }
                ],
                "name": "com.google.android.gms.appinvite.PreviewActivity",
                "theme": "@7F0C0143"
            },
            // <snip>
        ],
        "file": "AndroidManifest.xml",
        "md5": "d9889e18d5ca404608a9258848cd3287",
        "package_name": "com.shuangq0929.fun.checkers",
        "permissions": [
            "android.permission.ACCESS_COARSE_LOCATION",
            "android.permission.ACCESS_COARSE_LOCATION",
            "android.permission.ACCESS_FINE_LOCATION",
            "android.permission.ACCESS_NETWORK_STATE",
            // <snip>
            "com.sec.android.provider.badge.permission.WRITE",
            "com.shuangq0929.fun.checkers.permission.C2D_MESSAGE",
            "com.sonyericsson.home.permission.BROADCAST_BADGE"
        ],
        "receivers": [
            {
                "exported": "false",
                "name": "com.google.firebase.iid.FirebaseInstanceIdInternalReceiver"
            },
            {
                "name": "com.tushu.outlibrary.receive.RefreashConfigReceiver"
            },
            {
                "exported": "false",
                "intent-filter": [
                    {
                        "action": [
                            "com.facebook.sdk.ACTION_CURRENT_ACCESS_TOKEN_CHANGED"
                        ]
                    }
                ],
                "name": "com.facebook.CurrentAccessTokenExpirationBroadcastReceiver"
            },
            {
                "name": "com.tushu.outlibrary.receive.LockScreenReceiver"
            },
            // <snip>
        ],
        "sdk": {
            "min": "15",
            "target": "26"
        },
        "services": [
            {
                "exported": "true",
                "intent-filter": [
                    {
                        "action": [
                            "com.google.firebase.INSTANCE_ID_EVENT"
                        ],
                        "priority": "-500"
                    }
                ],
                "name": "com.google.firebase.iid.FirebaseInstanceIdService"
            },
            {
                "exported": "false",
                "name": "com.facebook.ads.internal.ipc.AdsProcessPriorityService"
            },
            // <snip>
        ],
        "sha1": "8072fb9a357dc3fef4b00c7e21a058558ced66a1",
        "sha256": "30b861a0202d4e5b7a6d0654aee81ce6e20f62166fc98592d101a35a294a66ca",
        "sha512": "c8178f3dade78da49a6d70dd1b76f648b0cd9ec71c97fe5d87236b566b78d901c173a0cfba8c00c2c60c891b87c703c292b3627671a677112fc5674e17abfaca",
        "size": 28640,
        "version": {
            "code": 17,
            "name": "1.1.6"
        }
    },
    "md5": "52554bdf442da46e3c037ba40475beb7",
    "other_files": [
        {
            "file": "androidsupportmultidexversion.txt",
            "md5": "0b13c8b4e813c60e0fdaf75f8d82e1fc",
            "sha1": "d5ef2133c35386a565f5e14140b508f7abbbb895",
            "sha256": "822dca0ed97b7639d81c9c5704a5172403e70ce03149ed586d84325b9a438e43",
            "sha512": "d9ebe674d203fb0926e7d661223c64e2c564ada6a4f4020977f7213e435b1ed8b5627b028fcda48a1575f6eaf6a4ac064bb3f662ca4db71e7340280378ad479e",
            "size": 53
        },
        {
            "file": "assets/com.shuangq0929.fun.checkers_v42.json",
            "md5": "cf4c937a749e7cd8461ac82e21c27bdd",
            "sha1": "8e6bed86ca74d64a6116dbf6f7a1372aedb36362",
            "sha256": "104d52eb5fd6af04dcdee1d15190f5e9f6f179f1c560dfcd2724fdc20c6550c7",
            "sha512": "bd28ab89eb01f603236341f6414f69b8df409e2243ba0c4e70f513c220eb22fe1c16383cdda27e6151efdadc549f3c903932b48803f86f9a1ab8d62323e5c0a3",
            "size": 4664
        },
        // <snip>
        {
            "file": "META-INF/MANIFEST.MF",
            "md5": "36ee06eaeb4501c09cf2cd3068604883",
            "sha1": "aa83af7e52d0e81965b49f9895d4de542c355600",
            "sha256": "51d3480d828d04ee54f708635d9c0ccdf449db7fdd5b771e8b91fabd8fdf57e8",
            "sha512": "9223faaa1b0d27efa98fa9cfc60193b4abd69907232cb2bb78b9743b7a740e0af1bbfb14fd4be4307084c4c5b244a66699101e7b13c180c16a2c7282127af25c",
            "size": 88954
        }
    ],
    "sha1": "c0682c62a3c8c116691fe5a8093cab39e2abaca1",
    "sha256": "0040344becfad6fbada8aea0a628c0883f9aaa29db2c2ed632452cf6a8a2d8b1",
    "sha512": "a222ffd7e8fde71c0b231db7356e17f576a80accaf2dab99475cc989baab2df1bccfc46679ce97f610d186c058b0434adac29cd63cffd525a433ff5a35b4d537",
    "size": 7631744
}
```
