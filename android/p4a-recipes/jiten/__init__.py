from pythonforandroid.recipe import CompiledComponentsPythonRecipe, Recipe
from pythonforandroid.logger import info

class JitenRecipe(CompiledComponentsPythonRecipe):
    # name = 'jiten'
    # version = '0.1.1'
    # url = 'https://github.com/obfusk/jiten/archive/v{version}.tar.gz'

    depends = ['setuptools', 'flask', 'click', 'sqlite3', 'libpcre']

    call_hostpython_via_targetpython = False
    install_in_hostpython = False

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        env['JITEN_ANDROID'] = 'yes'

        def add_flags(include_flags, link_dirs, link_libs):
            env['CPPFLAGS'] = env.get('CPPFLAGS', '') + include_flags
            env['LDFLAGS'] = env.get('LDFLAGS', '') + link_dirs
            env['LIBS'] = env.get('LIBS', '') + link_libs

        info('Activating flags for sqlite3')
        recipe = Recipe.get_recipe('sqlite3', self.ctx)
        add_flags(' -I' + recipe.get_build_dir(arch.arch),
                  ' -L' + recipe.get_lib_dir(arch), ' -lsqlite3')

        info('Activating flags for libpcre')
        recipe = Recipe.get_recipe('libpcre', self.ctx)
        add_flags(' -I' + recipe.get_build_dir(arch.arch),
                  ' -L' + recipe.get_lib_dir(arch), ' -lpcre')

        return env

recipe = JitenRecipe()

# FIXME
def _patch_webview():
    import subprocess
    file  = "pythonforandroid/bootstraps/webview/build/" \
          + "src/main/java/org/kivy/android/PythonActivity.java"
    sett  = " "*12 + "mWebView.getSettings()."
    zoomc = sett + "setBuiltInZoomControls(true);"
    zoomd = sett + "setDisplayZoomControls(false);"
    cmd   = """
      set -e
      if ! grep -q ZoomControls {file}; then
        sed '/setDomStorageEnabled/ s/$/\n{zoomc}\n{zoomd}/' -i {file}
        echo patched
      fi
    """.format(file = file, zoomc = zoomc, zoomd = zoomd)
    info("Patching webview to allow zoom...")
    subprocess.run(cmd, shell = True, check = True)

_patch_webview()
