import compileall
import os
import site

# Find the path to site-packages
site_packages_path = site.getsitepackages()[0]

# Specify the library name
library_name = "supervisely"

# Construct the path to the heavy library
library_path = os.path.join(site_packages_path, library_name)

# Compile the specific library
compileall.compile_dir(library_path, force=True)
