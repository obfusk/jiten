from pythonforandroid.recipe import PythonRecipe

class FlaskRecipe(PythonRecipe):
    version = '2.0.1'
    url = 'https://github.com/pallets/flask/archive/{version}.zip'

    depends = ['setuptools', 'click', 'jinja2', 'werkzeug', 'itsdangerous']

    call_hostpython_via_targetpython = False
    install_in_hostpython = False

recipe = FlaskRecipe()
