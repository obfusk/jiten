from pythonforandroid.recipe import CompiledComponentsPythonRecipe, Recipe
from pythonforandroid.logger import info

class JitenRecipe(CompiledComponentsPythonRecipe):
    # name = 'jiten'
    # version = '0.3.5'
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
