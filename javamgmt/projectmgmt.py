import os
from javamgmt.packagecreator import PackageManager

__author__ = 'roberto'


if __name__ == '__main__':

    # Specify here the source base path
    basepath = os.path.join("d:\\", "progetti", "javaworks")

    # Specify here all packages
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

    PackageManager.create_project(basepath, packages)