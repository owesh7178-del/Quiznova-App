[app]

# (str) Title of your application
title = Quiznova

# (str) Package name
package.name = quiznova

# (str) Package domain (needed for android packaging)
package.domain = com.quiznova.app

# (str) Source code directory where main.py is located
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Supported orientations (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) Permissions required by the app
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (str) Application version
version = 1.0

# Requirements
requirements = python3==3.11.1, kivy==2.3.0, kivmob, pyjnius, jnius

# (str) Supported platforms
target = android

# ----------------------------------
# Android specific configurations
# ----------------------------------

# 🔒 [THE MULTI-ARCH FIX] बिल्ड को सिर्फ 64-bit (arm64-v8a) पर लॉक करना ताकि Compilations टकराएं न!
android.archs = arm64-v8a

# गिटहब रनर का SDK पाथ
android.sdk_path = /usr/local/lib/android/sdk

# NDK Settings
android.ndk = 25c
android.ndk_api = 21
android.api = 33
android.minapi = 21

# (list) Gradle dependencies
android.gradle_dependencies = 'com.google.android.gms:play-services-ads:22.6.0'

# (list) Packaging options for gradle
android.add_compile_options = "sourceCompatibility = JavaVersion.VERSION_1_8", "targetCompatibility = JavaVersion.VERSION_1_8"

# (list) Android manifest extra elements
android.manifest_metadata = meta-data:com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

# ----------------------------------
# Buildozer settings
# ----------------------------------

[buildozer]

log_level = 2
warn_on_root = 1
