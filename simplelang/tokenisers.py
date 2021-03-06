"""
Tokenisers that form part of the simplelang package.
"""
import re

_bangtag_regex = re.compile(r'^<!')
_tag_regex = re.compile(r'^</?([a-zA-Z0-9]+).*?/?>$')
_entity_regex = re.compile(r'^&([a-zA-Z]+|#[0-9]+);$')
_closing_tag_regex = re.compile(r'^</')
_empty_space_re = re.compile(r'^[ ,.\r\t\n]*$')
_
class Token:
	def __init__(self, value):
		g = _tag_regex.match(value)
		if g is not None:
			self.token_type = 'html_tag'
			self.tag_type = g.group(1)
			if _closing_tag_regex.match(value):
				self.opening_tag = False
			else:
				self.opening_tag = True
		else:
			self.token_type = 'plain'
			self.tag_type = None
			self.opening_tag = None
		
		self.value = value
		self.meta = {}
	
	def __str__(self):
		return self.value
	
	def __repr__(self):
		return "<simplelang.tokenisers.Token('%s', %s, %s, %s)>" % (self.value, self.token_type, self.tag_type, self.opening_tag)

def tokenise_html(raw_html):
	"""
	A sequence object that splits a HTML file into a stream of tokens.
	Doesn't have to be a perfectly formed HTML file.
	"""
	
	in_tag = False
	in_tag_dquote = False
	in_tag_squote = False
	in_entity = False
	token = ''
	
	separators = [" ", "\n", ".", ","]
	
	for i in xrange(0, len(raw_html)):
		if raw_html[i] in separators and _empty_space_re.match(token) is None and not in_tag:
			yield Token(token)
			token = ''
		elif in_tag:
			if not in_tag_dquote and not in_tag_squote and raw_html[i] == '>':
				token = token + raw_html[i]
				yield Token(token)
				token = ''
				in_tag = False
			elif in_tag_dquote and raw_html[i] == '"':
				token = token + raw_html[i]
				in_tag_dquote = False
			elif in_tag_squote and raw_html[i] == '\'':
				token = token + raw_html[i]
				in_tag_squote = False
			elif not in_tag_dquote and not in_tag_squote and raw_html[i] == '\'':
				token = token + raw_html[i]
				in_tag_squote = True
			elif not in_tag_dquote and not in_tag_squote and raw_html[i] == '"':
				token = token + raw_html[i]
				in_tag_dquote = True
			else:
				token = token + raw_html[i]
		else:
			if raw_html[i] == '<':
				# new token
				# yield the old one
				if _empty_space_re.match(token) is None:
					yield Token(token)
				
				token = raw_html[i]
				in_tag = True
			else:
				token = token + raw_html[i]

