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

# (list) Permissions required by the app (Internet & Network state are must for Ads)
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (str) Application version
version = 1.0

# 🔒 [THE PYTHON COMPILING FIX] पाइथन वर्जन को एंड्रॉइड के लिए 3.11 पर लॉक करना
requirements = python3==3.11.1, kivy==2.3.0, kivmob, pyjnius, jnius

# (str) Supported platforms
target = android

# ----------------------------------
# Android specific configurations
# ----------------------------------

# गिटहब रनर का ऑफिशियल SDK पाथ
android.sdk_path = /usr/local/lib/android/sdk

# गिटहब रनर का ऑफिशियल NDK पाथ
android.ndk_path = /usr/local/lib/android/sdk/ndk/27.3.13750724

# (int) Android API to use (Target SDK)
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (list) Gradle dependencies (Google Play Services for Ads/Kivmob)
android.gradle_dependencies = 'com.google.android.gms:play-services-ads:22.6.0'

# (list) Packaging options for gradle
android.add_compile_options = "sourceCompatibility = JavaVersion.VERSION_1_8", "targetCompatibility = JavaVersion.VERSION_1_8"

# (list) Android manifest extra elements (AdMob App ID Configuration)
android.manifest_metadata = meta-data:com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

# ----------------------------------
# Buildozer settings
# ----------------------------------

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
