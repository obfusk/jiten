def _patch():
  global Python3Recipe, recipe
  import importlib.util as IU, os
  name  = "pythonforandroid.recipes._python3"
  file  = os.path.join(os.path.dirname(__file__), "_python3.py")
  spec  = IU.spec_from_file_location(name, file)
  mod   = IU.module_from_spec(spec)
  spec.loader.exec_module(mod)
  Python3Recipe, recipe         = mod.Python3Recipe, mod.recipe
  Python3Recipe.configure_args += ("--enable-loadable-sqlite-extensions",)
  Python3Recipe.version         = "3.8.6"
_patch()
