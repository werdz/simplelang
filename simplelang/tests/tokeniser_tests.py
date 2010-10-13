from simplelang.tokenisers import Token, tokenise_html
import unittest

_page1 = ("""<html>
<head>
<title>Test page</title>
</head>
<body>
<p>This is a very simple test page.</p>
</body>
</html>""",
	[
		Token("<html>"),
		Token("<head>"),
		Token("<title>"),
		Token("Test"),
		Token("page"),
		Token("</title>"),
		Token("</head>"),
		Token("<body>"),
		Token("<p>"),
		Token("This"), Token("is"), Token("a"), Token("very"), Token("simple"), Token("test"), Token("page"),
		Token("</p>"),
		Token("</body>"),
		Token("</html>")
	])


class TokeniserTests(unittest.TestCase):
	def setUp(self):
		pass
	
	def test_token1(self):
		t = Token("hello")
		self.assertEqual(repr(t), "<simplelang.tokenisers.Token('hello', plain, None, None)>")
	
	def test_token2(self):
		t = Token("<html>")
		self.assertEqual(repr(t), "<simplelang.tokenisers.Token('<html>', html_tag, html, True)>")
	
	def test_token3(self):
		t = Token("</html>")
		self.assertEqual(repr(t), "<simplelang.tokenisers.Token('</html>', html_tag, html, False)>")
	
	def test_token4(self):
		t = Token("<img&lt;")
		self.assertEqual(repr(t), "<simplelang.tokenisers.Token('<img&lt;', plain, None, None)>")
	
	def test_token5(self):
		t = Token("<img src=\"http://www.example.com/image.png\" alt=\"An image! Use this with <img>.\" />")
		self.assertEqual(repr(t), "<simplelang.tokenisers.Token('<img src=\"http://www.example.com/image.png\" alt=\"An image! Use this with <img>.\" />', html_tag, img, True)>")
	
	def test_page1(self):
		generator = tokenise_html(_page1[0])
		l = []
		for x in generator:
			l.append(x)
		
		self.assertEqual(len(l), len(_page1[1]))
		for i in xrange(0, len(l)):
			self.assertEqual(repr(l[i]), repr(_page1[1][i]))

if __name__ == '__main__':
	# allow running from cmd line
	suite = unittest.TestLoader().loadTestsFromTestCase(TokeniserTests)
	unittest.TextTestRunner(verbosity=2).run(suite)
