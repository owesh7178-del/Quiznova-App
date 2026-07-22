name: Build APK

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-22.04

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install System Dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y git zip unzip colordiff libstdc++6 python3-pip build-essential libltdl-dev libffi-dev libssl-dev openjdk-17-jdk
        echo "JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64" >> $GITHUB_ENV

    - name: Install Stable Buildozer & P4A (Release Tag)
      run: |
        python -m pip install --upgrade pip
        pip install "cython<3.0.0" virtualenv
        pip install buildozer
        # 🔒 Python 3.14 बग से बचने के लिए p4a का स्टेबल रिलीज़ वर्ज़न इंस्टॉल कर रहे हैं
        pip install python-for-android==2024.1.21

    - name: Fix Android SDK Tools Path Bug
      run: |
        sudo mkdir -p /usr/local/lib/android/sdk/tools/bin
        if [ -f "/usr/local/lib/android/sdk/cmdline-tools/latest/bin/sdkmanager" ]; then
          sudo ln -sf /usr/local/lib/android/sdk/cmdline-tools/latest/bin/sdkmanager /usr/local/lib/android/sdk/tools/bin/sdkmanager
        elif [ -f "/usr/local/lib/android/sdk/cmdline-tools/16.0/bin/sdkmanager" ]; then
          sudo ln -sf /usr/local/lib/android/sdk/cmdline-tools/16.0/bin/sdkmanager /usr/local/lib/android/sdk/tools/bin/sdkmanager
        fi
        yes | sdkmanager --licenses || true

    - name: Purge Cache & Execute Build
      run: |
        export ANDROID_HOME=/usr/local/lib/android/sdk
        unset ANDROID_NDK
        unset ANDROID_NDK_HOME
        unset ANDROID_NDK_ROOT
        
        # 💣 पुराना सारा कैशे साफ़ करना
        rm -rf .buildozer/
        rm -rf ~/.buildozer/
        
        buildozer android debug

    - name: Upload APK Artifact
      uses: actions/upload-artifact@v4
      with:
        name: app-release
        path: bin/*.apk
