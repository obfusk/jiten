from pythonforandroid.recipe import PythonRecipe

class Jinja2Recipe(PythonRecipe):
    version = '3.0.1'
    url = 'https://github.com/pallets/jinja/archive/{version}.zip'
    depends = ['setuptools', 'markupsafe']

recipe = Jinja2Recipe()
