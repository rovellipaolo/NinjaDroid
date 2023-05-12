NinjaDroid
==========

NinjaDroid is a simple tool to reverse engineering Android APK packages.

Published at: [https://snapcraft.io/ninjadroid](https://snapcraft.io/ninjadroid)
```shell
$ snap install ninjadroid --channel=beta
```

[![Build Status: GitHub Actions](https://github.com/rovellipaolo/NinjaDroid/actions/workflows/ci.yml/badge.svg)](https://github.com/rovellipaolo/NinjaDroid/actions)
[![Test Coverage: Coveralls](https://coveralls.io/repos/github/rovellipaolo/NinjaDroid/badge.svg)](https://coveralls.io/github/rovellipaolo/NinjaDroid)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/ninjadroid)

![NinjaDroid](docs/images/ninjadroid.gif "Screencast of NinjaDroid")



## Overview

NinjaDroid uses [AXMLParser](https://github.com/appknox/pyaxmlparser) together with a series of Python scripts based on `aapt`, `keytool`, `string` and such to extract a series of information from a given APK package, such as:

- List of files of the APK: file name, size, MD5, SHA-1, SHA-256 and SHA-512
- `AndroidManifest.xml` info: app name, package name, version, sdks, permissions, activities, services, broadcast-receivers, ...
- `CERT.RSA/DSA` digital certificate info: serial number, validity, fingerprint, issuer and owner
- List of URLs, shell commands and other generic strings hard-coded into the `classes.dex` files

Furthermore, NinjaDroid uses [apktool](https://github.com/iBotPeaches/Apktool) and [dex2jar](https://github.com/pxb1988/dex2jar) to extract and store:

- JSON report file, which contains all the extracted APK info
- `AndroidManifest.xml` file (thanks to `apktool`)
- `CERT.RSA/DSA` digital certificate file
- `classes.dex` files
- translated _.jar_ file (thanks to `dex2jar`)
- disassembled smali files (thanks to `apktool`)
- `assets/` and `res/` folders together with their content (thanks to `apktool`)



## Installation

The first step is cloning the NinjaDroid repository, or downloading its source code.

```shell
$ git clone https://github.com/rovellipaolo/NinjaDroid
$ cd NinjaDroid
```

NinjaDroid has several ways to be executed: natively in your local environment, in [Docker](https://www.docker.com/), as a [Flatpak](https://flatpak.org/) (experimental) and as a [Snap](https://snapcraft.io/) (experimental).

### Native
To execute NinjaDroid in your local machine, you need to install `Python 3.5` or higher, `Java 8` or higher and `binutils`.

Optionally, if you have the Android SDK installed locally, you can use the SDK version of `aapt` instead of the included one. In order to do so, you need to change the `aapt` location in `ninjadroid/aapt/Aapt.py` (i.e. `__AAPT_EXEC_PATH = "ninjadroid/aapt/aapt"`).

#### Linux
Just launch the following commands, which will install all the Python dependencies (making sure that `aapt`, `apktool` and `dex2jar` have executable permissions) and add a `ninjadroid` symlink to `/usr/local/bin/`.

```shell
$ make build-linux
$ make install
$ ninjadroid --help
```

#### MacOS
Just launch the following commands, which will install all the needed Python dependencies (making sure that `aapt`, `apktool` and `dex2jar` have executable permissions) and add a `ninjadroid` symlink to `/usr/local/bin/`.

```shell
$ make build-macos
$ make install
$ ninjadroid --help
```

### Docker
To execute NinjaDroid in Docker, you need `Docker` installed.
To build the Docker image, launch the following commands:
```shell
$ make build-docker
$ docker run --name ninjadroid ninjadroid:latest ninjadroid --help
```

Note that you need to bind the directory containing the target APK package to the Docker image:
```shell
$ mkdir apks
$ cp /path/to/your/package.apk apks/package.apk
$ docker run --name ninjadroid -it --rm -v $(pwd)/apks:/apks ninjadroid:latest ninjadroid /apks/package.apk -aj
```
And the same applies also to the output directory when using the `-e`/`--extract` option, to which you also need to grant permissions:
```shell
$ mkdir output
$ chmod 777
$ docker run --name ninjadroid --rm -v $(pwd)/apks:/apks -v $(pwd)/output:/output ninjadroid:latest ninjadroid /apks/package.apk -ae /output
```

### Flatpak (experimental)
To execute NinjaDroid as a Flatpak, you need `Flatpak` and `flatpak-builder` installed.
Just launch the following commands, which will install all the needed Flatpak dependencies:
```shell
$ make build-flatpak
$ flatpak-builder --run flatpak/build flatpak/com.github.rovellipaolo.NinjaDroid.yaml ninjadroid --help
```

**NOTE:** The `-e`/`--extract` option does not work correctly at present (see: https://github.com/rovellipaolo/NinjaDroid/issues/21).


### Snap (experimental)
To execute NinjaDroid as a Snap, you need `Snap` and `snapcraft` installed.
Just launch the following commands, which will install all the needed Snap dependencies:
```shell
$ make build-snap
$ make install-snap
$ ninjadroid --help
```

**NOTE:** The `-e`/`--extract` option does not work correctly when the snap is installed without using the `--devmode` option (see: https://github.com/rovellipaolo/NinjaDroid/issues/20).



## Checkstyle

Once you've configured it (see the _"Installation"_ section), you can also run NinjaDroid checkstyle as follows.

### Native
To run the checkstyle in your local machine, launch the following command:
```shell
$ make checkstyle
```
**NOTE:** This is using [`pylint`](https://github.com/PyCQA/pylint) under-the-hood.

You can also run the checkstyle automatically at every git commit by launching the following command:
```shell
$ make install-githooks
```

### Docker
To run the checkstyle in Docker, launch the following command:
```shell
$ make checkstyle-docker
```



## Tests

Once you've configured it (see the _"Installation"_ section), you can also run NinjaDroid tests as follows.

### Native
To run unit and regression tests in your local machine, launch the following commands:
```shell
$ make test
$ make regression
```

You can also run the tests with coverage by launching the following command:
```shell
$ make test-coverage
```

### Docker
To run unit and regression tests in Docker, launch the following commands:
```shell
$ make test-docker
$ make regression-docker
```

### Flatpak
To run regression tests in Flatpak, launch the following command:
```shell
$ make regression-flatpak
```

### Snap
To run regression tests in Snap, launch the following command:
```shell
$ make regression-snap
```



## Usage

The following are examples of running NinjaDroid against the sample APK package.

### Show APK summary
```shell
$ ninjadroid regression/data/Example.apk
```
```shell
file:    regression/data/Example.apk
size:    70058
md5:     c9504f487c8b51412ba4980bfe3cc15d
sha1:    482a28812495b996a92191fbb3be1376193ca59b
sha256:  8773441a656b60c5e18481fd5ba9c1bf350d98789b975987cb3b2b57ee44ee51
sha512:  559eab9840ff2f8507842605e60bb0730442ddf9ee7ca4ab4f386f715c1a4707766065d6f0b977816886692bf88b400643979e2fd13e6999358a21cabdfb3071
name:    Example
cert:
	file:   META-INF/CERT.RSA
	size:   906
	md5:    860e19fa47d37d9510f1245c511a8578
	sha1:   59a04084c0d5ef23fd05f0f429dab6267ccb3d0b
	sha256: 0efa622919417adfa6eb77770fd33d3bcd93265ac7343695e246dab1a7b6bfee
	sha512: 2a5befcc0bcb14e44d7b7cb4322a76933ad3e90e5e1ffbb87ba31ee7cc0172725dcc98e9d414fb3a207bc107b2a7ca7563b5f954cac6bd41d77e4726c70a95a3
manifest:
	file:   AndroidManifest.xml
	size:   6544
	md5:    1f97f7e7ca62f39f8f81d79b1b540c37
	sha1:   011316a011e5b8738c12c662cb0b0a6ffe04ca74
	sha256: 7c8011a46191ecb368bf2e0104049abeb98bae8a7b1fa3328ff050aed85b1347
	sha512: 8c7c1ede610f9c6613418b46a52a196ad6d5e8cc067c2f26b931738ad8087f998d9ea95e80ec4352c95fbdbb93a4f29c646973535068a3a3d584da95480ab45f
	package: com.example.app
	version:
		code:  1
		name:  1.0
	sdk:
		min:   10
		target: 20
		max:   20
	permissions:
		- android.permission.INTERNET
		- android.permission.READ_EXTERNAL_STORAGE
		- android.permission.RECEIVE_BOOT_COMPLETED
		- android.permission.WRITE_EXTERNAL_STORAGE
dex:
	file:   classes.dex
	size:   2132
	md5:    7bc52ece5249ccd2d72c4360f9be2ca5
	sha1:   89476799bf92798047ca026c922a5bc33983b008
	sha256: 3f543c68c4c059548cec619a68f329010d797e5e4c00aa46cd34c0d19cabe056
	sha512: 0725f961bc1bac47eb8dd045c2f0a0cf5475fd77089af7ddc3098e341a95d8b5624969b6fa47606a05d5a6adf9d74d0c52562ea41a376bd3d7d0aa3695ca2e22
```

### Show APK extended information in JSON format
```shell
$ ninjadroid regression/data/Example.apk --all --json
```
```json
{
    "cert": {
        "file": "META-INF/CERT.RSA",
        "fingerprint": {
            "md5": "",
            "sha1": "5A:C0:6C:32:63:7F:5D:BE:CA:F9:38:38:4C:FA:FF:ED:20:52:43:B6",
            "sha256": "E5:15:CC:BC:5E:BF:B2:9D:A6:13:03:63:CF:19:33:FA:CE:AF:DC:ED:5D:2F:F5:98:7C:CE:37:13:64:4A:CF:77",
            "signature": "SHA1withRSA",
            "version": "3"
        },
        "issuer": {
            "city": "City",
            "country": "XX",
            "domain": "",
            "email": "",
            "name": "Name",
            "organization": "Organization",
            "state": "State",
            "unit": "Unit"
        },
        "md5": "860e19fa47d37d9510f1245c511a8578",
        "owner": {
            "city": "City",
            "country": "XX",
            "domain": "",
            "email": "",
            "name": "Name",
            "organization": "Organization",
            "state": "State",
            "unit": "Unit"
        },
        "serial_number": "558e7595",
        "sha1": "59a04084c0d5ef23fd05f0f429dab6267ccb3d0b",
        "sha256": "0efa622919417adfa6eb77770fd33d3bcd93265ac7343695e246dab1a7b6bfee",
        "sha512": "2a5befcc0bcb14e44d7b7cb4322a76933ad3e90e5e1ffbb87ba31ee7cc0172725dcc98e9d414fb3a207bc107b2a7ca7563b5f954cac6bd41d77e4726c70a95a3",
        "size": 906,
        "validity": {
            "from": "2015-06-27 10:06:13Z",
            "until": "2515-02-26 10:06:13Z"
        }
    },
    "dex": [
        {
            "file": "classes.dex",
            "md5": "7bc52ece5249ccd2d72c4360f9be2ca5",
            "sha1": "89476799bf92798047ca026c922a5bc33983b008",
            "sha256": "3f543c68c4c059548cec619a68f329010d797e5e4c00aa46cd34c0d19cabe056",
            "sha512": "0725f961bc1bac47eb8dd045c2f0a0cf5475fd77089af7ddc3098e341a95d8b5624969b6fa47606a05d5a6adf9d74d0c52562ea41a376bd3d7d0aa3695ca2e22",
            "shell_commands": [
                "set"
            ],
            "size": 2132,
            "strings": [
                "!Lcom/example/app/ExampleService2;",
                "!Lcom/example/app/ExampleService3;",
                "#Landroid/content/BroadcastReceiver;",
                ")Lcom/example/app/ExampleBrodcastReceiver;",
                "*Lcom/example/app/ExampleBrodcastReceiver2;",
                "*Lcom/example/app/ExampleBrodcastReceiver3;",
                "*Lcom/example/app/ExampleBrodcastReceiver4;",
                "<init>",
                "Landroid/app/Activity;",
                "Landroid/app/Service;",
                "Landroid/content/Context;",
                "Landroid/content/Intent;",
                "Landroid/os/Bundle;",
                "Landroid/os/IBinder;",
                "Lcom/example/app/ExampleService;",
                "Lcom/example/app/HomeActivity;",
                "Lcom/example/app/OtherActivity;",
                "onBind",
                "onCreate",
                "onReceive",
                "setContentView"
            ],
            "urls": []
        }
    ],
    "file": "regression/data/Example.apk",
    "manifest": {
        "activities": [
            {
                "intent-filter": [
                    {
                        "action": [
                            "android.intent.action.MAIN"
                        ],
                        "category": [
                            "android.intent.category.LAUNCHER"
                        ]
                    }
                ],
                "launchMode": "1",
                "name": "com.example.app.HomeActivity"
            },
            {
                "intent-filter": [
                    {
                        "action": [
                            "android.intent.action.VIEW"
                        ],
                        "category": [
                            "android.intent.category.DEFAULT"
                        ],
                        "data": [
                            {
                                "scheme": "content"
                            },
                            {
                                "scheme": "file"
                            },
                            {
                                "mimeType": "application/vnd.android.package-archive"
                            }
                        ]
                    }
                ],
                "launchMode": "1",
                "meta-data": [
                    {
                        "name": "android.support.PARENT_ACTIVITY",
                        "value": "com.example.app.HomeActivity"
                    }
                ],
                "name": "com.example.app.OtherActivity",
                "noHistory": "true",
                "parentActivityName": "com.example.app.HomeActivity"
            }
        ],
        "file": "AndroidManifest.xml",
        "md5": "1f97f7e7ca62f39f8f81d79b1b540c37",
        "package": "com.example.app",
        "permissions": [
            "android.permission.INTERNET",
            "android.permission.READ_EXTERNAL_STORAGE",
            "android.permission.RECEIVE_BOOT_COMPLETED",
            "android.permission.WRITE_EXTERNAL_STORAGE"
        ],
        "receivers": [
            {
                "name": "com.example.app.ExampleBrodcastReceiver"
            },
            {
                "exported": false,
                "intent-filter": [
                    {
                        "action": [
                            "android.intent.action.BOOT_COMPLETED",
                            "android.intent.action.MY_PACKAGE_REPLACED"
                        ],
                        "priority": "1000"
                    }
                ],
                "name": "com.example.app.ExampleBrodcastReceiver2"
            },
            {
                "enabled": true,
                "exported": false,
                "intent-filter": [
                    {
                        "action": [
                            "android.intent.action.BROADCAST_PACKAGE_REMOVED",
                            "android.intent.action.PACKAGE_ADDED",
                            "android.intent.action.PACKAGE_REPLACED"
                        ],
                        "data": [
                            {
                                "scheme": "package"
                            }
                        ],
                        "priority": "800"
                    }
                ],
                "name": "com.example.app.ExampleBrodcastReceiver3"
            },
            {
                "enabled": false,
                "exported": true,
                "name": "com.example.app.ExampleBrodcastReceiver4"
            }
        ],
        "sdk": {
            "max": "20",
            "min": "10",
            "target": "20"
        },
        "services": [
            {
                "name": "com.example.app.ExampleService"
            },
            {
                "enabled": false,
                "exported": true,
                "isolatedProcess": true,
                "name": "com.example.app.ExampleService2"
            },
            {
                "enabled": true,
                "exported": false,
                "isolatedProcess": false,
                "name": "com.example.app.ExampleService3"
            }
        ],
        "sha1": "011316a011e5b8738c12c662cb0b0a6ffe04ca74",
        "sha256": "7c8011a46191ecb368bf2e0104049abeb98bae8a7b1fa3328ff050aed85b1347",
        "sha512": "8c7c1ede610f9c6613418b46a52a196ad6d5e8cc067c2f26b931738ad8087f998d9ea95e80ec4352c95fbdbb93a4f29c646973535068a3a3d584da95480ab45f",
        "size": 6544,
        "version": {
            "code": 1,
            "name": "1.0"
        }
    },
    "md5": "c9504f487c8b51412ba4980bfe3cc15d",
    "name": "Example",
    "other": [
        {
            "file": "res/drawable-hdpi-v4/ic_launcher.png",
            "md5": "e74dbf28ebab4e1b7442a9c78067d1c2",
            "sha1": "450d3d44325fdf259810a60e6afa36103e186b3d",
            "sha256": "9b2639dbfdd60e0dab70e572f39660c8dfabd19b7987a7619d770824db342925",
            "sha512": "44050c4db6d5275b70856050c0d58d3d9892ba09bd8cf1a8343a3c6d4f2e2af6eae1f8b687efb59b7f8122e5bea1a63e08546fee35124cc0faab40ef6274ab4f",
            "size": 9193
        },
        {
            "file": "res/drawable-hdpi-v4/ic_launcher_logo.png",
            "md5": "e74dbf28ebab4e1b7442a9c78067d1c2",
            "sha1": "450d3d44325fdf259810a60e6afa36103e186b3d",
            "sha256": "9b2639dbfdd60e0dab70e572f39660c8dfabd19b7987a7619d770824db342925",
            "sha512": "44050c4db6d5275b70856050c0d58d3d9892ba09bd8cf1a8343a3c6d4f2e2af6eae1f8b687efb59b7f8122e5bea1a63e08546fee35124cc0faab40ef6274ab4f",
            "size": 9193
        },
        {
            "file": "res/drawable-ldpi-v4/ic_launcher.png",
            "md5": "58b9a42eeb99fad5321208fe02f24375",
            "sha1": "09ea65885b4080e515ef7064e816c77991c0757b",
            "sha256": "c4f061b2c758185371f39afcb166ba039e955d3be2619ab5469a1b873f952d0d",
            "sha512": "415ed16de6fd335b24bd985d9152323d04fc02287acd3f26fa98722832cfecf89cf2c77ad8ae3f5588acc5cac401129ac3b3d714abbf8dcc492ab2fd98f106e5",
            "size": 2658
        },
        {
            "file": "res/drawable-ldpi-v4/ic_launcher_logo.png",
            "md5": "58b9a42eeb99fad5321208fe02f24375",
            "sha1": "09ea65885b4080e515ef7064e816c77991c0757b",
            "sha256": "c4f061b2c758185371f39afcb166ba039e955d3be2619ab5469a1b873f952d0d",
            "sha512": "415ed16de6fd335b24bd985d9152323d04fc02287acd3f26fa98722832cfecf89cf2c77ad8ae3f5588acc5cac401129ac3b3d714abbf8dcc492ab2fd98f106e5",
            "size": 2658
        },
        {
            "file": "res/drawable-mdpi-v4/ic_launcher.png",
            "md5": "acefc1f320111a8d71bcdb8b4aa0656c",
            "sha1": "23730fd0d5e720d1f719be1afc8c48fa7305da6c",
            "sha256": "05346d62d4096537906928af523ef9d5997663707a1d48e08f20992584e1424d",
            "sha512": "59896fc52679e86898dc09b56fb53270d4297c53adee26f864657c5ef4aff9e5f5922dfa9370c3d1748068aa7b1270e0fa8a1323ce3b69c7548a50ca221befc1",
            "size": 5057
        },
        {
            "file": "res/drawable-mdpi-v4/ic_launcher_logo.png",
            "md5": "acefc1f320111a8d71bcdb8b4aa0656c",
            "sha1": "23730fd0d5e720d1f719be1afc8c48fa7305da6c",
            "sha256": "05346d62d4096537906928af523ef9d5997663707a1d48e08f20992584e1424d",
            "sha512": "59896fc52679e86898dc09b56fb53270d4297c53adee26f864657c5ef4aff9e5f5922dfa9370c3d1748068aa7b1270e0fa8a1323ce3b69c7548a50ca221befc1",
            "size": 5057
        },
        {
            "file": "res/drawable-xhdpi-v4/ic_launcher.png",
            "md5": "94f5591633218c0b469b65947fd8943b",
            "sha1": "502cd84fa444f26d7ecfdf4a355064867977f236",
            "sha256": "29d15992424b40757135f47fc8ddd15e30c7774646b37755608f7cfec1df7d8a",
            "sha512": "d5b48e065a614c5a2400b6565dc36777d9923d8d5154487113dd1f46b05d36d1db3f28fb72f61a68fcbd225c93495541579574e6611f650fe2857767412c3b1f",
            "size": 14068
        },
        {
            "file": "res/drawable-xhdpi-v4/ic_launcher_logo.png",
            "md5": "94f5591633218c0b469b65947fd8943b",
            "sha1": "502cd84fa444f26d7ecfdf4a355064867977f236",
            "sha256": "29d15992424b40757135f47fc8ddd15e30c7774646b37755608f7cfec1df7d8a",
            "sha512": "d5b48e065a614c5a2400b6565dc36777d9923d8d5154487113dd1f46b05d36d1db3f28fb72f61a68fcbd225c93495541579574e6611f650fe2857767412c3b1f",
            "size": 14068
        },
        {
            "file": "res/layout/main.xml",
            "md5": "8cdec0105448937475e45e22c80fd611",
            "sha1": "51ebf14ed21238f7d147a6744cae18c0f55fcbe6",
            "sha256": "e74db1ac37395ca9fd25b93261d3ab76ed7dfc9b355ea63d856afc7453313738",
            "sha512": "2d2147365b8b00f2db7498b7f0ed8a360fc15bd43dfd3704b4b1cb912619d9ff1bc35837eb1e601ea6d1aa3a8c0d555f2105d6ed37de919fa128568527765d63",
            "size": 552
        },
        {
            "file": "resources.arsc",
            "md5": "2886f2825eef3b5c4478852935c68640",
            "sha1": "1eff126288b4bea6fa78eb79832d6a7fa098695e",
            "sha256": "ac46f54fa12dc20e94619465482186047505fb9f27508861220063c93f0c6c4e",
            "sha512": "da8c41d0c27839ed89cb06a2f89f6993bd88f5179e97f3291f0e17348868b3e9c106e96f482ecd86f11808170937773e7599ccd338900908359e870ea5446169",
            "size": 1640
        },
        {
            "file": "META-INF/MANIFEST.MF",
            "md5": "6098a6409625f1c0d97cd33c13ad300c",
            "sha1": "ccfe31190feb259a4a56599ad1403a956f6944b5",
            "sha256": "8a18f285481346919f4df55f576ee504bf5abecb068a2d642fdef17f3b5cd631",
            "sha512": "17a68bf605aff149aa31e1b0b81af3d3f74f939e1cb7a10f3eddf84775f901b09ba9722efad1265b0057cdfcd12c6fac701067993081620b00bbfcc4efff3599",
            "size": 1061
        },
        {
            "file": "META-INF/CERT.SF",
            "md5": "fb02917b68510e413a06e52873802bcd",
            "sha1": "dfb7bbb487010b980152610fe7d669c1b4f626be",
            "sha256": "e2fa373f8b065ef7c78387ab9242e98dd19bdeb2b768295506295f7beb0bfe3f",
            "sha512": "3aa74603588ca5c563b6586d1216dc6cea3b8d2a1a47eb189197e8f20cd7508d3e652c7ff849261e95cff52451476b2993caadf051fdf66cc01f5e6e16b180fc",
            "size": 1114
        }
    ],
    "sha1": "482a28812495b996a92191fbb3be1376193ca59b",
    "sha256": "8773441a656b60c5e18481fd5ba9c1bf350d98789b975987cb3b2b57ee44ee51",
    "sha512": "559eab9840ff2f8507842605e60bb0730442ddf9ee7ca4ab4f386f715c1a4707766065d6f0b977816886692bf88b400643979e2fd13e6999358a21cabdfb3071",
    "size": 70058
}
```

### Extract and store APK entries and information
```shell
$ ninjadroid regression/data/Example.apk --all --extract output/
```
```shell
  >> NinjaDroid: [INFO] Executing apktool...
  >> NinjaDroid: [INFO] Creating output/smali/...
  >> NinjaDroid: [INFO] Creating output/AndroidManifest.xml...
  >> NinjaDroid: [INFO] Creating output/res/...
  >> NinjaDroid: [INFO] Creating output/assets/...
  >> NinjaDroid: [INFO] Executing dex2jar...
  >> NinjaDroid: [INFO] Creating output/Example.jar...
dex2jar regression/data/Example.apk -> output/Example.jar
  >> NinjaDroid: [INFO] Extracting certificate file...
  >> NinjaDroid: [INFO] Creating output/META-INF/CERT.RSA...
  >> NinjaDroid: [INFO] Extracting DEX files...
  >> NinjaDroid: [INFO] Creating output/classes.dex...
  >> NinjaDroid: [INFO] Generating JSON report file...
  >> NinjaDroid: [INFO] Creating output/report-Example.json...
```
**NOTE:** without specifying an output directory, one with the APK package name will be created inside the current working directory.



## Licence

NinjaDroid is licensed under the GNU General Public License v3.0 (http://www.gnu.org/licenses/gpl-3.0.html).
