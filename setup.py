from setuptools import setup, find_packages

DESCRIPTION = "Parse XML files generated from POLUtils"

with open('README') as f:
    LONG_DESCRIPTION = f.read()

VERSION = '0.0.5'

setup(
    name = "POLUtils Parser",
    version = VERSION,
    author = "Matthew Scragg",
    author_email = "scragg@gmail.com",
    description = DESCRIPTION,
    license = "MIT",
    url = "https://github.com/scragg0x/polutils-parser",
    packages=find_packages(),
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
    test_suite='tests'
)
