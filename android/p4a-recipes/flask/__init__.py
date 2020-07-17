from pythonforandroid.recipe import PythonRecipe

class FlaskRecipe(PythonRecipe):
    version = '1.1.2'
    url = 'https://github.com/pallets/flask/archive/{version}.zip'

    depends = ['setuptools', 'click']
    python_depends = ['jinja2', 'werkzeug', 'markupsafe', 'itsdangerous']

    call_hostpython_via_targetpython = False
    install_in_hostpython = False

recipe = FlaskRecipe()
