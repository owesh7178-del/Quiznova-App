[app]

# (string) Title of your application
title = Quiznova

# (string) Package name
package.name = quiznova

# (string) Package domain (needed for android packaging)
package.domain = org.quiznova

# (string) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) Application requirements
# 💰 बदलाव: यहाँ kivmob और urllib3 जोड़ दिया गया है
requirements = python3, kivy, urllib3, kivmob

# (str) Custom source folders for requirements
# (list) Permissions
# 💰 बदलाव: विज्ञापनों के लिए इंटरनेट और नेटवर्क स्टेट की परमिशन ऑन कर दी है
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data directory for storage (true) or public (--dir)
android.private_storage = True

# (list) Android application meta-data
# 💰 बदलाव: यहाँ AdMob की टेस्ट App ID सेट कर दी है (प्ले स्टोर पर जाते समय इसे बदलेंगे)
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

# (list) Android gradle dependencies
# 💰 बदलाव: गूगल विज्ञापन लोड करने के लिए प्ले-सर्विसेस डिपेंडेंसी जोड़ी गई है
android.gradle_dependencies = 'com.google.android.gms:play-services-ads:22.6.0'

# (list) The Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Allow service to be foreground
android.foreground_service = False

# (str) The format used to package the app for release mode (apk or aab)
# नोट: अभी टेस्टिंग के लिए 'apk' रखा है, प्ले स्टोर पर डालते समय इसे 'aab' कर देंगे
target = apk

# (str) Build profile (debug or release)
build_profile = debug

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level
