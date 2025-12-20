import unittest

from block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks
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

if __name__ == "__main__":
    unittest.main()