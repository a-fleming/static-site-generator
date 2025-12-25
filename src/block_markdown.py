from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_node_to_html_node, text_to_text_nodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    if is_code_block(block):
        return BlockType.CODE
    
    block_lines = block.split("\n")
    if is_heading_block(block_lines):
        return BlockType.HEADING
    if is_quote_block(block_lines):
        return BlockType.QUOTE
    if is_unordered_list_block(block_lines):
        return BlockType.ULIST
    if is_ordered_list_block(block_lines):
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def is_code_block(block: str) -> bool:
    if len(block) > 6 and block[:3] == block[-3:] == "```":
        return True
    return False

def is_heading_block(block_list: list) -> bool:
    if len(block_list) != 1:
        return False
    words = block_list[0].split(" ")
    if len(words) < 2:
        return False
    lead_chars = words[0]
    if len(lead_chars) < 1 or len(lead_chars) > 6:
        return False
    
    for i in range(len(lead_chars)):
        if lead_chars[i] != "#":
            return False
    return True

def is_quote_block(block_list: list) -> bool:
    for line in block_list:
        if not line.startswith(">"):
        # if len(line) < 2 or line[:2] != "> ":
            return False
    return True

def is_unordered_list_block(block_list: list) -> bool:
    for line in block_list:
        if len(line) < 2 or line[:2] != "- ":
            return False
    return True

def is_ordered_list_block(block_list: list) -> bool:
    for number, line in enumerate(block_list, start=1):
        if not line.startswith(f"{number}. "):
            return False
    return True

def markdown_to_blocks(markdown: str) -> list:
    if type(markdown) != str:
        raise TypeError("Markdown must be a string.")
    return [block.strip() for block in markdown.split("\n\n") if block != ""]

def markdown_to_html_node(markdown: str, verbose=False) -> HTMLNode:
    if verbose:
        print(f"markdown:-->{markdown}")
    # create ParentNode (HTMLNode) for entire document; this ParentNode should be a single <div> element
    document_children = [] # need to fill children before we can initialize the ParentNode

    # split markdown into blocks
    blocks = markdown_to_blocks(markdown)
    if verbose:
        print(f"blocks: {blocks}")

    # for each block
    for block in blocks:
        # Convert block to HTMLNode
        block_node = block_to_html_node(block, verbose)
        # Add ParentNode to children of the document node
        document_children.append(block_node)
       
    document_node = ParentNode(tag="div", children=document_children)
    if verbose:
        print(f"document_children: {document_children}")
        print(f"document_node:{document_node}")
        print(f"document_node.to_html(): [starts on next line]\n{document_node.to_html()}")
    return document_node

def block_to_html_node(block, verbose=False):
    if verbose:
        print(f"block: {block}")
    # determine BlockType
    block_type = block_to_block_type(block)
    if verbose:
        print(f"block_type: {block_type}")
    
    match block_type:
        case BlockType.PARAGRAPH:
            block_node = paragraph_to_html_node(block)
        case BlockType.HEADING:
            block_node = heading_to_html_node(block)
        case BlockType.CODE:
            block_node = code_to_html_node(block)
        case BlockType.QUOTE:
            block_node = quote_to_html_node(block)
        case BlockType.ULIST:
            block_node = ulist_to_html_node(block)
        case BlockType.OLIST:
            block_node = olist_to_html_node(block)
        case _:
            raise TypeError(f"Unrecognized BlockType:'{block_type}'")
    if verbose:
        print(f"block_node: {block_node}")
    return block_node

def paragraph_to_html_node(block: str) -> HTMLNode:
    block = remove_unnecessary_whitespace_and_newlines(block)
    block_tag = "p"
    block_html_nodes = text_to_children_html_nodes(block)
    return ParentNode(tag=block_tag, children=block_html_nodes)

def heading_to_html_node(block: str) -> HTMLNode:
    block = remove_unnecessary_whitespace_and_newlines(block)
    sections = block.split(" ")
    # Determine heading level
    block_tag = f"h{sections[0].count("#")}"
    # Remove leading "#"s and single space
    block = " ".join(sections[1:])
    block_html_nodes = text_to_children_html_nodes(block)
    return ParentNode(tag=block_tag, children=block_html_nodes)

def code_to_html_node(block: str) -> HTMLNode:
    # Strip leading triple backticks and newlines, and trailing backticks (not newlines) 
    block = block[4:-3]
    # Leave the text within the block unconverted
    plain_text_node = LeafNode(tag=None, value=block)
    # Wrap the text in a <code> tag
    code_node = ParentNode(tag="code", children=[plain_text_node])
    # Wrap the <code> element with <pre> tags
    return ParentNode(tag="pre", children=[code_node])

def quote_to_html_node(block: str) -> HTMLNode:
    block = remove_unnecessary_whitespace_and_newlines(block)
    block = block.replace("> ", "")
    block_html_nodes = text_to_children_html_nodes(block)
    return ParentNode(tag="blockquote", children=block_html_nodes)

def ulist_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    # Remove leading "- " each line
    lines = [line[2:] for line in lines]
    # Wrap each line in an <li> tag
    block_html_nodes = [ParentNode(tag="li", children=text_to_children_html_nodes(line)) for line in lines]
    # Wrap entire block in a <ul> tag
    return ParentNode(tag="ul", children=block_html_nodes)

def olist_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    # Remove the leading number, decimal point, and space from each line
    lines = [". ".join(line.split(". ")[1:]) for line in lines]
    # Wrap each line in an <li> tag
    block_html_nodes = [ParentNode(tag="li", children=text_to_children_html_nodes(line)) for line in lines]
    # Wrap entire block in an <ol> tag
    return ParentNode(tag="ol", children=block_html_nodes)

def text_to_children_html_nodes(block: str, verbose=False) -> list:
    # convert text within block into TextNodes of correct type using text_to_text_nodes()
    block_text_nodes = text_to_text_nodes(block)
    if verbose:
        print(f"block_text_nodes: {block_text_nodes}")
    # convert TextNodes to LeafNodes using text_node_to_html_node()
    block_html_nodes = [text_node_to_html_node(text_node) for text_node in block_text_nodes]
    return block_html_nodes

def remove_unnecessary_whitespace_and_newlines(text: str) -> str:
    return " ".join(text.split())

