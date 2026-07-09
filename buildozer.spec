[app]

# (string) Title of your application
title = Quiznova

# (string) Package name
package.name = quiznova

# (string) Package domain (needed for android packaging)
package.domain = org.owesh

# (string) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,json

# (string) Version of your application
version = 0.1

# (list) Application requirements (सिर्फ ज़रूरी चीजें जो एरर न दें)
requirements = python3, kivy, urllib3

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# =============================================================================
# Android specific configuration
# =============================================================================

# (list) Android permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (bool) Use architectures like armeabi-v7a, arm64-v8a
android.archs = arm64-v8a, armeabi-v7a

# (bool) Allow backup
android.allow_backup = True

# (str) The Android architectural target
target = apk

[buildozer]
log_level = 2
warn_on_root = 1
