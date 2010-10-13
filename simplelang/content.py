"""
Things to analyse the content of a tokenised web page
"""

# these tags will be ignored when looking for big large blocks 
_in_content_tags = ['p', 'a', 'img', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'b', 'i', 'u', 'strong']

def breaker_ratio(page, start_pos=0, end_pos=None):
	if end_pos is None:
		end_pos = len(page)
	
	content_count = 0
	tag_count = 0

	for i in range(start_pos, end_pos):
		if page[i].token_type == 'html_tag' and page[i].tag_type not in _in_content_tags:
			tag_count = tag_count + 1
		else:
			content_count = content_count + 1
	
	return float(tag_count) / float(tag_count + content_count)

