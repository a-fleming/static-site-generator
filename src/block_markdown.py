def markdown_to_blocks(text: str) -> list:
    if type(text) != str:
        raise TypeError("Markdown text must be a string.")
    return [block.strip() for block in text.split("\n\n") if block != ""]