[app]

# (str) Title of your application
title = German Article Trainer

# (str) Package name
package.name = articletrainer

# (str) Package domain (needed for android packaging)
package.domain = org.article

# (str) Source code directory
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,json,ttf,otf

# (str) Application version
version = 0.1

# --- REQUIREMENTS ---
# Updated Kivy to 2.3.0 for better API 33 support
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, arabic_reshaper, python-bidi, kivmob, android

# (str) Presplash of the application
presplash.filename = data/presplash.png

# (str) Icon of the application
icon.filename = data/icon.png

# (str) Supported orientation
orientation = portrait

# --- ANDROID SPECIFIC ---
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Accept SDK license without operator interaction
android.accept_sdk_license = True

# --- ARCHITECTURE ---
# Fixed key name: 'android.archs' instead of 'android.arch'
android.archs = arm64-v8a

# --- ADMOB CONFIGURATION ---
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-9298331856947532~1106493604
android.gradle_dependencies = com.google.android.gms:play-services-ads:22.6.0

# --- ASSETS ---
# This ensures your fonts in 'assets/' are bundled
android.add_assets = assets

[buildozer]
log_level = 2
warn_on_root = 1
