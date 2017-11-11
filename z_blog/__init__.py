#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/11 11:13
# @Author  : Guo Ziyao
import os
import sqlite3

from flask import abort
from flask import flash
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

app = Flask(__name__)
app.config.from_object('config.online')


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    from z_blog.common.db import init_db
    init_db()
    print('Initialized the database.')
