#!/bin/zsh

# should be finish in jenkins
python setup.py build
python setup.py bdist_wheel --skip-build
