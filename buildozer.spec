[app]

# Application information
title = German Article Trainer
package.name = articletrainer
package.domain = org.article
source.dir = .
source.main = main.py  # <-- THIS IS CRITICAL!

# Files to include
source.include_exts = py,png,jpg,kv,json,ttf,otf
version = 0.1

# Requirements - FIXED VERSIONS
requirements = python3,kivy==2.1.0,kivymd==1.2.0,pillow,arabic_reshaper,python-bidi,kivmob,android

# Graphics
presplash.filename = data/presplash.png
icon.filename = data/icon.png
orientation = portrait

# Android configuration
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 23
android.accept_sdk_license = True

# Architecture
android.arch = arm64-v8a

# AdMob
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-9298331856947532~1106493604
android.gradle_dependencies = com.google.android.gms:play-services-ads:22.6.0

# Assets
android.add_assets = assets

[buildozer]
log_level = 2
warn_on_root = 1