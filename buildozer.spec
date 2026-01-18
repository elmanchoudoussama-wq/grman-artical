[app]

# (str) Title of your application
title = German Artical Trainer

# (str) Package name
package.name = articaltrainer

# (str) Package domain (needed for android packaging)
package.domain = org.artical

# (str) Source code directory
source.dir = .

# (list) Source files to include (let's include py, kv, json, ttf, and png)
source.include_exts = py,png,jpg,kv,json,ttf

# (str) Application version
version = 0.1

# --- CRITICAL REQUIREMENTS ---
# Added 'pillow' for image rendering and 'arabic_reshaper/python-bidi' for logic
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, arabic_reshaper, python-bidi, kivmob, android

# (str) Presplash of the application
presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

#
# Android specific
#

# (list) Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API
android.api = 33
android.build_tools_version = 33.0.0

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage
android.private_storage = True

# --- ASSETS FOLDER ---
# This ensures your 'assets' folder (containing fonts) is included in the APK
android.add_assets = assets

# (list) Android additionnal libraries to copy into libs/armeabi
# Including harfbuzz and fribidi as a safety net for the system engine
android.dependencies = libharfbuzz, libfribidi

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (str) The Android arch to build for
android.archs = arm64-v8a

# (bool) indicates whether the screen should stay on
# android.wakelock = False

# --- ADMOB CONFIGURATION ---
# Your specific AdMob App ID
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-9298331856947532~1106493604

# (list) Android application meta-data
android.gradle_dependencies = com.google.android.gms:play-services-ads:20.6.0

# (bool) Enable AndroidX support
android.enable_androidx = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = no, 1 = yes)
warn_on_root = 1
