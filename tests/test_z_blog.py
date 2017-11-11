#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/11 15:48
# @Author  : Guo Ziyao
import os
import z_blog
import unittest
import tempfile

class Z_BlogTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, z_blog.app.config['DATABASE'] = tempfile.mkstemp()
        z_blog.app.testing = True
        self.app = z_blog.app.test_client()
        with z_blog.app.app_context():
            z_blog.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(z_blog.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin', '000000')
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data
        rv = self.login('adminx', '000000')
        assert b'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert b'Invalid password' in rv.data

    def test_messages(self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data

if __name__ == '__main__':
    unittest.main()