"""
Things to analyse the content of a tokenised web page
"""
import re

# these tags will be ignored when looking for big large blocks 
_in_content_tags = ['p', 'a', 'img', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'b', 'i', 'u', 'strong', 'ul', 'li', 'pre', 'blockquote']
_script_re = re.compile(r'(?i)script')
_style_re = re.compile(r'(?i)style')

def is_breaker(tag):
	return tag.token_type == 'html_tag' and tag.tag_type not in _in_content_tags

def breaker_ratio(page, start_pos=0, end_pos=None):
	if end_pos is None:
		end_pos = len(page)
	
	content_count = 0
	tag_count = 0

	for i in range(start_pos, end_pos):
		if is_breaker(page[i]):
			tag_count = tag_count + 1
		else:
			content_count = content_count + 1
	
	if tag_count + content_count <= 0:
		return 0.0
	
	return float(tag_count) / float(tag_count + content_count)

def find_content_blocks(page):
	blocks = []
	current_block = []
	for token in page:
		current_block.append(token)
		if is_breaker(token) or 'script' in token.meta:
			blocks.append(current_block)
			current_block = []
	
	return blocks

def classify_script(page):
	in_js = []
	script_open = True
	
	for i in xrange(0, len(page)):
		if page[i].token_type == 'html_tag' and _script_re.match(page[i].tag_type) is not None:
			if page[i].opening_tag is True:
				script_open = True
			else:
				script_open = False
				for index in in_js:
					page[i].meta['script'] = True
				in_js = []
		elif script_open is True:
			in_js.append(i)			
	
	return page