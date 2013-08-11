#-*- coding: utf-8 -*-

import flask
from flask import Flask
from flask import request
from flask import render_template

from indexing import Indexing
from retrieval import Retrieval

app = Flask(__name__)

@app.route('/')
def index():
	index_handler = Indexing()
	index_handler.index()
	return render_template('index.html')

#
# [Search] => 'http://127.0.0.1:5000/search?query=test' or 'http://127.0.0.1:5000/search/test'
#

def _search(query = None, other_param = None):
    retrieve_handler = Retrieval()
    retrieve_out = retrieve_handler.retrieve(query)
    return retrieve_out

@app.route('/search', methods=['GET'])
def search_query_custom():
    query = request.args.get('query')
    return _search(query = query)

@app.route('/search/<query>', methods=['GET'])
def search_query(query):
    return _search(query = query)

#
# [Content] => 'http://127.0.0.1:5000/content?id=test' or 'http://127.0.0.1:5000/content/test'
#

def _content(doc_id = None, other_param = None):
    retrieve_handler = Retrieval()
    retrieve_out = retrieve_handler.getDocument2(doc_id)

    return retrieve_out

@app.route('/content', methods=['GET'])
def search_content_custom():
    doc_id = request.args.get('id')
    return _content(doc_id = doc_id)

@app.route('/content/<id>', methods=['GET'])
def search_content(doc_id):
    return _content(doc_id = doc_id)


if __name__ == "__main__":
        app.run()
