__author__ = 'roberto'

import os
from javamgmt.packagecreator import PackageManager


# Set flag to True for structure creation
create = True
# Set flag to True for structure build
build = True

# Specify here the source base path
basepath = os.path.join("d:\\", "progetti", "javaworks")

# Specify here all packages and classes
packages = {
    "org.crynet.crypto": [
        "BaseCryptoClass",
    ],
    "org.crynet.utils": [
        "BaseUtils",
        "ExtendedUtils",
    ],
    "org.crynet.web": [
        "WebUtils",
        "ServletUtils",
    ],
    "org.crynet.sec": [
        "SecUtils",
        "AccessControlUtils",
    ],
    "org.crynet.hash": [
        "ShaUtils",
        "MD5Utils",
    ],
    "org.crynet.sym": [
        "AESUtils",
        "TripleDESUtils",
    ],
    "org.crynet.asym": [
        "RSAUtils",
        "ELGamalUtils",
        "ECUtils",
    ],
}


if __name__ == '__main__':

    if create:
        manager = PackageManager.create_project(basepath, packages)
    if build:
        manager = PackageManager.load_project(basepath, packages)
        manager.build_all()