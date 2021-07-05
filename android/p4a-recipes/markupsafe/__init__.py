from pythonforandroid.recipe import PythonRecipe

class MarkupsafeRecipe(PythonRecipe):
    version = '2.0.1'
    url = 'https://github.com/pallets/markupsafe/archive/{version}.zip'
    depends = ['setuptools']

recipe = MarkupsafeRecipe()
