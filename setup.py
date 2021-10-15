import setuptools

setuptools.setup(
    name='get-manaba',
    version='2.0.6',
    packages=setuptools.find_packages(),
    install_requires=["beautifulsoup4", "requests", "html5lib"],
    url='https://github.com/book000/get-manaba',
    license='MIT',
    author='Tomachi',
    author_email='tomachi@tomacheese.com',
    maintainer='Tomachi',
    maintainer_email='tomachi@tomacheese.com',
    description='Library for get various information about manaba.',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],
)
