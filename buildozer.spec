[app]
title = German Article Trainer
package.name = articletrainer
package.domain = org.article
source.dir = .
source.include_exts = py,png,jpg,kv,json,ttf,otf
version = 0.1

# REQUIREMENTS: Added Pillow, Arabic Reshaper, and Python-Bidi
requirements = python3, kivy==2.3.0, kivymd==1.2.0, pillow, arabic_reshaper, python-bidi, android

orientation = portrait
android.permissions = INTERNET, ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 23
android.accept_sdk_license = True

# ARCHITECTURE: Fixed to modern 64-bit
android.archs = arm64-v8a

# ASSETS: Ensure your fonts folder is included
android.add_assets = assets

[buildozer]
log_level = 2
warn_on_root = 1
