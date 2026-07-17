name: Build APK

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install --upgrade buildozer cython virtualenv

    - name: Install Android SDK/NDK dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y ccache libncurses5:i386 libstdc++6:i386 libgtk2.0-0:i386 libpangox-1.0-0:i386 libpangoxft-1.0-0:i386 libidn11:i386 python3-dev
        sudo apt-get install -y openjdk-17-jdk
        echo "JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64" >> $GITHUB_ENV

    # 🧹 यह स्टेप पुराने जंग खाए हुए टूल्स को साफ़ कर देगा
    - name: Clean Buildozer Cache
      run: |
        buildozer android clean || true

    - name: Build APK with Buildozer
      run: |
        buildozer android debug
