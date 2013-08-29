# coding=utf8

import os, sys, glob, codecs
from pyquery import PyQuery as pq

from pltk.PerStemmer import PerStemmer
import lucene
from lucene import  SimpleFSDirectory,\
					System,\
					File,\
					Document,\
					Field,\
					StandardAnalyzer,\
					IndexWriter,\
					Version

""" Indexing Class
"""
class Indexing():
	def __init__( self, doc_dir = './data/corpus', index_dir = './data/index-dir' ):
		self.DOC_DIR = doc_dir
		self.INDEX_DIR = index_dir
		self.stemmer = PerStemmer()

	def stem( self, token ):
		return self.stemmer.stemText(token)

	def index( self ):
		lucene.initVM()
		indexdir = SimpleFSDirectory( File( self.INDEX_DIR ) )
		analyzer = StandardAnalyzer( Version.LUCENE_30 )
		index_writer = IndexWriter( indexdir, analyzer, True, IndexWriter.MaxFieldLength( 512 ) )
		# read input files (.xml)
		for in_file in glob.glob( os.path.join( self.DOC_DIR, '*.xml' ) ):
			corpus = codecs.open( in_file, encoding='utf-8' ).read()
			d = pq( corpus, parser='html' )
			for text in d( 'Article' ).items():
				document = Document()
				# find ID
				art_id = str( text.attr( 'articleid' ).encode( 'utf-8' ) ).replace( '+', '-' )
				# find Title
				art_title = self.stem( str( text.attr( 'title' ).encode( 'utf-8' ) ) )
				# find Abstract
				art_abstract = self.stem( str( text.find( 'Abstract' ).html().encode('utf-8') ) )
				# find Keyword
				art_keyword = text.find( 'Keyword' ).html().encode('utf-8')
				# find Content
				art_content = self.stem( str( text.find( 'Content' ).html().encode('utf-8') ) )
				# find Authors
				art_authors = text.find( 'Authors' ).html().encode('utf-8')
				document.add( Field( 'id', art_id, Field.Store.YES, Field.Index.ANALYZED ) )
				document.add( Field( 'title', art_title, Field.Store.YES, Field.Index.ANALYZED ) )
				document.add( Field( 'abstract', art_abstract, Field.Store.YES, Field.Index.ANALYZED ) )
				document.add( Field( 'keyword', art_keyword, Field.Store.YES, Field.Index.ANALYZED ) )
				document.add( Field( 'content', art_content, Field.Store.YES, Field.Index.ANALYZED ) )
				document.add( Field( 'authors', art_authors, Field.Store.YES, Field.Index.ANALYZED ) )
				document.add( Field( 'article', art_title + art_abstract + art_keyword + art_content,\
									 Field.Store.YES,\
									 Field.Index.ANALYZED ) )
				index_writer.addDocument( document )
			index_writer.optimize()
			index_writer.close()