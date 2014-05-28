# realMonkey

realMonkey is an open source, lightweight, cross-platform test automation tool base on uiautomator for mobile apps, tested on emulators(Android) and real devices(Android)

# Supported Platforms
 - Android

#Why realMonkey?
1. You don't have to recomplie your app or modify it in any way, due to use of standard automation APIs on all platforms.
2. You can write tests with your favorite dev tools using [Python](https://www.python.org/download/) language
3. You can test multiple applications in one script

Normal, if use robotium library to write your test case without realMonkey.Then, you must modify your app's signature and compile your test case.Similarly, with Android's uiautomator you have to accept that tedious debugging process.realMonkey opens up the possibility of quickly and simply.Finally!

# Requirements
When use realMonkey, you don't need to do a lot of complicated settings.See below for environment setting.

If you want to write and run test case with realMonkey, you only need to install [Android SDK](http://developer.android.com/sdk/index.html) and [Python](https://www.python.org/download/)(recommend 2.7)

### Android Requirements
 - [Android SDK](http://developer.android.com/sdk/index.html) API>=16
 - realMonkey supports Android on OSX, Linux and Windows. Make sure you setting up your environment properly for testing on different OSes.

# Quick Start
Make sure you have already configured the development environment.

    $ python your/realMonkey/path/test.py
# How It Works
realMonkey depend on adb interact with the device, which is based mainly on Android's uiautomator
# Mailing List
If you have any proplem when you use.
*Contact us: realMonkeyWQM@163.com*

