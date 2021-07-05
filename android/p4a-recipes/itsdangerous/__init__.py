from pythonforandroid.recipe import PythonRecipe

class ItsdangerousRecipe(PythonRecipe):
    version = '2.0.1'
    url = 'https://github.com/pallets/itsdangerous/archive/{version}.zip'
    depends = ['setuptools']

recipe = ItsdangerousRecipe()
