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
        if len(line) < 2 or line[:2] != "> ":
            return False
    return True

def is_unordered_list_block(block_list: list) -> bool:
    for line in block_list:
        if len(line) < 2 or line[:2] != "- ":
            return False
    return True

def is_ordered_list_block(block_list: list) -> bool:
    for number, line in enumerate(block_list, start=1):
        if len(line) < 3 or line[:3] != f"{number}. ":
            return False
    return True

def markdown_to_blocks(markdown: str) -> list:
    if type(markdown) != str:
        raise TypeError("Markdown must be a string.")
    return [block.strip() for block in markdown.split("\n\n") if block != ""]

def markdown_to_html_node(markdown: str, verbose=True) -> HTMLNode:
    if verbose:
        print(f"markdown:-->{markdown}")
    # create ParentNode (HTMLNode) for entire document; this ParentNode should be a single <div> element
    document_children = [] # need to fill children before we can initialize the ParentNode

    # split markdown into blocks
    blocks = markdown_to_blocks(markdown)
    if verbose:
        print(f"blocks: {blocks}")

    # block_types_to_html_tags = {
    #     BlockType.PARAGRAPH: "p",
    #     BlockType.HEADING: "h",
    #     BlockType.CODE: "code",
    #     BlockType.QUOTE: "blockquote",
    #     BlockType.ULIST: "ul",
    #     BlockType.OLIST: "ol"
    # }

    # for each block
    for block in blocks:
        if verbose:
            print(f"block: {block}")

        # determine BlockType
        block_type = block_to_block_type(block)
        if verbose:
            print(f"block_type: {block_type}")
        if block_type not in [BlockType.PARAGRAPH, BlockType.HEADING]:
            return None
        
        # --- create ParentNode for each block ---

        # # convert text within block into TextNodes of correct type using text_to_text_nodes()
        # block_text_nodes = text_to_text_nodes(block)
        # if verbose:
        #     print(f"block_text_nodes: {block_text_nodes}")

        # # convert TextNodes to LeafNodes using text_node_to_html_node()
        # block_html_nodes = [text_node_to_html_node(text_node) for text_node in block_text_nodes]
        block = remove_unnecessary_whitespace_and_newlines(block)
        if block_type == BlockType.HEADING:
            sections = block.split(" ")
            heading_tag = f"h{sections[0].count("#")}"
            block = " ".join(sections[1:])

        block_html_nodes = text_to_children_html_nodes(block)
        if verbose:
            print(f"block_html_nodes: {block_html_nodes}")

        # add LeafNodes as children of ParentNode for current block
        block_node = None
        match block_type:
            case BlockType.PARAGRAPH:
                block_node = ParentNode(tag="p", children=block_html_nodes)
            case BlockType.HEADING:
                # heading_tag = f"h{block.split(" ")[0].count('#')}"
                block_node = ParentNode(tag=heading_tag, children=block_html_nodes)
            case _:
                raise TypeError(f"Unrecognized BlockType:'{block_type}'")
        if verbose:
            print(f"block_node: {block_node}")

        # add ParentNode to children of the document node
        document_children.append(block_node)
    
    document_node = ParentNode(tag="div", children=document_children)
    if verbose:
        print(f"document_children: {document_children}")
        print(f"document_node:{document_node}")
        print(f"document_node.to_html(): [starts on next line]\n{document_node.to_html()}")
    return document_node

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

