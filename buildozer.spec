[app]
title = 3D Savas
package.name = ucdsavas
package.domain = org.oyun
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,pygame
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/kapak.png
orientation = landscape
fullscreen = 1
android.permissions = INTERNET
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
