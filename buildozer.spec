[app]

# (string) Title of your application
title = Quiznova

# (string) Package name
package.name = quiznova

# (string) Package domain (needed for android packaging)
package.domain = org.owesh

# (string) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,json

# (string) Version of your application (यह एरर फिक्स कर देगा!)
version = 0.1

# (list) Application requirements
# KivMob और विज्ञापनों के लिए ज़रूरी लायब्रेरीज़ जोड़ी गई हैं
requirements = python3, kivy, urllib3, kivmob

# (str) Supported orientations (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# =============================================================================
# Android specific configuration
# =============================================================================

# (list) Android permissions (इंटरनेट और नेटवर्क स्टेट ज़रूरी है विज्ञापनों के लिए)
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (bool) Use architectures like armeabi-v7a, arm64-v8a
android.archs = arm64-v8a, armeabi-v7a

# (list) Android building dependencies (Google Ads SDK को शामिल किया गया है)
android.gradle_dependencies = 'com.google.android.gms:play-services-ads:22.6.0'

# (list) Android application meta-data (AdMob App ID सेट की गई है)
# नोट: प्ले स्टोर पर डालते समय इस टेस्ट आईडी को अपनी असली AdMob App ID से बदलें
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

# (bool) Allow backup
android.allow_backup = True

# (str) The Android architectural target (apk या aab)
# अभी टेस्ट करने के लिए 'apk' रखा है। जब प्ले स्टोर पर डालना हो तो इसे 'aab' कर देना।
target = apk

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
