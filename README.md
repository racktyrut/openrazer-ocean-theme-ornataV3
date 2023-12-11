# openrazer-ocean-theme-ornataV3

A theme for the Ornata V3 Razer keyboard on linux, with openrazer.

## Description

The [openrazer project](https://github.com/openrazer/openrazer) allows users to run python script that enhanced the feature of creating customs effects. Scripting openrazer themes allow users to custom their devices as if they were on Windows, using the official razer client. Whit that users can create complex themes, including layers management, color variations, time based features and all of what user's imagination can create in python.

An openrazer theme script use the *openrazer/pylib* python library of the project. Some themes are already presented in *openrazer/examples*.

# How it works

> This theme was only build for the Ornata V3 (02A1) razer keyboard. !

The code was based on the [keyboard.py](https://gist.github.com/bluzukk/2f5ce1d21bcafbf6dd70d0b8f95a30f1) code of [bluzukk](https://gist.github.com/bluzukk)

Using that, we wrote a custom script theme called **"Ocean"**. This theme is composed of two layer :
1. Static blue color layer.
2. Reactive light blue color layer.

The KEY_MAPPING dictionnary was rebuild, and contains the **scan_code** of each key of the kb, this is to be sure of what key was pressed or released. But this imply to use the keyboard python lib that have to be run as root.

The keyboard is divided in 10 zones, left (0) to right (9).

The script is multi-threaded for necessity and efficiency.

## How to use

We invite you to take this code and rewrite it as you want.

The color are saved into constants as the fading time (when a key is released)

To run this code it is necessary to run the openrazer daemon as root (not secure) :

  $ sudo openrazer-daemon --as-root

And then :

  $ sudo python3 ocean.py

## Ends

Thanks to you.

