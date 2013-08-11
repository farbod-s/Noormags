import os,sys,glob
import lucene
from lucene import SimpleFSDirectory, System, File, Document, Field, StandardAnalyzer, IndexSearcher, Version, QueryParser

class Retrieval():
	def __init__(self):
		self.INDEX_DIR = "./MyIndex"

	def retrieve(self, query):
  	      	lucene.initVM()
		inDir = SimpleFSDirectory( File( self.INDEX_DIR ) )
	        lucene_analyzer = StandardAnalyzer( Version.LUCENE_30 )
	        lucene_searcher = IndexSearcher( inDir )
	        my_query = QueryParser( Version.LUCENE_30, 'content' , lucene_analyzer ).parse( query )
	        # top 100!
		MAX = 100
	        total_hits = lucene_searcher.search( my_query, MAX )
	        print "Hits: ", total_hits.totalHits
	        for hit in total_hits.scoreDocs:
	                print "Hit String:", hit.toString()
	                doc = lucene_searcher.doc( hit.doc )
	                print doc.getField( 'id' )
