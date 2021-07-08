from pythonforandroid.recipe import PythonRecipe

class CertifiRecipe(PythonRecipe):
    version = '2021.5.30'
    url = 'https://pypi.python.org/packages/source/c/certifi/certifi-{version}.tar.gz'
    depends = ['setuptools']
    call_hostpython_via_targetpython = False

recipe = CertifiRecipe()
