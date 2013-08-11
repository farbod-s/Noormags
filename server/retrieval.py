#-*- coding: utf-8 -*-

import os,sys,glob
import lucene
from lucene import SimpleFSDirectory, System, File, Document, Field, StandardAnalyzer, IndexSearcher, Version, QueryParser

class Retrieval():
	def __init__( self):
		self.INDEX_DIR = "./MyIndex"

	def retrieve( self, query, max_res = 10 ):
  	      	lucene.initVM()
		inDir = SimpleFSDirectory( File( self.INDEX_DIR ) )
	        lucene_analyzer = StandardAnalyzer( Version.LUCENE_30 )
	        lucene_searcher = IndexSearcher( inDir )
	        my_query = QueryParser( Version.LUCENE_30, 'content' , lucene_analyzer ).parse( query )
	        # default: top 10!
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
				_rank = str( it )
				_score = str( hit.score )
				_title = doc.get( 'title' )
				_id = doc.get( 'id' )
				res_body += '{"rank":' + _rank + ',"score":"' + _score + '","title":"' + _title + '","id":"' + _id + '"}'
				if ( it < hits ):
					res_body += ','

			result += res_body

		result += res_tail

		return result

	def getDocument( self, docId, docDir = "./" ):
		result = '{'
                # read input file (.xml)
                for inFile in glob.glob( os.path.join( docDir, '*.xml' ) ):
                        text = open( inFile, 'r' ).read()

                        start = -1
                        end = -1

                        while ( True ):
                                # find ID
                                start = text.find( 'ArticleID="', end + 1 )
                                if ( start == -1 ):
                                        break
                                start += len( 'ArticleID="' )
                                end = text.find( '"', start + 1 )
                                art_id = text[start : end]

                                if ( art_id != docId ):
					continue

				result += '"id":"'
				result += art_id
				result += '",'

				# find Title
				start = text.find( 'Title="', end + 1 )
				if ( start == -1 ):
        	                        break
				start += len( 'Title="' )
				end = text.find( '"', start + 1 )
				art_title = text[start : end]

				result += '"title":"'
                                result += art_title
                                result += '",'

				# find Abstract
				start = text.find( '<Abstract>', end + 1 )
				if ( start == -1 ):
                	                break
				start += len( '<Abstract>' )
				end = text.find( '</Abstract>', start + 1 )
				art_abstract = text[start : end]
	
				result += '"abstract":"'
                                result += art_abstract
                                result += '",'

				# find Keyword
				start = text.find( '<Keyword>', end + 1 )
				if ( start == -1 ):
                	                break
				start += len( '<Keyword>' )
				end = text.find( '</Keyword>', start + 1 )
				art_keyword = text[start : end]
	
				result += '"keyword":"'
                                result += art_keyword
                                result += '",'

				# find Content
				start = text.find( '<Content>', end + 1 )
				if ( start == -1 ):
                	                break
				start += len( '<Content>' )
				end = text.find( '</Content>', start + 1 )
				art_content = text[start : end]
	
				result += '"content":"'
                                result += art_content
                                result += '",'

				# find Authors
				start = text.find( '<Authors>', end + 1 )
				if ( start == -1 ):
					break
				start += len( '<Authors>' )
				end = text.find( '</Authors>', start + 1 )
				art_authors = text[start : end]

				result += '"authors":"'
                                result += art_authors
                                result += '"'

				break

		result += '}'

		return result

	def getDocument2( self, docId, max_res = 1 ):
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
                                _id = doc.get( 'id' )
                                _title = doc.get( 'title' )
                                _abstract = doc.get( 'abstract' )
                                _keyword = doc.get( 'keyword' )
                                _content = doc.get( 'content' )
                                _authors = doc.get( 'authors' )
                                result += '"id":"'
                                result += _id
                                result += '",'
                                result += '"title":"'
                                result += _title
                                result += '",'
                                result += '"abstract":"'
                                result += _abstract
                                result += '",'
                                result += '"keyword":"'
                                result += _keyword
                                result += '",'
                                result += '"content":"'
                                result += _content
                                result += '",'
                                result += '"authors":"'
                                result += _authors
                                result += '"'
                result += '}'
                return result
