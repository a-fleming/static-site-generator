import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_text_nodes
)
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):

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
        node_list = [TextNode("**bold** and _italic_", TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(node_list, "**", TextType.BOLD)
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
        node_list = [TextNode("This is `code1``code2` in text", TextType.PLAIN)]
        new_nodes = split_nodes_delimiter(node_list, "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("code1", TextType.CODE),
            TextNode("code2", TextType.CODE),
            TextNode(" in text", TextType.PLAIN),
        ]
        self.assertListEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_delimiter_unrecognized_text_type(self):
        node_list = [TextNode("This is text with a `code block` word", TextType.PLAIN)]
        with self.assertRaises(TypeError):
            new_nodes = split_nodes_delimiter(node_list, "`", "NOT_A_TEXT_TYPE")

    def test_split_nodes_delimiter_unterminated(self):
        node_list = [TextNode("This is `unterminated code block in text", TextType.PLAIN)]
        with self.assertRaises(SyntaxError):
            new_nodes = split_nodes_delimiter(node_list, "`", TextType.CODE)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(matches, expected)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(matches, expected)

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("This is text without any images.")
        self.assertListEqual(matches, [])

    def test_extract_markdown_images_missing_alt_text(self):
        matches = extract_markdown_images(
            "This is text with an ![](https://www.example.com/image.png)"
        )
        expected = [("", "https://www.example.com/image.png")]
        self.assertListEqual(matches, expected)
    
    def test_extract_markdown_images_missing_url(self):
        matches = extract_markdown_images(
            "This is text with an ![image]()"
        )
        self.assertListEqual(matches, [])
    
    def test_extract_markdown_images_no_match_on_link(self):
        matches = extract_markdown_images(
            "This is text with a link [to boot dev](https://www.boot.dev)."
        )
        self.assertListEqual(matches, [])
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)."
        )
        expected = [("to boot dev", "https://www.boot.dev")]
        self.assertListEqual(matches, expected)
    
    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with links [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(matches, expected)
    
    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links(
            "This is text without any links."
        )
        self.assertListEqual(matches, [])
    
    def test_extract_markdown_links_missing_anchor_text(self):
        matches = extract_markdown_links(
            "This is text without a url for the [](https://www.example.com)"
        )
        self.assertListEqual(matches, [])
    
    def test_extract_markdown_links_missing_url(self):
        matches = extract_markdown_images(
            "This is text without a url for the [link]()"
        )
        self.assertListEqual(matches, [])
    
    def test_extract_markdown_links_no_match_on_image(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(matches, [])
    
    def test_split_nodes_image(self):
        node_list = [TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and extra text.",
            TextType.PLAIN,
        )]
        new_nodes = split_nodes_image(node_list)
        expected_nodes = [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and extra text.", TextType.PLAIN),
        ]
        self.assertListEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_image_multiple(self):
        node_list = [TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )]
        new_nodes = split_nodes_image(node_list)
        expected_nodes = [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ]
        self.assertListEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_image_none(self):
        node_list = [TextNode(
            "This is text with no images!",
            TextType.PLAIN,
        )]
        new_nodes = split_nodes_image(node_list)
        self.assertListEqual(new_nodes, node_list)
    
    def test_split_nodes_image_non_plain_text_type(self):
        node_list = [TextNode("`This is a code block`", TextType.CODE)]
        new_nodes = split_nodes_image(node_list)
        self.assertListEqual(new_nodes, node_list)
    
    def test_split_nodes_link(self):
        node_list = [TextNode(
            "This is text with a [link](https://www.boot.dev) and extra text.",
            TextType.PLAIN,
        )]
        new_nodes = split_nodes_link(node_list)
        expected_nodes = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and extra text.", TextType.PLAIN),
        ]
        self.assertListEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_link_multiple(self):
        node_list = [TextNode(
            "This is text with a [link](https://www.boot.dev) and another [second link](https://www.example.com/path/to/1/page.html)",
            TextType.PLAIN,
        )]
        new_nodes = split_nodes_link(node_list)
        expected_nodes = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and another ", TextType.PLAIN),
            TextNode(
                "second link", TextType.LINK, "https://www.example.com/path/to/1/page.html"
            ),
        ]
        self.assertListEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_link_none(self):
        node_list = [TextNode(
            "This is text with no links!",
            TextType.PLAIN,
        )]
        new_nodes = split_nodes_link(node_list)
        self.assertListEqual(new_nodes, node_list)
    
    def test_split_nodes_link_non_plain_text_type(self):
        node_list = [TextNode("`This is a code block`", TextType.CODE)]
        new_nodes = split_nodes_link(node_list)
        self.assertListEqual(new_nodes, node_list)

    def test_text_to_text_nodes_all_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_text_nodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(new_nodes, expected_nodes)
    
    def test_text_to_text_nodes_no_types(self):
        text = "This is plain text."
        new_nodes = text_to_text_nodes(text)
        expected_nodes = [TextNode(text, TextType.PLAIN)]
        self.assertListEqual(new_nodes, expected_nodes)
    
    def test_text_to_text_nodes_empty_str(self):
        text = ""
        new_nodes = text_to_text_nodes(text)
        expected_nodes = [TextNode(text, TextType.PLAIN)]
        self.assertListEqual(new_nodes, expected_nodes)
    
    def test_text_to_text_nodes_non_str(self):
        with self.assertRaises(TypeError):
            new_nodes = text_to_text_nodes(None)


if __name__ == "__main__":
    unittest.main()