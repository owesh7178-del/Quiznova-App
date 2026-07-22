[app]

# (str) Title of your application
title = Quiznova

# (str) Package name
package.name = quiznova

# (str) Package domain
package.domain = com.quiznova.app

# (str) Source code directory
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Supported orientations
orientation = portrait

# (list) Permissions required by the app
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (str) Application version
version = 1.0

# 🔒 Requirements
requirements = python3, kivy==2.3.0

# (str) Supported platforms
target = android

# ----------------------------------
# Android specific configurations
# ----------------------------------

# 🔒 Single Architecture
android.archs = arm64-v8a

# NDK & API Settings
android.sdk_path = /usr/local/lib/android/sdk
android.ndk = 25c
android.ndk_api = 21
android.api = 33
android.minapi = 21

# 🛑 [THE CRITICAL FIX] p4a को ज़बरदस्ती Python 3.11 यूज़ करने पर मजबूर करना
p4a.extra_args = --python-version=3.11.9

# Gradle & Ads Setup
android.gradle_dependencies = 'com.google.android.gms:play-services-ads:22.6.0'
android.add_compile_options = "sourceCompatibility = JavaVersion.VERSION_1_8", "targetCompatibility = JavaVersion.VERSION_1_8"
android.manifest_metadata = meta-data:com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

# ----------------------------------
# Buildozer settings
# ----------------------------------

[buildozer]

log_level = 2
warn_on_root = 1
