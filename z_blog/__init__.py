#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/11 11:13
# @Author  : Guo Ziyao
from flask import abort
from flask import flash
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

app = Flask(__name__)
app.config.from_object('config.online')

from z_blog.common.db import get_db, init_db


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

# 可视化相关
from py2neo import Graph, Node, Relationship
graph = Graph(
    "http://localhost:7474",
    username="neo4j",
    password="000000"
)


def buildNodes(nodeRecord):
    data = {"name": nodeRecord['name'], "label": next(iter(nodeRecord.labels()))}
    return {"data": data}


def buildEdges(relationRecord):
    data = {"source": relationRecord.start_node()['name'],
            "target": relationRecord.end_node()['name'],
            "relationship": relationRecord.type()}
    return {"data": data}


def query_name(company_name):
    query = u"""
    match p = (a)-[]-()-[]-()
    where a.name = '{name}' 
    return p
    """
    # print query.format(**{'name': company_name})
    return graph.data(query.format(**{'name': company_name}))


@app.route('/visual_data', methods=['GET'])
def visual():
    company_name = request.args.get('company_name')
    results = query_name(company_name)
    nli = []
    rli = []
    for each in results:
        for each_b in each['p'].nodes():
            nli.append(each_b)
        for each_b in each['p'].relationships():
            rli.append(each_b)
    nodes = map(buildNodes, nli)
    edges = map(buildEdges, rli)

    return jsonify(elements={"nodes": nodes, "edges": edges})

@app.route('/graph', methods=['GET'])
def data_view():
    company_name = request.args.get('company_name')
    return render_template('graph.html', company_name=company_name)