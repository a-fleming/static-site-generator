import re

from htmlnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if not isinstance(text_node, TextNode):
        raise TypeError("text_node must be a TextNode object")

    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(tag=None, value=text_node.text)

        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)

        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)

        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)

        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})

        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        
        case _:
            raise TypeError("TextNode must have a valid TextType")

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

def split_nodes_bold(old_nodes: list) -> list:
    return split_nodes_of_type(old_nodes, TextType.BOLD)

def split_nodes_italic(old_nodes: list) -> list:
    return split_nodes_of_type(old_nodes, TextType.ITALIC)

def split_nodes_code(old_nodes: list) -> list:
    return split_nodes_of_type(old_nodes, TextType.CODE)

def split_nodes_image(old_nodes: list, verbose=False) -> list:
    return split_nodes_of_type(old_nodes, TextType.IMAGE, verbose)

def split_nodes_link(old_nodes: list, verbose=False) -> list:
    return split_nodes_of_type(old_nodes, TextType.LINK, verbose)

def split_nodes_of_type(old_nodes: list, text_type: TextType, verbose=False) -> list:
    if text_type in [TextType.BOLD, TextType.ITALIC, TextType.CODE]:
        delimiters = {
            TextType.BOLD: "**",
            TextType.ITALIC: "_",
            TextType.CODE: "`",
        }
        return split_nodes_delimiter(old_nodes, delimiters[text_type], text_type)
    
    if text_type not in [TextType.IMAGE, TextType.LINK]:
        return old_nodes

    # Else, splitting TextType.IMAGE or TextType.LINK
    new_nodes = []
    for node in old_nodes:
        if verbose:
            print(f"\nNode: {node}")
        if node.text_type != TextType.PLAIN:
            if verbose:
                print(f"Node's text_type != TextType.PLAIN. Skipping...\n")
            new_nodes.append(node)
            continue

        extraction_functions = {
            TextType.IMAGE: extract_markdown_images_with_indices,
            TextType.LINK: extract_markdown_links_with_indices,
        }
        
        matches = extraction_functions[text_type](node.text)
        if not matches:
            if verbose:
                print(f"No regex matches for {text_type.value} found. Skipping...\n")
            new_nodes.append(node)
            continue
        
        previous_end = 0
        for text, url, start, end in matches:
            leading_text = node.text[previous_end:start]
            if leading_text:
                text_node = TextNode(leading_text, TextType.PLAIN)
                if verbose:
                    print(f"Adding leading text: {text_node}")
                new_nodes.append(text_node)
            new_node = TextNode(text, text_type, url)
            if verbose:
                print(f"Adding {text_type.value}: {new_node}")
            new_nodes.append(new_node)
            previous_end = end
        trailing_text = node.text[previous_end:]
        if trailing_text:
            text_node = TextNode(trailing_text, TextType.PLAIN)
            if verbose:
                print(f"Adding trailing text: {text_node}")
            new_nodes.append(text_node)
    return new_nodes

def extract_markdown_images(text: str) -> list:
    # Takes raw markdown text and returns a list of tuples. Each tuple contains the alt text (if any) and the
    # URL of the markdown images.
    # pattern matches ![alt text](https://www.example.com/path/to/1/image.png)
    # pattern = r"!\[(.*?)\]\((https?:\/\/\w(?:.\w+).*?)\)" # old pattern (doesn't match relative web pages)
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]+)\)" # modified boot.dev's example pattern
    # pttrn = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)" # boot.dev's example pattern
    # TODO: can probably improve the pattern
    return re.findall(pattern, text)

def extract_markdown_images_with_indices(text: str) -> list:
    # pattern = r"!\[(.*?)\]\((https?:\/\/\w(?:.\w+).*?)\)" # old pattern (doesn't match relative web pages)
    num_groups = 2
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]+)\)" # modified boot.dev's example pattern
    # pttrn = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)" # boot.dev's example pattern
    # TODO: can probably improve the pattern
    return extract_pattern_with_start_and_end_indices(pattern, num_groups, text)


def extract_markdown_links(text: str) -> list:
    # Takes raw markdown text and returns a list of tuples. Each tuple contains the anchor text (required) and the
    # URL of the link.
    # pattern matches [anchor text](https://www.example.com/path/to/1/page.html)
    # pattern = r"(?<!!)\[(.+?)\]\((https?:\/\/\w(?:.\w+).*?)\)" # old pattern (doesn't match relative web pages)
    pattern = r"(?<!!)\[([^\[\]]+)\]\(([^\(\)]*)\)" # modified boot.dev's example pattern
    #  ptrn = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)" # boot.dev's example pattern
    # TODO: can probably improve the pattern
    # return re.findall(pattern, text)
    return [(grouping[0], grouping[1]) for grouping in extract_markdown_links_with_indices(text)]

def extract_markdown_links_with_indices(text: str) -> list:
    # pattern = r"(?<!!)\[(.+?)\]\((https?:\/\/\w(?:.\w+).*?)\)" # old pattern (doesn't match relative web pages)
    num_groups = 2
    pattern = r"(?<!!)\[([^\[\]]+)\]\(([^\(\)]*)\)" # modified boot.dev's example pattern
    #  ptrn = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)" # boot.dev's example pattern
    # TODO: can probably improve the pattern
    return extract_pattern_with_start_and_end_indices(pattern, num_groups, text)

def extract_pattern_with_start_and_end_indices(pattern: str, num_groups: int, text: str) -> list:
    matches = re.finditer(pattern, text)
    matches_with_indices = []
    for match in matches:
        grouping = []
        for i in range(1, num_groups + 1):
            grouping.append(match.group(i))
        grouping.append(match.start())
        grouping.append(match.end())
        matches_with_indices.append(tuple(grouping))
    return matches_with_indices

def text_to_text_nodes(text: str) -> list:
    if type(text) != str:
        raise TypeError("Text to convert to TextNodes must be a string.")
    new_nodes = [TextNode(text, TextType.PLAIN)]
    split_functions = [
        split_nodes_bold,
        split_nodes_italic,
        split_nodes_code,
        split_nodes_image,
        split_nodes_link
    ]
    for function in split_functions:
        new_nodes = function(new_nodes)
    return new_nodes

def main():
    plain_node = TextNode("This is text with two `code block` words. `more code stuff`", TextType.PLAIN)
    new_nodes = split_nodes_delimiter([plain_node], "`", TextType.CODE)

    print("new_nodes:\n[")
    for node in new_nodes:
        print(f"\t{node}")
    print("]")

if __name__ == "__main__":
    main()