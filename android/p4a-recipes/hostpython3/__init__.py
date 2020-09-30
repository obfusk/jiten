def _patch():
  global HostPython3Recipe, recipe
  import importlib.util as IU, os
  name  = "pythonforandroid.recipes._hostpython3"
  file  = os.path.join(os.path.dirname(__file__), "_hostpython3.py")
  spec  = IU.spec_from_file_location(name, file)
  mod   = IU.module_from_spec(spec)
  spec.loader.exec_module(mod)
  HostPython3Recipe, recipe = mod.HostPython3Recipe, mod.recipe
  HostPython3Recipe.version = "3.8.6"
_patch()
