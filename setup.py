from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'One Piece - Downloader'
LONG_DESCRIPTION = 'One Piece - Downloader'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="piece",
    version=VERSION,
    author="Joao Carlos",
    author_email="<joaocarlos@duck.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'one piece'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
