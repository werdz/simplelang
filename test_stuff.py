#!/usr/bin/env python

# A script to test things as I write them. Don't pay much attention to it.

import os
import sys
from optparse import OptionParser

from simplelang.tokenisers import tokenise_html
from simplelang.content import breaker_ratio, is_breaker, find_content_blocks, classify_script

def main():
	parser = OptionParser()
	
	parser.add_option('-f', '--file', default='test.html', dest='file', help='the file to test with')
	options, args = parser.parse_args()
	
	f = open(options.file)
	html_data = f.read()
	f.close()
	
	tokenised_page_gen = tokenise_html(html_data)
	tokenised_page = classify_script(list(tokenised_page_gen))
	blocks = find_content_blocks(tokenised_page)
	
	sorted_blocks = sorted(blocks, key=len, reverse=True)
	
	
	print [str(x) for x in sorted_blocks[0]]

if __name__ == '__main__':
	main()
