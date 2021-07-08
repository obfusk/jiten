from pythonforandroid.recipe import PythonRecipe

class KanjidrawRecipe(PythonRecipe):
    version = '0.2.3'
    url = 'https://github.com/obfusk/kanjidraw/archive/v{version}.tar.gz'
    depends = ['setuptools']
    call_hostpython_via_targetpython = False

recipe = KanjidrawRecipe()
