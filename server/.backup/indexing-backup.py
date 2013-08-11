import os,sys,glob
import lucene
from lucene import  SimpleFSDirectory, System, File, Document, Field, StandardAnalyzer, IndexWriter, Version

class Indexing():
	def __init__( self ):
		self.INDEX_DIR = "./MyIndex"

	def index( self, docDir = "./" ):
        	lucene.initVM()
	        DIR_TO_INDEX = docDir
	        indexdir = SimpleFSDirectory( File( self.INDEX_DIR ) )
       		analyzer = StandardAnalyzer( Version.LUCENE_30 )
	        index_writer = IndexWriter( indexdir, analyzer, True, IndexWriter.MaxFieldLength( 512 ) )
        
		# read input file (.xml)
		for inFile in glob.glob( os.path.join( DIR_TO_INDEX, '*.xml' ) ):
	                print "Indexing: ", inFile
	                text = open( inFile, 'r' ).read()

			start = -1
			end = -1

			while ( True  ):
				document = Document()

				# find ID
				start = text.find( 'ArticleID="', end + 1 )
				if ( start == -1 ):
                        	        break
				start += len( 'ArticleID="' )
				end = text.find( '"', start + 1 )
				art_id = text[start : end]

				print "\nID: ", art_id
		
				# find Title
				start = text.find( 'Title="', end + 1 )
				if ( start == -1 ):
        	                        break
				start += len( 'Title="' )
				end = text.find( '"', start + 1 )
				art_title = text[start : end]

				print "\nTitle: ", art_title

				# find Abstract
				start = text.find( '<Abstract>', end + 1 )
				if ( start == -1 ):
                	                break
				start += len( '<Abstract>' )
				end = text.find( '</Abstract>', start + 1 )
				art_abstract = text[start : end]
	
				print "\nAbstract: ", art_abstract
	
				# find Keyword
				start = text.find( '<Keyword>', end + 1 )
				if ( start == -1 ):
                	                break
				start += len( '<Keyword>' )
				end = text.find( '</Keyword>', start + 1 )
				art_keyword = text[start : end]
	
				print "\nKeyword: ", art_keyword
	
				# find Content
				start = text.find( '<Content>', end + 1 )
				if ( start == -1 ):
                	                break
				start += len( '<Content>' )
				end = text.find( '</Content>', start + 1 )
				art_content = text[start : end]
	
				print "\nContent: ", art_content
	
				# find Authors
				start = text.find( '<Authors>', end + 1 )
				if ( start == -1 ):
					break
				start += len( '<Authors>' )
				end = text.find( '</Authors>', start + 1 )
				art_authors = text[start : end]

				print "\nAuthors: ", art_authors			

	        		document.add( Field( 'id', art_id, Field.Store.YES, Field.Index.ANALYZED ) )
				document.add( Field( 'title', art_title, Field.Store.YES, Field.Index.ANALYZED ) )
				document.add( Field( 'abstract', art_abstract, Field.Store.YES, Field.Index.ANALYZED ) )
				document.add( Field( 'keyword', art_keyword, Field.Store.YES, Field.Index.ANALYZED ) )
				document.add( Field( 'content', art_content, Field.Store.YES, Field.Index.ANALYZED ) )
				document.add( Field( 'authors', art_authors, Field.Store.YES, Field.Index.ANALYZED ) )
		       		document.add( Field( 'article', art_title + art_abstract + art_keyword + art_content, Field.Store.YES, Field.Index.ANALYZED ) )

         			index_writer.addDocument( document )
               
		print "\nDone: ", inFile

        	index_writer.optimize()
	        print index_writer.numDocs()
        	index_writer.close()
