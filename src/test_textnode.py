import unittest

# from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node

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

    def test_text_node_to_html_node_plain(self):
        text_node = TextNode("Plain text", TextType.PLAIN)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Plain text")

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_text_node_to_html_node_code(self):
        text_node = TextNode("Code text", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code text")

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("Link text", TextType.LINK, "www.example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link text")
        self.assertTrue("href" in html_node.props)
        self.assertEqual(html_node.props["href"], "www.example.com")

    def test_text_node_to_html_node_image(self):
        text_node = TextNode(text="Image text", text_type=TextType.IMAGE, url="www.image-url.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertTrue("src" in html_node.props)
        self.assertEqual(html_node.props["src"], "www.image-url.com")
        self.assertTrue("alt" in html_node.props)
        self.assertEqual(html_node.props["alt"], "Image text")

if __name__ == "__main__":
    unittest.main()