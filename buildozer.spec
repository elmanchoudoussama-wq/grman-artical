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

# Application requirements
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,arabic_reshaper,python-bidi,kivmob,android

# (str) Presplash of the application
presplash.filename = %(source.dir)s/presplash.png

# Icon of the application
icon.filename = %(source.dir)s/icon.png

# Supported orientation
orientation = portrait

# Fullscreen
fullscreen = 0

# OSX settings
osx.python_version = 3
osx.kivy_version = 2.3.0

#
# Android specific
#

# Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Android NDK version
android.ndk = 25b

# Accept SDK licenses automatically
android.accept_sdk_license = True

# Gradle dependencies (AdMob)
android.gradle_dependencies = com.google.android.gms:play-services-ads:20.6.0

# Build tools version
android.build_tools_version = 33.0.0

# Enable AndroidX
android.enable_androidx = True

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

#
# iOS specific
#

ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

ios.codesign.allowed = false


[buildozer]

# Log level
log_level = 2

# Warn if run as root
warn_on_root = 1
