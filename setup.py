# chardet's setup.py
from distutils.core import setup
setup(
    name = "dccpi",
    packages = ["dccpi"],
    version = "0.0.1",
    description = "A Python NMRA DCC implementation for RaspberryPi",
    author = "Hector Sanjuan",
    author_email = "hector@convivencial.org",
    url = "https://github.com/hsanjuan/dccpi",
    download_url = "",
    keywords = ["dcc", "nmra", "pi", "raspberry", "modelling", "train", "decoder" ],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        "Development Status :: 1 - Alpha",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Operating System :: Linux",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Software Development :: Embedded Systems",
        "Topic :: System :: Networking",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    long_description = """\
NRMA Digical Command Control (DCC) implementation for Raspberry Pi
------------------------------------------------------------------

This module allows to use a minimal subset of the DCC protocol to
control DCC-compatible devices, usually model trains, using the 
Raspberry PI GPIO interface.

It is based on the:
  * [S-91 Electrical Standard](http://www.nmra.org/sites/default/files/standards/sandrp/pdf/s-9.1_electrical_standards_2006.pdf)
  * [S-92 DCC Communications Standard](http://www.nmra.org/sites/default/files/s-92-2004-07.pdf)

"""
)
