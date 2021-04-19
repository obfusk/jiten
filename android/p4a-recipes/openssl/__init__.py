def _patch():
  global OpenSSLRecipe, recipe
  import importlib.util as IU, os
  name  = "pythonforandroid.recipes._openssl"
  file  = os.path.join(os.path.dirname(__file__), "_openssl.py")
  spec  = IU.spec_from_file_location(name, file)
  mod   = IU.module_from_spec(spec)
  spec.loader.exec_module(mod)
  OpenSSLRecipe, recipe     = mod.OpenSSLRecipe, mod.recipe
  OpenSSLRecipe.name        = "openssl"
  OpenSSLRecipe.url_version = "1.1.1k"
_patch()
