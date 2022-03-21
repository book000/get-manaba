# get-manaba

[日本語の README はこちらから](https://github.com/book000/get-manaba/blob/master/README-ja.md)

Library for get various information about [manaba](https://manaba.jp).

## Announcement

- This library is mainly designed to operate the service in the developer's university. Please note that it may not work well for other universities.
- The university to which the developer of this library belongs will no longer be using manaba since 2022. As a result, support for this library will be discontinued and it will be archived as of April 2022.
- I am planning to develop a library of ["UNIVERSAL PASSPORT" by Japan System Techniques Co](https://www.jast-gakuen.com/products/unipa/): [book000/get-unipa](https://github.com/book000/get-unipa)

## Warning / Disclaimer

- **The developer assumes no responsibility for any problems resulting from the use of this project and library. Use at your own risk.**
- Do not use this library to make many requests in a short amount of time.

## Documentation

- [get-manaba documents](https://book000.github.io/get-manaba/)

## Requirements

- manaba (Tested with `manaba 2.971`)
  - [Official documentation for student](https://doc.manaba.jp/doc/course2-manual/student2.971/en/)
  - [Official documentation for teacher](https://doc.manaba.jp/doc/course2-manual/teacher2.971/en/)
- Python 3.9+
- [requirements.txt](requirements.txt): `requests`, `beautifulsoup4`, `html5lib`

## Installation

There are two ways to install it, either from PyPI or by cloning the repository.

## Install from PyPI

1. Install get-manaba from PyPI: `pip install -U get-manaba`

## Install from cloning the repository

1. Clone from GitHub repository: `git clone https://github.com/book000/get-manaba.git`
2. Install the dependency package from `requirements.txt`: `pip install -U -r requirements.txt`
3. Install the get-manaba package: `pip install .`

## License

The license for this project is [MIT License](https://github.com/book000/get-manaba/blob/master/LICENSE).
