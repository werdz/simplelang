def content_block_str(content_block):
	output = ""
	for item in content_block:
		if item.token_type != 'html_tag':
			output = output + str(item) + ' '
	
	return output