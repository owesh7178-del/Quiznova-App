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

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.png

# (html) Icon of the application
#icon.filename = %(source.dir)s/logo.png

# (str) Supported orientations (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) Permissions required by the app (Internet is must for Ads)
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (str) Application version
version = 1.0

# (list) Application requirements
# हमने यहाँ kivmob, pyjnius, और jnius को शामिल किया है जो विज्ञापन चलाने के लिए ज़रूरी हैं
requirements = python3, kivy==2.3.0, kivmob, pyjnius, jnius

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/logo.png

# (str) Supported platforms
target = android

# ----------------------------------
# Android specific configurations
# ----------------------------------

# (int) Android API to use (33 or 34 is highly recommended)
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
#android.ndk = 25b

# (bool) Use --private data directory (True is recommended)
android.private_storage = True

# (list) Gradle dependencies (Google Play Services for Ads)
# यह लाइन AdMob के असली विज्ञापन लोड करने के लिए सबसे ज़रूरी है
android.gradle_dependencies = 'com.google.android.gms:play-services-ads:22.6.0'

# (list) Packaging options for gradle
android.add_compile_options = "sourceCompatibility = JavaVersion.VERSION_1_8", "targetCompatibility = JavaVersion.VERSION_1_8"

# (list) Android building arguments
# android.extra_build_args = 

# (list) Android manifest extra elements (AdMob App ID configuration)
# ⚠️ नीचे "value" में अपनी असली AdMob App ID डालें। अभी यहाँ Google की टेस्ट App ID डली है।
android.manifest_metadata = meta-data:com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

# ----------------------------------
# Buildozer settings
# ----------------------------------

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
