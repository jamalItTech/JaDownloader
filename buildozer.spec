[app]

title = JaFlex Downloader
package.name = jaflexdownloader
package.domain = com.jaflex.downloader
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,yt-dlp
orientation = portrait
fullscreen = 0
icon.filename = icon.png

# Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]

log_level = 2
warn_on_root = 1
