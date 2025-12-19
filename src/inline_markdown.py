import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType) -> list:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise SyntaxError(f"unterminated '{delimiter}' delimiter detected")

        if len(sections) < 2: # delimiter not found
            new_nodes.append(node)
            continue

        # iterate through sections; even sections are PLAIN text, odd sections are between delimiters
        for i in range(len(sections)):
            text = sections[i]
            if text == "":
                continue
            if i % 2 == 0:
                plain_node = TextNode(text, TextType.PLAIN)
                new_nodes.append(plain_node)
            else:
                delimited_node = TextNode(text, text_type)
                new_nodes.append(delimited_node)
    return new_nodes

def extract_markdown_images(text: str) -> list:
    # Takes raw markdown text and returns a list of tuples. Each tuple contains the alt text (if any) and the
    # URL of the markdown images.
    # pattern matches ![alt text](https://www.example.com/path/to/1/image.png)
    pattern = r"!\[(.*?)\]\((https?:\/\/\w(?:.\w+).*?)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text: str) -> list:
    # Takes raw markdown text and returns a list of tuples. Each tuple contains the anchor text (required) and the
    # URL of the link.
    # pattern matches [anchor text](https://www.example.com/path/to/1/page.html)
    pattern = r"(?<!\!)\[(.+?)\]\((https?:\/\/\w(?:.\w+).*?)\)"
    return re.findall(pattern, text)
    

def main():
    plain_node = TextNode("This is text with two `code block` words. `more code stuff`", TextType.PLAIN)
    new_nodes = split_nodes_delimiter([plain_node], "`", TextType.CODE)

    print("new_nodes:\n[")
    for node in new_nodes:
        print(f"\t{node}")
    print("]")

if __name__ == "__main__":
    main()