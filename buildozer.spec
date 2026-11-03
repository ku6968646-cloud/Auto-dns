[app]

# (str) Title of your application
title = Auto DNS Switcher

# (str) Package name
package.name = autodns

# (str) Package domain (needed for android packaging)
package.domain = org.autodns

# (list) Source files to include (let it include python files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Directory where the source files are located
source.dir = .

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3,hostpython3

# (str) Supported orientation
orientation = portrait

# (list) Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

[buildozer]
log_level = 2
warn_on_root = 1

