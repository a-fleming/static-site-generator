import unittest

from block_markdown import markdown_to_blocks

class TestInlineMarkdown(unittest.TestCase):
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