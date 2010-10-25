#!/usr/bin/env python

# A script to test things as I write them. Don't pay much attention to it.

import os
import sys
from optparse import OptionParser

from simplelang.tokenisers import tokenise_html
from simplelang.content import *
from simplelang.util import *
def main():
	parser = OptionParser()
	
	parser.add_option('-f', '--file', default='test.html', dest='file', help='the file to test with')
	options, args = parser.parse_args()
	
	f = open(options.file)
	html_data = f.read()
	f.close()
	
	tokenised_page_gen = tokenise_html(html_data)
	tokenised_page = classify_block(list(tokenised_page_gen), 'script', script_re)
	tokenised_page = classify_block(tokenised_page, 'style', style_re)
	tokenised_page = classify_block(tokenised_page, 'a', anchor_re)
	blocks = find_content_blocks(tokenised_page)
	
	sorted_blocks = sorted(blocks, key=len, reverse=True)
	
	print content_block_str(sorted_blocks[0])
	print sorted(word_frequencies(filter_common_words(sorted_blocks[0])), key=lambda x:x[1], reverse=True)

if __name__ == '__main__':
	main()
