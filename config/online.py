#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/11 11:17
# @Author  : Guo Ziyao
import os

from z_blog import app

DATABASE = os.path.join(app.root_path, 'db/z_blog.db')
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = '000000'