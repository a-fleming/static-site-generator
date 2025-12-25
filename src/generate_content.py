from pathlib import Path

from block_markdown import markdown_to_html_node

def extract_title(markdown: str):
    sections = markdown.split("\n\n")
    for section in sections:
        if section.startswith("# "):
            return section[2:]
    raise ValueError("Markdown does not contain a header.")

def generate_page(from_path: str | Path, template_path:str | Path, dest_path: str | Path, basepath: str | Path, verbose: bool=False) -> bool:
    if not isinstance(from_path, (str, Path)):
        print(f"from_path must be a string or Path object.")
        return False
    from_path = Path(from_path)
    if not isinstance(template_path, (str, Path)):
        print(f"template_path must be a string or Path object.")
        return False
    template_path = Path(template_path)
    if not isinstance(dest_path, (str, Path)):
        print(f"dest_path must be a string or Path object.")
        return False
    dest_path = Path(dest_path)
    if not isinstance(basepath, (str, Path)):
        print(f"basepath must be a string or Path object.")
        return False
    basepath = Path(basepath)

    print(f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'")

    try:
        with open(from_path, 'r') as from_file:
            from_content = from_file.read()
    except FileNotFoundError as fnfe:
        print(f"Source file '{from_path}' not found.")
        return False
    
    try:
        with open(template_path, 'r') as template_file:
            template_content = template_file.read()
    except FileNotFoundError as fnfe:
        print(f"Template file '{template_path}' not found.")
        return False
    
    html = markdown_to_html_node(from_content, verbose).to_html()
    title = extract_title(from_content)

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html)
    template_content = template_content.replace('href="/', f'href="{basepath}/')
    template_content = template_content.replace('src="/', f'src="{basepath}/')

    try:
        with open(dest_path, 'w') as dest_file:
            dest_file.write(template_content)
    except Exception as e:
        print(f"Error writing to '{dest_path}': {e}")
        return False
    return True

def generate_pages_recursive(content_dir_path: str | Path, template_path: str | Path, dest_dir_path: str | Path, basepath: str| Path, verbose=False) -> bool:
    if not isinstance(content_dir_path, (str, Path)):
        print(f"content_dir_path must be a string or Path object.")
        return False
    content_dir_path = Path(content_dir_path)
    if not isinstance(template_path, (str, Path)):
        print(f"template_path must be a string or Path object.")
        return False
    template_path = Path(template_path)
    if not isinstance(dest_dir_path, (str, Path)):
        print(f"dest_dir_path must be a string or Path object.")
        return False
    dest_dir_path = Path(dest_dir_path)
    if not isinstance(basepath, (str, Path)):
        print(f"basepath must be a string or Path object.")
        return False
    basepath = Path(basepath)
    
    for dir_or_file in content_dir_path.iterdir():
        if dir_or_file.is_dir():
            new_dir_path = dest_dir_path / dir_or_file.name
            new_dir_path.mkdir()
            print(f"Created new directory: {new_dir_path}")
            if not generate_pages_recursive(dir_or_file, template_path, new_dir_path, basepath, verbose):
                return False
        else:
            new_file_path = dest_dir_path / dir_or_file.name.replace("md", "html")
            if not generate_page(dir_or_file, template_path, new_file_path, basepath, verbose):
                return False
    return True