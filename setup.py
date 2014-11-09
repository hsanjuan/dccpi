from distutils.core import setup, Extension
setup(
    name = "dccpi",
    packages = ["dccpi"],
    version = "0.0.1",
    description = "A Python NMRA DCC protocol implementation for RaspberryPi",
    author = "Hector Sanjuan",
    author_email = "hector@convivencial.org",
    url = "https://github.com/hsanjuan/dccpi",
    download_url = "",
    license = "GNU General Public License v3 (GPLv3)",
    keywords = ["dcc", "nmra", "pi", "raspberry", "modelling",
                "train", "decoder" ],
    install_requires=[
        'bitstring',
    ],
    ext_modules=[
        Extension('dcc_rpi_encoder_c',
                  sources = ['extensions/dcc_rpi_encoder_c.c'],
                  libraries = ['wiringPi'])
    ],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 1 - Planning",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Networking",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    long_description = """\
NRMA Digical Command Control (DCC) implementation for Raspberry Pi
==================================================================

This module implements the DCC protocol for controlling model trains using a RaspberryPi.

It is able to output direction and speed DCC-encoded packets on one of the GPIO pins.

It is based on the:
 - `S-91 Electrical Standard <http://www.nmra.org/sites/default/files/standards/sandrp/pdf/s-9.1_electrical_standards_2006.pdf>`_
 - `S-92 DCC Communications Standard <http://www.nmra.org/sites/default/files/s-92-2004-07.pdf>`_

Please visit the github page for more information: https://github.com/hsanjuan/dccpi.
    """
)
