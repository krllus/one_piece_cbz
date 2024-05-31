from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'One Piece - Downloader'
LONG_DESCRIPTION = 'One Piece - Downloader'

# Setting up
setup(
    # the name must match the folder name 'piece'
    name="onepiececbz",
    version=VERSION,
    author="Joao Carlos",
    author_email="<joaocarlos@duck.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'setuptools>=40.9.0',
        'beautifulsoup4==4.11.1',
        'bs4==0.0.1',
        'certifi==2022.9.24',
        'charset-normalizer==2.1.1',
        'idna==3.4',
        'requests==2.28.1',
        'soupsieve==2.3.2.post1',
        'urllib3==1.26.13'
    ],
    keywords=['python', 'one piece'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        'console_scripts' : [
            'piece = piece:episodes_downloader.__main__:main'
        ]
    } 
)
