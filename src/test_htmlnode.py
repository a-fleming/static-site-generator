import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_init_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
    
    def test_init_with_values(self):
        node = HTMLNode(tag="div", value="Hello", children=["child1", "child2"], props={"property": "value"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, ["child1", "child2"])
        self.assertEqual(node.props, {"property": "value"})
    
    def test_init_invalid_tag(self):
        with self.assertRaises(TypeError):
            node = HTMLNode(tag=123)
    
    def test_init_invalid_value(self):
        with self.assertRaises(TypeError):
            node = HTMLNode(value=456)
    
    def test_init_invalid_children(self):
        with self.assertRaises(TypeError):
            node = HTMLNode(children="not a list")
    
    def test_init_invalid_props(self):
        with self.assertRaises(TypeError):
            node = HTMLNode(props="not a dict")
    
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

class TestLeafNode(unittest.TestCase):
    def test_init_missing_tag(self):
        with self.assertRaises(TypeError):
            node = LeafNode(value="Some text")

    def test_init_missing_value(self):
        with self.assertRaises(TypeError):
            node = LeafNode(tag="p")
    
    def test_init_value_none(self):
        with self.assertRaises(ValueError):
            node = LeafNode(tag="p", value=None)
    
    def test_init_with_children_keyword(self):
        with self.assertRaises(TypeError):
            node = LeafNode(tag="p", value="Some text", children=None)

            node = LeafNode(tag="p", value="Some text", children=[])
        
        with self.assertRaises(TypeError):
            node = LeafNode(tag="p", value="Some text", children=["child1", "child2"])   
    
    def test_init_with_children_positional(self):
        with self.assertRaises(TypeError):
            node = LeafNode("p", "Some text", None, {"prop": "value"})

        with self.assertRaises(TypeError):
            node = LeafNode("p", "Some text", [], {"prop": "value"})
        
        with self.assertRaises(TypeError):
            node = LeafNode("p", "Some text", ["child1", "child2"], {"prop": "value"})
    
    def test_to_html(self):
        node = LeafNode(tag="span", value="Leaf Node", props={"class": "leaf"})
        expected_html = '<span class="leaf">Leaf Node</span>'
        self.assertEqual(node.to_html(), expected_html)
    
    def test_to_html_no_props(self):
        node = LeafNode(tag="div", value="No Props")
        expected_html = '<div>No Props</div>'
        self.assertEqual(node.to_html(), expected_html)
    
    def test_to_html_raw_text(self):
        node = LeafNode(tag=None, value="Raw text")
        expected_html = 'Raw text'
        self.assertEqual(node.to_html(), expected_html)

class TestParentNode(unittest.TestCase):
    def test_init_missing_tag(self):
        with self.assertRaises(TypeError):
            node = ParentNode(children=["child"])
    
    def test_init_tag_empty(self):
        with self.assertRaises(ValueError):
            node = ParentNode(tag=None, children=["child"])
        
        # with self.assertRaises(ValueError):
        #     node = ParentNode(tag="", children=["child"]) # not sure if empty string should be accepted
    
    def test_init_missing_children(self):
        with self.assertRaises(TypeError):
            node = ParentNode(tag="div")
    
    def test_init_with_value_keyword(self):
        with self.assertRaises(TypeError):
            node = ParentNode(tag="div", children=[], value="Some value")
        
        with self.assertRaises(TypeError):
            node = ParentNode(tag="div", children=[], value=None)
    
    def test_init_with_value_positional(self):
        with self.assertRaises(TypeError):
            node = ParentNode("div", [], "Some value", {"prop": "value"})
        
        with self.assertRaises(TypeError):
            node = ParentNode("div", [], None, {"prop": "value"})
    
    def test_to_html_single_child(self):
        child = LeafNode(tag="p", value="Child 1")
        parent = ParentNode(tag="div", children=[child])
        expected_html = '<div><p>Child 1</p></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_to_html_multiple_children(self):
        child1 = LeafNode(tag="p", value="Child 1")
        child2 = LeafNode(tag="p", value="Child 2", props={"class": "second"})
        parent = ParentNode(tag="div", children=[child1, child2], props={"id": "parent"})
        expected_html = '<div id="parent"><p>Child 1</p><p class="second">Child 2</p></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_to_html_nested_parents(self):
        child1 = LeafNode(tag="span", value="Inner Child")
        inner_parent = ParentNode(tag="div", children=[child1])
        outer_parent = ParentNode(tag="section", children=[inner_parent], props={"class": "outer"})
        expected_html = '<section class="outer"><div><span>Inner Child</span></div></section>'
        self.assertEqual(outer_parent.to_html(), expected_html)


if __name__ == "__main__":
    unittest.main()