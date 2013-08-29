#-*- coding: utf-8 -*-

import flask
from flask import Flask

from indexing import Indexing
from retrieval import Retrieval

app = Flask(__name__)

@app.route('/')
def index():
    # just for test
    handler = Indexing()
    handler.index()
    return "Welcome to Noormags-Server"

#
# [Search] => 'http://127.0.0.1:5000/search?query=test' or 'http://127.0.0.1:5000/search/test'
#

def _search(query = None, other_param = None):
    handler = Retrieval()
    result = handler.retrieve(query)
    return result

@app.route('/search', methods=['GET'])
def search_query_custom():
    query = request.args.get('query')
    return _search(query = query)

@app.route('/search/<query>', methods=['GET'])
def search_query(query):
    return _search(query = query)

#
# [Content] => 'http://127.0.0.1:5000/content?id=1' or 'http://127.0.0.1:5000/content/1'
#

def _content(doc_id = None, other_param = None):
    handler = Retrieval()
    result = handler.document(doc_id)
    return result

@app.route('/content', methods=['GET'])
def search_content_custom():
    doc_id = request.args.get('id')
    return _content(doc_id = doc_id)

@app.route('/content/<id>', methods=['GET'])
def search_content(doc_id):
    return _content(doc_id = doc_id)

if __name__ == "__main__":
        app.run()