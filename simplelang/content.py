"""
Things to analyse the content of a tokenised web page
"""
import re

# these tags will be ignored when looking for big large blocks 
_in_content_tags = ['p', 'a', 'img', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'b', 'i', 'u', 'strong', 'ul', 'li', 'pre', 'blockquote', 'em', 'span', 'br']
_common_words = ['about','after','again','air','all','along','also','an','and','another','any','are','around','as','at','away','back','be','because','been','before','below','between','both','but','by','came','can','come','could','day','did','different','do','does','don\'t','down','each','end','even','every','few','find','first','for','found','from','get','give','go','good','great','had','has','have','he','help','her','here','him','his','home','house','how','I','if','in','into','is','it','its','just','know','large','last','left','like','line','little','long','look','made','make','man','many','may','me','men','might','more','most','Mr','must','my','name','never','new','next','no','not','now','number','of','off','old','on','one','only','or','other','our','out','over','own','part','people','place','put','read','right','said','same','saw','say','see','she','should','show','small','so','some','something','sound','still','such','take','tell','than','that','the','them','then','there','these','they','thing','think','this','those','thought','three','through','time','to','together','too','two','under','up','us','use','very','want','water','way','we','well','went','were','what','when','where','which','while','who','why','will','with','word','work','world','would','write','year','you','your','was','a','their','bbc','cop','actually']

script_re = re.compile(r'(?i)^script$')
style_re = re.compile(r'(?i)^style$')
anchor_re = re.compile(r'(?i)^a$')

def is_breaker(tag):
	"""
	Returns true if tag is a breaker. That is, something that wouldn't normally be found in a block of text.
	"""
	return tag.token_type == 'html_tag' and tag.tag_type not in _in_content_tags

def breaker_ratio(page, start_pos=0, end_pos=None):
	"""
	Returns the ratio of breakers to non-breakers in a portion of text.
	"""
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
	"""
	Returns a list of all of the content blocks (areas of text with no major interrupting features) in a page.
	Each block is a list of tokens.
	"""
	blocks = []
	current_block = []
	
	for token in page:
		current_block.append(token)
		if is_breaker(token) or 'script' in token.meta or 'style' in token.meta:
			blocks.append(current_block)
			current_block = []
	return blocks

def classify_block(block, meta_note, block_tag_re):
	"""
	Applies classifications to a block of tokens (block). 
	The classification is applied as a member of the meta dictionary on the relevant Token objects. Classifications are applied to
	tokens between opening and closing tags matching block_tag_re (a compiled regex object).
	"""
	in_js = []
	script_open = False
	
	for i in xrange(0, len(block)):
		if block[i].token_type == 'html_tag' and block_tag_re.match(block[i].tag_type) is not None:
			if block[i].opening_tag is True:
				script_open = True
				in_js.append(i)
			else:
				script_open = False
				for index in in_js:
					block[index].meta[meta_note] = True
				in_js = []
		elif script_open is True:
			in_js.append(i)
	
	return block

def filter_common_words(tokens):
	"""
	Removes the most commonly occurring english words from a piece of text.
	"""
	output = []
	for token in tokens:
		if str(token) not in _common_words:
			output.append(token)
	
	return output

def word_frequencies(tokens):
	"""
	Returns a list of tuples showing the frequency of each word appearing in the tokens list.
	"""
	words = {}
	for token in tokens:
		if token.token_type == 'html_tag':
			continue
		
		if str(token) not in words:
			words[str(token)] = 1
		else:
			words[str(token)] = words[str(token)] + 1
	
	return [(x, words[x]) for x in words.keys()]