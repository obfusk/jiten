#!/bin/bash
set -xe
if [ -z "$PIP_INSTALL" ]; then PIP_INSTALL='pip3 install'; fi
$PIP_INSTALL --upgrade sh==1.14.2                   # FIXME
$PIP_INSTALL --upgrade ${BUILDOZER:-buildozer==1.2.0}
$PIP_INSTALL --upgrade Cython==0.29.19 virtualenv   # FIXME
# FIXME
# buildozer="$( python3 -c 'import buildozer.targets.android as x; print(x.__file__)' )"
# sed -r 's!^( *_version *=) *re.search.*!\1 self.android_ndk_version!' "$buildozer" -i
