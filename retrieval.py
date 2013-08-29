# coding=utf8

import os, sys, glob, codecs
from pyquery import PyQuery as pq

import lucene
from lucene import SimpleFSDirectory,\
				   System,\
				   File,\
				   Document,\
				   Field,\
				   StandardAnalyzer,\
				   IndexSearcher,\
				   Version,\
				   QueryParser

""" Retrieval Class
"""
class Retrieval():
	def __init__( self, index_dir = './data/index-dir' ):
		self.INDEX_DIR = index_dir

	def retrieve( self, query, max_res = 10 ):
		lucene.initVM()
		inDir = SimpleFSDirectory( File( self.INDEX_DIR ) )
		lucene_analyzer = StandardAnalyzer( Version.LUCENE_30 )
		lucene_searcher = IndexSearcher( inDir )
		my_query = QueryParser( Version.LUCENE_30, 'content' , lucene_analyzer ).parse( query )
		MAX = max_res
		total_hits = lucene_searcher.search( my_query, MAX )
		res_head = '{"query":"' + query + '","results":['
		res_tail = ']}'
		result = res_head
		hits = total_hits.totalHits
		if ( hits > 0 ):
			res_body = ''
			it = 0
			for hit in total_hits.scoreDocs:
				it += 1
				doc = lucene_searcher.doc( hit.doc )
				res_body += '{"rank":' +\
							str( it ) +\
							',"score":"' +\
							str( hit.score ) +\
							'","title":"' +\
							doc.get( 'title' ).encode('utf-8') +\
							'","id":"' +\
							doc.get( 'id' ).encode('utf-8') +\
							'"}'
				if ( it < hits ):
					res_body += ','
			result += res_body
		result += res_tail
		return result

	def document( self, docId, max_res = 1 ):
		lucene.initVM()
		inDir = SimpleFSDirectory( File( self.INDEX_DIR ) )
		lucene_analyzer = StandardAnalyzer( Version.LUCENE_30 )
		lucene_searcher = IndexSearcher( inDir )
		my_query = QueryParser( Version.LUCENE_30, 'id' , lucene_analyzer ).parse( docId )
		MAX = max_res
		total_hits = lucene_searcher.search( my_query, MAX )
		result = '{'
		hits = total_hits.totalHits
		if ( hits == 1 ):
			for hit in total_hits.scoreDocs:
				doc = lucene_searcher.doc( hit.doc )
				result += '"id":"' +\
						  doc.get( 'id' ) +\
						  '","title":"' +\
						  doc.get( 'title' ) +\
						  '","abstract":"' +\
						  doc.get( 'abstract' ) +\
						  '","keyword":"' +\
						  doc.get( 'keyword' ) +\
						  '","content":"' +\
						  doc.get( 'content' ) +\
						  '","authors":"' +\
						  doc.get( 'authors' ) +\
						  '"'
		result += '}'
		return result