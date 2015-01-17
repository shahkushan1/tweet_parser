# Standard Libraries 
from os.path import dirname, realpath
import sys
import re
from urlparse import urlparse, parse_qs

# Project specific third party libraries
from yajl import YajlContentHandler, YajlParser

BASEPATH = dirname(dirname(realpath(__file__)))
DATAPATH = BASEPATH + '/data'
INPUT_FILE_PATH = DATAPATH + '/sample_tweets_data.json'

class ContentHandler(YajlContentHandler):
	'''
	This class hosts all the custom callback routines that
	will be called by YajlParser while parsing the json object
	in a streaming fashion.

	It currently has only one active callback routine that detects
	matches a string and detects whether it matches a regex pattern

	Notes -
	
	The Twitter Streaming API response in /doc/twitter_streaming_api_sample.json
	indicates that when a tweet contains a url, the url is available in the 'text'
	field as well as in the 'urls' field. For more info see the sampled response in
	../data/twitter_streaming_api_sample.json
	
	Hence while stream parsing the json response, this leads to duplicates since 
	the regex will match both the fields. These duplicates are a known issue and
	need to be filtered.
	'''
	def __init__(self):
		self.out = sys.stdout
		# Matches and returns only url part
		# Youtube video IDs usually span 11 characters hence {11}
		self.pattern_to_match = re.compile('http[s]:\/\/www\.youtube\.com/watch\?v\=.{11}|https:\/\/youtu.be\/.{11}')
	def yajl_null(self, ctx):
		pass
	def yajl_boolean(self, ctx, boolVal):
		pass
	def yajl_integer(self, ctx, integerVal):
		pass
	def yajl_double(self, ctx, doubleVal):
		pass
	def yajl_number(self, ctx, stringNum):
		pass
	def yajl_string(self, ctx, stringVal):
		'''
		Generates a callback when string matches the given value
		'''
		matched = re.search(self.pattern_to_match, stringVal)
		if matched:
			parsed_id = self.fetch_video_id(matched.group())
			self.out.write("%s\n" %parsed_id)

	def fetch_video_id(self, youtube_url):
	    """
	    Extracts the video_id from the url
	    Examples:
	    - http://youtu.be/SA2iWivDJiE
	    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
	    - http://www.youtube.com/embed/SA2iWivDJiE
	    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
	    """
	    query = urlparse(youtube_url)
	    if query.hostname == 'youtu.be':
	        return query.path[1:]
	    if query.hostname in ('www.youtube.com', 'youtube.com'):
	        if query.path == '/watch':
	            p = parse_qs(query.query)
	            return p['v'][0]
	        if query.path[:7] == '/embed/':
	            return query.path.split('/')[2]
	        if query.path[:3] == '/v/':
	            return query.path.split('/')[2]
	    # fail?
	    return None
	def yajl_start_map(self, ctx):
		pass
	def yajl_map_key(self, ctx, stringVal):
		pass
	def yajl_end_map(self, ctx):
		pass
	def yajl_start_array(self, ctx):
		pass
	def yajl_end_array(self, ctx):
		pass

def main():
	# The YajlParser class is responsible for iterating over the JSON document
	# in a streaming fashion.
	parser = YajlParser(ContentHandler())
	parser.allow_multiple_values = True
	try:
		f = open(INPUT_FILE_PATH)
	except IOError:
		print ("Input file does not exist at path %s", INPUT_FILE_PATH)
		return 1
	parser.parse(f=f)
	f.close()

if __name__ == "__main__":
	main()