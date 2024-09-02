__author__ = "weijie"

import os as _os
import sys as _sys

from EmQuantAPI import *  # noqa: F403


def installEmQuantAPI():
    print("Start to install EmQuantAPI...")

    if UtilAccess.adapter.get_py_name() != PY_Python3:
        print("Error: Python version must be 3.x!")
        return

    currDir = _os.path.split(_os.path.realpath(__file__))[0]
    site_pkg_names = ["site-packages"]
    if UtilAccess.adapter.get_os_name() == OS_Linux:
        site_pkg_names.append("dist-packages")

    # get site-packages path
    packagepath = ""
    for site_pkg_name in site_pkg_names:
        if packagepath != "":
            break
        for spath in _sys.path:
            pos = spath.find(site_pkg_name)
            if pos >= 0 and spath[pos:] == site_pkg_name:
                packagepath = spath
                break

    if packagepath != "":
        pthPath = _os.path.join(packagepath, "EmQuantAPI.pth")
        pthFile = open(pthPath, "w")
        pthFile.writelines(currDir)
        pthFile.close()
        print("Success:", "EmQuantAPI installed.")
    else:
        print("Error: EmQuantApi install fail!(in get pth)")


if __name__ == "__main__":
    installEmQuantAPI()
