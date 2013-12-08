#!/bin/sh

#
# ninjadroid - Tools to play with Android APK packages.
# Copyright (c) 2013 Paolo Rovelli
# 
# Licensed under the GPLv3 License.
#

#Launch dex2jar in order to generate a jar file from the classes.dex (e.g. DroidRoot.A.apk -> DroidRoot.A-dex2jar.jar):
./ninjadroid-libs/dex2jar-0.0.9.13/d2j-dex2jar.sh --force $1
#jar xf $1_dex2jar.jar

#Launch apktool in order to extract the decrypted AndroidManifest.xml, the resources and to generate the smali code (e.g. DroidRoot.A.apk -> DroidRoot.A/):
java -jar ninjadroid-libs/apktool1.5.2/apktool.jar d -f $1
