import shutil

from pathlib import Path

from block_markdown import markdown_to_html_node
from textnode import TextNode, TextType

def main():
    src_dir = "static"
    dest_dir = "public"
    copy_directory_contents(src_dir, dest_dir, remove_dest=True, verbose=True)
    
    content_path = "content"
    template_path = "template.html"
    dest_path = "public"
    if generate_pages_recursive(content_path, template_path, dest_path, verbose=False):
        print("Successfully generated page from '{content_path}' to '{dest_path}' using '{template_path}'")
    else:
        print(f"Failed to generate page from '{content_path}' to '{dest_path}' using '{template_path}'")

def copy_directory_contents(src: str | Path, dest: str | Path, remove_dest: bool=True, verbose: bool = False) -> bool:
    if verbose:
        print(f"Copying contents of '{src}' to '{dest}'")

    if not isinstance(src, (str, Path)):
        if verbose:
            print(f"src must be a string or Path object.")
        return False
    src_path = Path(src)
    if not isinstance(dest, (str, Path)):
        if verbose:
            print(f"dest must be a string or Path object.")
        return False
    dest_path = Path(dest)

    if remove_dest and not remove_directory_contents(dest_path, verbose):
        return False
    
    for dir_or_file in src_path.iterdir():
        new_path = dest_path / dir_or_file.name
        if dir_or_file.is_dir():
            new_path.mkdir()
            copy_directory_contents(dir_or_file, new_path, False, verbose)
        elif shutil.copy(dir_or_file, dest_path) and verbose:
            print(f"Copied file '{dir_or_file}' to '{new_path}'")
    return True

def remove_directory_contents(directory: str | Path, verbose: bool=False) -> bool:
    if not isinstance(directory, (str, Path)):
        print(f"'{directory}' must be a string or Path object.")
        return False
    path = Path(directory)
    if path.exists():
        if not path.is_dir():
            print(f"Directory not found at '{path}'.")
            return False
        try:
            shutil.rmtree(path)
            if verbose:
                print(f"Directory '{path}' and contents successfully removed.")
        except Exception as e:
            print(f"Error removing '{path}': {e}")
            return False
    else:
        print(f"Directory '{path}' does not exist.")
    try:
        path.mkdir(parents=True, exist_ok=True)
        print(f"Directory '{path}' successfully recreated. ")
    except Exception as e:
        print(f"Error recreating '{path}': {e}")
        return False
    return True

def extract_title(markdown: str):
    sections = markdown.split("\n\n")
    for section in sections:
        if section.startswith("# "):
            return section[2:]
    raise ValueError("Markdown does not contain a header.")

def generate_page(from_path: str | Path, template_path:str | Path, dest_path: str | Path, verbose: bool=False) -> bool:
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

    try:
        with open(dest_path, 'w') as dest_file:
            dest_file.write(template_content)
    except Exception as e:
        print(f"Error writing to '{dest_path}': {e}")
        return False
    return True

def generate_pages_recursive(content_dir_path: str | Path, template_path: str | Path, dest_dir_path: str | Path, verbose=False) -> bool:
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
    
    for dir_or_file in content_dir_path.iterdir():
        if dir_or_file.is_dir():
            new_dir_path = dest_dir_path / dir_or_file.name
            new_dir_path.mkdir()
            print(f"Created new directory: {new_dir_path}")
            if not generate_pages_recursive(dir_or_file, template_path, new_dir_path, verbose):
                return False
        else:
            new_file_path = dest_dir_path / dir_or_file.name.replace("md", "html")
            if not generate_page(dir_or_file, template_path, new_file_path, verbose):
                return False
    return True

if __name__ == "__main__":
    main()