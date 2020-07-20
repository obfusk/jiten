def _patch():
  global PyjniusRecipe, recipe
  import importlib.util as IU, os
  name  = "pythonforandroid.recipes._pyjnius"
  file  = os.path.join(os.path.dirname(__file__), "_pyjnius.py")
  spec  = IU.spec_from_file_location(name, file)
  mod   = IU.module_from_spec(spec)
  spec.loader.exec_module(mod)
  PyjniusRecipe, recipe = mod.PyjniusRecipe, mod.recipe
  PyjniusRecipe.version = "1.3.0"
_patch()
