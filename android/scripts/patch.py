#!/usr/bin/env python3
import subprocess

def run(cmd):
  subprocess.run(cmd, shell = True, check = True, cwd = ".p4a")

# FIXME
def patch_webview():
  file  = "pythonforandroid/bootstraps/webview/build/" \
        + "src/main/java/org/kivy/android/PythonActivity.java"
  sett  = " "*12 + "mWebView.getSettings()."
  zoomc = sett + "setBuiltInZoomControls(true);"
  zoomd = sett + "setDisplayZoomControls(false);"
  ext   = "\\n".join( " "*18 + x for x in """
    if(!(url.startsWith("file:") || url.startsWith("http://127.0.0.1:"))) {
      Intent i = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
      startActivity(i);
      return true;
    }
  """.splitlines()[1:-1] ).replace("/", "\\/")
  cmd   = """
    set -e
    if ! grep -qF ZoomControls {file}; then
      sed '/setDomStorageEnabled/ s/$/\\n{zoomc}\\n{zoomd}/' -i {file}
      if ! grep -qF ZoomControls {file}; then echo failed; exit 1; fi
      echo patched zoom
    fi
    if ! grep -qF android.net.Uri {file}; then
      sed '/import.*WebView;/ s/$/\\nimport android.net.Uri;/' -i {file}
      if ! grep -qF android.net.Uri {file}; then echo failed; exit 1; fi
      echo patched uri
    fi
    if ! grep -qF url.startsWith {file}; then
      sed '/shouldOverrideUrlLoading/ s/$/\\n{ext}/' -i {file}
      if ! grep -qF url.startsWith {file}; then echo failed; exit 1; fi
      echo patched load
    fi
  """.format(file = file, zoomc = zoomc, zoomd = zoomd, ext = ext)
  print("Patching webview activity ...")
  run(cmd)

# FIXME
def patch_python():
  file  = "pythonforandroid/bootstraps/common/build/" \
        + "src/main/java/org/kivy/android/PythonUtil.java"
  cmd   = """
    set -e
    if ! grep -qF python3.9 {file}; then
      sed 's/python3\\.8/python3.9/g' -i {file}
      if ! grep -qF python3.9 {file}; then echo failed; exit 1; fi
      echo patched python3.9
    fi
  """.format(file = file)
  print("Patching python util ...")
  run(cmd)

# FIXME
def patch_android():
  file1 = "pythonforandroid/recipes/android/__init__.py"
  file2 = "pythonforandroid/recipes/android/src/setup.py"
  cmd   = r"""
    set -e
    if ! grep -qF WebView_AndroidGetJNIEnv __FILE1__; then
      patch __FILE1__ <<-EOF
	--- a/pythonforandroid/recipes/android/__init__.py
	+++ b/pythonforandroid/recipes/android/__init__.py
	@@ -77,6 +77,11 @@ class AndroidRecipe(IncludedFilesBehaviour, CythonRecipe):
	                 fh.write(
	                     '#define SDL_ANDROID_GetJNIEnv SDL_AndroidGetJNIEnv\n'
	                 )
	+            else:
	+                fh.write('JNIEnv *WebView_AndroidGetJNIEnv(void);\n')
	+                fh.write(
	+                    '#define SDL_ANDROID_GetJNIEnv WebView_AndroidGetJNIEnv\n'
	+                )


	 recipe = AndroidRecipe()
	EOF
    if ! grep -qF main __FILE2__; then
      patch __FILE2__ <<-EOF
	--- a/pythonforandroid/recipes/android/src/setup.py
	+++ b/pythonforandroid/recipes/android/src/setup.py
	@@ -5,7 +5,7 @@ library_dirs = ['libs/' + os.environ['ARCH']]
	 lib_dict = {
	     'sdl2': ['SDL2', 'SDL2_image', 'SDL2_mixer', 'SDL2_ttf']
	 }
	-sdl_libs = lib_dict.get(os.environ['BOOTSTRAP'], [])
	+sdl_libs = lib_dict.get(os.environ['BOOTSTRAP'], ['main'])

	 modules = [Extension('android._android',
	                      ['android/_android.c', 'android/_android_jni.c'],
	EOF
    fi
  """.replace("__FILE1__", file1).replace("__FILE2__", file2)
  print("Patching android recipe ...")
  run(cmd)

patch_webview()
patch_python()
patch_android()
