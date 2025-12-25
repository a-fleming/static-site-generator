import shutil

from pathlib import Path

from block_markdown import markdown_to_html_node
from textnode import TextNode, TextType

def main():
    src_dir = "static"
    dest_dir = "public"
    copy_directory_contents(src_dir, dest_dir, remove_dest=True, verbose=True)
    
    from_path = "content/index.md"
    template_path = "template.html"
    dest_path = "public/index.html"
    generate_page(from_path, template_path, dest_path)


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
        if verbose:
            print(f"'{directory}' must be a string or Path object.")
        return False
    path = Path(directory)
    if path.exists():
        if not path.is_dir():
            if verbose:
                print(f"Directory not found at '{path}'.")
            return False
        try:
            shutil.rmtree(path)
            if verbose:
                print(f"Directory '{path}' and contents successfully removed.")
        except Exception as e:
            print(f"Error removing '{path}': {e}")
            return False
    elif verbose:
        print(f"Directory '{path}' does not exist.")
    try:
        path.mkdir(parents=True, exist_ok=True)
        if verbose:
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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'")

    with open(from_path, 'r') as from_file:
        from_content = from_file.read()
    
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()
    
    html = markdown_to_html_node(from_content, verbose=True).to_html()
    title = extract_title(from_content)

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html)

    with open(dest_path, 'w') as dest_file:
        dest_file.write(template_content)


if __name__ == "__main__":
    main()