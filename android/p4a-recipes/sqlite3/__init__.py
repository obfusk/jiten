def _patch():
  global Sqlite3Recipe, recipe
  import importlib.util as IU, os
  name  = "pythonforandroid.recipes._sqlite3"
  file  = os.path.join(os.path.dirname(__file__), "_sqlite3.py")
  spec  = IU.spec_from_file_location(name, file)
  mod   = IU.module_from_spec(spec)
  spec.loader.exec_module(mod)
  Sqlite3Recipe, recipe = mod.Sqlite3Recipe, mod.recipe
  Sqlite3Recipe.name    = "sqlite3"
  Sqlite3Recipe.version = "3.36.0"
  Sqlite3Recipe.url     = "https://www.sqlite.org/2021/sqlite-amalgamation-3360000.zip"
_patch()
