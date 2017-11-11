#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/11 13:58
# @Author  : Guo Ziyao
from setuptools import setup

setup(
    name='z_blog',
    packages=['z_blog'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)