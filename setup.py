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
    license = "GNU General Public License v3 (GPLv3)",
    keywords = ["dcc", "nmra", "pi", "raspberry", "modelling",
                "train", "decoder" ],
    install_requires=[
        'bitarray',
    ],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: "GNU General Public License v3 (GPLv3)
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
    long_description = read('README.md')
)
