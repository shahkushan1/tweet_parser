High Volume JSON Parser Example 
==================================

It's written for Python 2.7.8 and it's based on [YAJL](http://lloyd.github.io/yajl/) and its Python bindings 
[yajl-py](https://pykler.github.io/yajl-py/)


Directory Structure
-------------------
/data
/parser

Installation
------------

These installation instructions are for *Ubuntu 14.04* installed with python 2.7.8.

1. Install ruby and cmake since these form the dependencies for yajl
	`sudo apt-get install ruby cmake`
2. Clone YAJL
	`git clone https://github.com/lloyd/yajl.git`
3. Go to the cloned repo and
	`./configure && make install`
4. You can create a sandboxed virtualenv at this step so that system configuration is not 
disturbed
5. Activate the virtual environment and install yajl-py
	 `pip install yajl-py==2.1.1`
6. Ensure that YAJL and yajl-py are of the same version 2.1.1

How to use it
-------------

Download the [sample data](https://www.dropbox.com/s/wc32q81gxkc8umr/sample_tweets_data.json?dl=00) and store it in */data*

After installing the pre-requisite libraries, you can run the tweet parser by

`python /parser/tweet_parser.py > /data/video_ids.txt`

Instead of storing the complete URLs, the parser only stores the 11 digit Video IDs. Given the Video IDs it is very trivial to construct the URLs by appending *http://www.youtube.com/*. 

Duplicates can be removed by 

`awk '!seen[$0]++' /data/video_ids.txt`