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
  Python3Recipe.version         = "3.8.5"
  old_get_recipe_env = Python3Recipe.get_recipe_env
  def new_get_recipe_env(*a, **kw):
    env = old_get_recipe_env(*a, **kw)
    env["CFLAGS"] += " -O3"
    return env
  Python3Recipe.get_recipe_env = new_get_recipe_env
_patch()
