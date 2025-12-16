import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_init_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
    
    def test_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    def test_props_to_html_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_with_props(self):
        node = HTMLNode(props={"prop1": "val1", "prop2": "val2", "prop3": "val3",})
        expected_html = ' prop1="val1" prop2="val2" prop3="val3"'
        self.assertEqual(node.props_to_html(), expected_html)
    
    def test_repr(self):
        node = HTMLNode(tag="div", value="Hello", children=[], props={"property": "value"})
        expected_repr = "HTMLNode(tag=div, value=Hello, children=[], props={'property': 'value'})"
        self.assertEqual(repr(node), expected_repr)
    
    def test_repr_none_fields(self):
        node = HTMLNode()
        expected_repr = "HTMLNode(tag=None, value=None, children=None, props=None)"
        self.assertEqual(repr(node), expected_repr)


if __name__ == "__main__":
    unittest.main()