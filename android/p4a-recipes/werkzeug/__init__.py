from pythonforandroid.recipe import PythonRecipe

class WerkzeugRecipe(PythonRecipe):
    version = '2.0.1'
    url = 'https://github.com/pallets/werkzeug/archive/{version}.zip'
    depends = ['setuptools']
    call_hostpython_via_targetpython = False

recipe = WerkzeugRecipe()
