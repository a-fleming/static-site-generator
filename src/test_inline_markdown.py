import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType

class TestHelpers(unittest.TestCase):
    def test_split_nodes_delimiter_not_in_text(self):
        node_list = [TextNode("This is text with no delimiters", TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(node_list, "`", TextType.CODE)
        self.assertListEqual(new_nodes, node_list)

    def test_split_nodes_delimiter_bold(self):
        node_list = [TextNode("This is text with a **bold** word", TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(node_list, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_italic(self):
        node_list = [TextNode("This is text with a _italic_ word", TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_code(self):
        node_list = [TextNode("This is text with a `code block` word", TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(node_list, "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertListEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_delimiter_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        expected_nodes = [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
            ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_wrong_text_type(self):
        node_list = [TextNode("This is bold text", TextType.BOLD)]
        new_nodes = split_nodes_delimiter(node_list, "`", TextType.CODE)
        self.assertListEqual(new_nodes, node_list)

    def test_split_nodes_delimiter_multiple_matches(self):
        node_list = [TextNode("This is `code one` and `code two` in text", TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(node_list, "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("code one", TextType.CODE),
            TextNode(" and ", TextType.PLAIN),
            TextNode("code two", TextType.CODE),
            TextNode(" in text", TextType.PLAIN),
        ]
        self.assertListEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_delimiter_adjacent_delimiters(self):
        node_list = [TextNode("This is `` empty code block", TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(node_list, "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is ", TextType.PLAIN),
            TextNode(" empty code block", TextType.PLAIN),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_adjacent_delimited_sections(self):
        print("in split_nodes_delimiter_adjacent_delimited_sections")
        node_list = [TextNode("This is `code1``code2` in text", TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(node_list, "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("code1", TextType.CODE),
            TextNode("code2", TextType.CODE),
            TextNode(" in text", TextType.PLAIN),
        ]
        self.assertListEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_unrecognized_text_type(self):
        node_list = [TextNode("This is text with a `code block` word", TextType.PLAIN)]
        with self.assertRaises(TypeError):
            new_nodes = split_nodes_delimiter(node_list, "`", "NOT_A_TEXT_TYPE")

    
    def test_split_nodes_delimiter_unterminated(self):
        node_list = [TextNode("This is `unterminated code block in text", TextType.PLAIN)]
        with self.assertRaises(SyntaxError):
            new_nodes = split_nodes_delimiter(node_list, "`", TextType.CODE)

if __name__ == "__main__":
    unittest.main()