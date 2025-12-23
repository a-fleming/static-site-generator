import unittest

from block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)

class TestBlockMarkdown(unittest.TestCase):
    def test_block_to_block_type_paragraph(self):
        block = "This is a \bparagraph block\nwith some text."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_heading(self):
        block = "# This is a heading."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading_h6(self):
        block = "###### This is an h6 heading."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = "```This is a\ncode block\nwith code```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = "> This is a\n> quote block\n> with some text"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block = "- This is an\n- unordered list\n- with items"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ULIST)

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is an\n2. ordered list\n3. with items"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.OLIST)

    def test_block_to_block_type_malformed_heading_missing_space(self):
        block = "#This is a malformed heading."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_malformed_heading_extra_octothorpe(self):
        block = "####### This is a malformed heading."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_malformed_code_bad_start(self):
        block = "``This is a\ncode block\nwith code```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_malformed_code_bad_end(self):
        block = "``This is a\ncode block\nwith code`"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_malformed_quote_missing_space(self):
        block = "> This is a\n>malformed\n- quote block"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    # This test might need to be removed when we no longer split blocks by looking for "\n\n"
    def test_block_to_block_type_malformed_heading_extra_line(self):
        block = "# This is another\n# malformed heading."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_malformed_unordered_list_missing_space(self):
        block = "- This is a\n-malformed\n- unordered list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_malformed_ordered_list_missing_space(self):
        block = "1. This is an\n2.improperly ordered\n3. list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_malformed_ordered_list_not_sequential(self):
        block = "1. This is an\n4. improperly ordered\n3. list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_markdown_to_blocks_single(self):
        md = "This is **bolded** paragraph"
        blocks = markdown_to_blocks(md)
        expected_blocks = ["This is **bolded** paragraph"]
        self.assertListEqual(blocks, expected_blocks)

    def test_markdown_to_blocks_multiple(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items 
"""
        blocks = markdown_to_blocks(md)
        expected_blocks = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertListEqual(blocks, expected_blocks)

    def test_markdown_to_blocks_extra_newlines(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        expected_blocks = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertListEqual(blocks, expected_blocks)
    
    def test_markdown_to_blocks_empty_sty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(blocks, [])

    def test_markdown_to_blocks_non_str(self):
        with self.assertRaises(TypeError):
            blocks = markdown_to_blocks(None)
    
    def test_markdown_to_html_node_paragraph_block_small(self):
        md = """
This is **bolded** paragraph
text in a p
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><p>This is <b>bolded</b> paragraph text in a p</p></div>"
        self.assertEqual(html, expected_html)
    
    def test_markdown_to_html_node_paragraph_block(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(html, expected_html)
    
    def test_markdown_to_html_node_heading_block(self):
        md = """
# h1 heading

## h2 heading

### h3 heading

#### h4 heading

##### h5 heading

###### h6 heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><h1>h1 heading</h1><h2>h2 heading</h2><h3>h3 heading</h3><h4>h4 heading</h4><h5>h5 heading</h5><h6>h6 heading</h6></div>"
        self.assertEqual(html, expected_html)

#     def test_markdown_to_html_node_code_block(self):
#         md = """
# ```
# This is text that _should_ remain
# the **same** even with inline stuff
# ```
# """

#         node = markdown_to_html_node(md)
#         html = node.to_html()
#         expected_html = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
#         self.assertEqual(html, expected_html)
    
    def test_markdown_to_html_node_quote_block(self):
        md = """
> This is a quote block
> with some text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><blockquote>This is a quote block with some text</blockquote></div>"
        self.assertEqual(html, expected_html)

#     def test_markdown_to_html_node_unordered_list_block(self):
#         md = """
# - This is an unordered list
# - with items
# """
#         node = markdown_to_html_node(md)
#         html = node.to_html()
#         expected_html = "<div><ul><li>This is an unordered list</li><li>with items</li></ul></div>"
#         self.assertEqual(html, expected_html)
    
#     def test_markdown_to_html_node_ordered_list_block(self):
#         md = """
# 1. This is an ordered list
# 2. with **bold** items
# """
#         node = markdown_to_html_node(md)
#         html = node.to_html()
#         expected_html = "<div><ol><li>This is an ordered list</li><li>with <b>bold</b> items</li></ol></div>"
#         self.assertEqual(html, expected_html)


if __name__ == "__main__":
    unittest.main()