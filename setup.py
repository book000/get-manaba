from setuptools import setup

setup(
    name='get-manaba',
    version='2.0.0',
    packages=['manaba'],
    install_requires=["beautifulsoup4", "requests", "html5lib"],
    url='https://github.com/book000/get-manaba',
    license='MIT License',
    author='tomachi',
    author_email='tomachi@tomacheese.com',
    description='Library for get various information about manaba.'
)
