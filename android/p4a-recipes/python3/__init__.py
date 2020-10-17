def _patch():
  global Python3Recipe, recipe
  import importlib.util as IU, os
  name  = "pythonforandroid.recipes._python3"
  file  = os.path.join(os.path.dirname(__file__), "_python3.py")
  spec  = IU.spec_from_file_location(name, file)
  mod   = IU.module_from_spec(spec)
  spec.loader.exec_module(mod)
  sqlite_ext  = "--enable-loadable-sqlite-extensions"
  patches     = [
    "patches/py3.8.1.patch",
    "patches/py3.8.1_fix_cortex_a8.patch"
  ]
  Python3Recipe, recipe = mod.Python3Recipe, mod.recipe
  Python3Recipe.version = "3.9.0"
  if sqlite_ext not in Python3Recipe.configure_args:
    Python3Recipe.configure_args += (sqlite_ext,)
  for patch in patches:
    if patch not in Python3Recipe.patches:
      Python3Recipe.patches.append(patch)
_patch()
