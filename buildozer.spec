[app]

# (str) Title of your application
title = German Article Trainer

# (str) Package name (use lowercase, no spaces)
package.name = articletrainer

# (str) Package domain (needed for android packaging)
package.domain = org.article

# (str) Source code directory
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,json,ttf,otf

# (str) Application version
version = 0.1

# (str) Source code where the main.py is
source.main = main.py

# --- REQUIREMENTS ---
# KivyMD 1.2.0 requires Kivy 2.1.0, not 2.3.0
requirements = python3,kivy==2.1.0,kivymd==1.2.0,pillow,arabic_reshaper,python-bidi,kivmob,android

# (str) Presplash of the application
presplash.filename = data/presplash.png

# (str) Icon of the application
icon.filename = data/icon.png

# (str) Supported orientation
orientation = portrait

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy

# (bool) Fullscreen (no status bar)
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 23

# (str) Android NDK version to use
# Recommended: 23b or 25b (23b is more stable)
android.ndk = 23b

# (bool) Use private storage
android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
# android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
# android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
# android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
# android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first running
# buildozer.
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
# android.entrypoint = org.kivy.android.PythonActivity

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# OUYA-ODK/libs/*.jar
# android.add_jars = foo.jar,bar.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
# android.add_src =

# (list) Android AAR archives to add (currently works only with sdl2_gradle
# bootstrap)
# android.add_aars =

# (list) Gradle dependencies to add
android.gradle_dependencies = 'com.google.android.gms:play-services-ads:22.6.0'

# (list) add java compile options
# this can for example be necessary when importing certain java libraries using the 'android.gradle_dependencies' option
# see https://developer.android.com/studio/write/java8-support for further information
# android.add_compile_options =

# (list) Gradle repositories to add {can be necessary for some android.gradle_dependencies}
# please enclose in double quotes 
# e.g. android.gradle_repositories = "maven { url 'https://kotlin.bintray.com/ktor' }"
#android.gradle_repositories =

# (list) packaging options to add 
# see https://google.github.io/android-gradle-dsl/current/com.android.build.gradle.internal.dsl.PackagingOptions.html
# can be necessary to solve conflicts in gradle_dependencies
# please enclose in double quotes 
# e.g. android.packaging_options = "exclude 'META-INF/common.kotlin_module'", "exclude 'META-INF/*.kotlin_module'"
#android.packaging_options =

# (list) Java classes to add as activities to the manifest.
#android.add_activites = com.example.ExampleActivity

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
#android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
#android.manifest.intent_filters =

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (list) Android additionnal libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_arm64_v8a = libs/android-v8/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# (bool) Indicate whether the screen should stay on
# android.wakelock = False

# (list) Android application meta-data to set (key=value format)
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-9298331856947532~1106493604

# (list) Android library project to add (will be added in the
# project.properties automatically.)
#android.library_references =

# (list) Android shared libraries which will be added to AndroidManifest.xml using <uses-library> tag
#android.uses_library =

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
# android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = arm64-v8a

# (int) overrides automatic versionCode computation (used in build.gradle)
# this is not the same as app version and should only be edited if you know what you're doing
# android.numeric_version = 1

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML file for additional configuration options for the backup (Android API >=23)
# android.backup_rules =

# (bool) If set to True, the --use-libraries flag will be passed to the RST document to
# allow it to use support libraries (Android API >=23)
# android.use_libraries = False

# (str) The format used to create the version code
# You can use the following substitutions:
# %(versionMajor)d - the major version as integer
# %(versionMinor)d - the minor version as integer
# %(versionPatch)d - the patch version as integer
# The default value is: %(versionMajor)02d%(versionMinor)02d%(versionPatch)02d
# android.version_code_format = %(versionMajor)02d%(versionMinor)02d%(versionPatch)02d

#
#    Python for android (p4a) specific
#

# (str) python-for-android URL to use for checkout
#p4a.url =

# (str) python-for-android fork to use in case if p4a.url is not specified, defaults to upstream (kivy)
#p4a.fork = kivy

# (str) python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
#p4a.source_dir =

# (str) The directory where the python-for-android library should be built
#p4a.build_dir = .p4a-build

# (str) The directory where the python-for-android library should install the distribution
#p4a.dist_dir = %(source.dir)s/dist

# (list) The distribution to use, you can also use "master"
p4a.branch = master

# (str) The bootstrap to use (sdl2, webview, service_only)
p4a.bootstrap = sdl2

# (int) port where to start the Gunicorn server
#p4a.gunicorn.port = 5000

#
# iOS specific
#

# (str) Path to a custom xcodebuild command to use
#ios.xcodebuild =

# (str) Path to a custom xcodebuild command to use
#ios.codesign.allowed_identities =

# (list) List of toolchain to use
#ios.toolchain = 

# (str) The bundle identifier of the application (used in codesign and profile)
#ios.bundle_identifier =

# (str) The app category to use (used in codesign and profile)
#ios.app_category =

# (int) the minimum version of iOS where the app will be able to run
#ios.deployment_target = 9.0

# (bool) whether to use the Swift runtime when building
#ios.use_swift_runtime = False

# (str) Xcode version to use
#ios.xcode_version = 

#
# Buildozer specific
#

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = false, 1 = true)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# buildozer.build_dir = .buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
# buildozer.bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    List as sections
#
#    You can define all the "list" as [section:key].
#    Each line will be considered as a option to the list.
#    Let's take [app] / source.exclude_patterns.
#    Instead of doing:
#
#[app]
#source.exclude_patterns = license,data/audio/*.wav,data/images/original/*
#
#    This can be translated into:
#
#[app:source.exclude_patterns]
#license
#data/audio/*.wav
#data/images/original/*
#

#    -----------------------------------------------------------------------------
#    Profiles
#
#    You can extend section / key with a profile
#    For example, you want to deploy a demo version of your application without
#    HD content. You could first change the title to add "(demo)" in the name
#    and extend the excluded directories to remove the HD content.
#
#[app@demo]
#title = My Application (demo)
#
#[app:source.exclude_patterns@demo]
#images/hd/*
#
#    Then, invoke the command line with the "demo" profile:
#
#buildozer --profile demo android debug