import unittest

from generate_content import extract_title

class TestGenerateContent(unittest.TestCase):
    def test_extract_title(self):
        md = "# This is a header"
        title = extract_title(md)
        expected = "This is a header"
        self.assertEqual(title, expected)
    
    def test_extract_title_not_at_beginning(self):
        md = """
This is some text
And some othe text
That comes before

# The heading

And more text
That comes after
"""

        title = extract_title(md)
        expected = "The heading"
        self.assertEqual(title, expected)
    
    def test_extract_title_multiple_heading_types(self):
        md = """
## Not the title

# The title

###### Also not the title
"""
        title = extract_title(md)
        expected = "The title"
        self.assertEqual(title, expected)

    def test_extract_title_none(self):
        md = "No title here"
        with self.assertRaises(ValueError):
            title = extract_title(md)
    
    def test_extract_title_empty_heading(self):
        md = "# "
        title = extract_title(md)
        expected = ""
        self.assertEqual(title, expected)
    
    def test_extract_title_empty_str(self):
        md = ""
        with self.assertRaises(ValueError):
            title = extract_title(md)

if __name__ == "__main__":
    unittest.main()