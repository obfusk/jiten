def _patch():
  global LibffiRecipe, recipe
  import importlib.util as IU, os
  name  = "pythonforandroid.recipes._libffi"
  file  = os.path.join(os.path.dirname(__file__), "_libffi.py")
  spec  = IU.spec_from_file_location(name, file)
  mod   = IU.module_from_spec(spec)
  spec.loader.exec_module(mod)
  LibffiRecipe, recipe = mod.LibffiRecipe, mod.recipe
  LibffiRecipe.version = "v3.3"
_patch()
