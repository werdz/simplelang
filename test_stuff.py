#!/usr/bin/env python

# A script to test things as I write them. Don't pay much attention to it.

import os

from optparse import OptionParser

from simplelang.tokenisers import tokenise_html
from simplelang.content import breaker_ratio

def main():
	parser = OptionParser()
	
	parser.add_option('-f', '--file', default='test.html', dest='file', help='the file to test with')
	options, args = parser.parse_args()
	
	f = open(options.file)
	html_data = f.read()
	f.close()

	print "HTML file contents:"
	print html_data
	print
	
	tok_gen = tokenise_html(html_data)
	page = []
	for tok in tok_gen:
		print repr(tok)
		page.append(tok)

	for i in xrange(0, len(page), 10):
		print "Testing 0 to %i...%f" % (i, breaker_ratio(page, 0, i))
		print "Testing %i to %i...%f" % (len(page) - i, len(page), breaker_ratio(page, len(page) - i, len(page)))

if __name__ == '__main__':
	main()
