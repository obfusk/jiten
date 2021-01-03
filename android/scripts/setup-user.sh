#!/bin/bash
set -xe
if [ -z "$PIP_INSTALL" ]; then PIP_INSTALL='pip3 install --user'; fi
$PIP_INSTALL --upgrade ${BUILDOZER:-buildozer}
$PIP_INSTALL --upgrade Cython==0.29.19 virtualenv
# FIXME
buildozer="$( python3 -c 'import buildozer.targets.android as x; print(x.__file__)' )"
sed -r 's!^( *_version *=) *re.search.*!\1 self.android_ndk_version!' "$buildozer" -i
