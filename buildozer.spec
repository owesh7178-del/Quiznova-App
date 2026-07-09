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

# (string) Version of your application
version = 0.1

# (list) Application requirements
requirements = python3, kettle, kivy, urllib3, kivmob

# (str) Supported orientations (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# =============================================================================
# Android specific configuration
# =============================================================================

# (list) Android permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (bool) Use architectures like armeabi-v7a, arm64-v8a
android.archs = arm64-v8a, armeabi-v7a

# (list) Android building dependencies
android.gradle_dependencies = 'com.google.android.gms:play-services-ads:22.6.0'

# (list) Android application meta-data
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

# (bool) Allow backup
android.allow_backup = True

# (str) The Android architectural target
target = apk

[buildozer]
log_level = 2
warn_on_root = 1
