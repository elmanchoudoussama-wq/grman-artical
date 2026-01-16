[app]

# Title of your application
title = German Artical Trainer

# Package name
package.name = articaltrainer

# Package domain
package.domain = org.artical

# Source code directory
source.dir = .

# Source files to include
source.include_exts = py,png,jpg,kv,json,ttf

# Application version
version = 0.1

# --- FIXED REQUIREMENTS ---
# Added pillow, arabic_reshaper, and python-bidi
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,arabic_reshaper,python-bidi,kivmob,android

# --- CRITICAL FIX FOR ARABIC ---
# This line tells Android to include the engines that connect Arabic letters
android.dependencies = libharfbuzz, libfribidi

# (str) Presplash of the application
presplash.filename = %(source.dir)s/data/presplash.png

# Icon of the application
icon.filename = %(source.dir)s/data/icon.png

# Supported orientation
orientation = portrait

# Fullscreen
fullscreen = 0

#
# Android specific
#

# Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Android API and NDK
android.api = 33
android.ndk = 25b
android.accept_sdk_license = True

# Gradle dependencies (AdMob)
android.gradle_dependencies = com.google.android.gms:play-services-ads:20.6.0

# Build tools version
android.build_tools_version = 33.0.0

# Enable AndroidX
android.enable_androidx = True

# --- ASSETS PATH ---
# This ensures your Amiri-Regular.ttf font is actually included
android.add_assets = assets

# Gradle repositories
android.gradle_repositories = google(),mavenCentral()

# AdMob App ID (REQUIRED)
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-9298331856947532~1106493604

# Architectures
android.archs = arm64-v8a

# Allow backup
android.allow_backup = True

# Debug artifact format
android.debug_artifact = apk

[buildozer]
# Log level (2 for full debug info)
log_level = 2
warn_on_root = 1
