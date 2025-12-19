import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_init_invalid_text_type(self):
        with self.assertRaises(TypeError):
            node = TextNode("This is a text node", "Invalid TextType")

    def test_eq_true(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        node2 = TextNode("This is a text node", TextType.PLAIN)
        self.assertEqual(node, node2)
    
    def test_eq_true_with_url(self):
        node = TextNode("This is a link", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a link", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)
    
    def test_eq_true_none_url(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        node2 = TextNode("This is a text node", TextType.PLAIN, None)
        self.assertEqual(node, node2)
    
    def test_eq_false_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        node2 = TextNode("This is a different text node", TextType.PLAIN)
        self.assertNotEqual(node, node2)
    
    def test_eq_false_text_type(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_eq_false_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://different.com")
        self.assertNotEqual(node, node2)
    
    def test_eq_false_non_textnode(self):
         node = TextNode("This is a text node", TextType.PLAIN)
         self.assertNotEqual(node, "not a text node")

    def test_repr(self):
        node = TextNode("Sample text", TextType.ITALIC, "https://example.com")
        expected_repr = "TextNode(Sample text, TextType.ITALIC, https://example.com)"
        self.assertEqual(repr(node), expected_repr)
    
    def test_repr_none_url(self):
        node = TextNode("Sample text", TextType.CODE)
        expected_repr = "TextNode(Sample text, TextType.CODE, None)"
        self.assertEqual(repr(node), expected_repr)

if __name__ == "__main__":
    unittest.main()