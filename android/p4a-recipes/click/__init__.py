from pythonforandroid.recipe import PythonRecipe

class ClickRecipe(PythonRecipe):
    version = '8.0.1'
    url = 'https://github.com/pallets/click/archive/{version}.zip'

    depends = ['setuptools']

    call_hostpython_via_targetpython = False
    install_in_hostpython = True

recipe = ClickRecipe()
