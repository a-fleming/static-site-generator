from enum import Enum


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