Noormags Server
===============

search API for **Noormags Server**:

### Search Query

search a text inside of documents, with URLs like these:

```
http://127.0.0.1:5000/search?query=test
```
or
```
http://127.0.0.1:5000/search/test
```

output is documents with `JSON` format, like this:

```
{
	"query":"_query_",
	"result":[
		{
			"rank":1,
			"title":"_title1_"
			"id":"_id1_"
		},
		{
			"rank":2,
			"title":"_title2_"
			"id":"_id2_"
		}
	]
}
```

### Search Content

search a document by its ID, with URLs like these:

```
http://127.0.0.1:5000/content?id=1
```
or
```
http://127.0.0.1:5000/content/1
```

output is a document with `JSON` format, like this:

```
{
	"id":"_id_",
	"content":"_content_"
}
```

<hr />

## Install [PyLucene] (http://pylucene.apache.org/)

for installation of **PyLucene**, use below instruction:

```bash
sudo apt-get install pylucene
```

<hr />

## Install [Flask] (http://flask.pocoo.org/)

for installation of **Flask**, use below instruction:

```bash
sudo pip install flask
```

<hr />

## Run Server with **Flask**

for run server with **Flask**, use bellow sample code:

```python
import flask
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
	return 'Welcome to Noormags-Server'

if __name__ == "__main__":
    app.run()
```

for test your code, you can use below instruction:

```bash
curl http://127.0.0.1:5000
```

* Note: by default flask listen on port 5000, but you can change it within your codes!

<hr />

## Index Documents

you can call `index` function of `Indexing` class, like below:

```python
from indexing import Indexing

index_handler = Indexing()
index_handler.index('doc_dir')
```

we find all `xml` files in a directory that can set by passing an argument through `index` function of `Indexing` class, we called it `doc_dir`.
after that, stem file, seperate all sections (eg, ID - Title - Content - ...) and finally index document by **Lucene**.

<hr />

## Retrieve Documents

you can call `retrieve` function of `Retrieval` class, like below:

```python
from retrieval import Retrieval

retrieve_handler = Retrieval()
result = retrieve_handler.retrieve(_query_)
```

we find all documents that matches with input query.

<hr />