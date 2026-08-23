[app]

# (str) Title of your application
title = QuizNova

# (str) Package name
package.name = quiznova

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
GitHub par automated build chalane ke liye exact aur optimized `buildozer.spec` ka code niche diya gaya hai. 

Apni GitHub repository ke root folder mein **`buildozer.spec`** naam ki file banayein aur is code ko paste kar dein:

```ini
[app]

# (str) Title of your application
title = QuizNova

# (str) Package name
package.name = quiznova

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning
version = 0.1

# (list) Application requirements
# KivMob GitHub Actions workflow me automatically pyjnius ke sath manage ho jata hai
requirements = python3,kivy==2.2.1,pyjnius

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions required by the app
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API
android.api = 33

# (int) Minimum API supported
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (list) The Android archs to build for
android.archs = arm64-v8a

# (bool) Accept SDK license automatically
android.accept_sdk_license = True

# (list) AdMob Application ID Metadata
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = disable, 1 = enable)
warn_on_root = 1
