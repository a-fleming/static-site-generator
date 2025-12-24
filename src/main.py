import shutil

from pathlib import Path

from textnode import TextNode, TextType

def main():
    src = "static"
    dest = "public"
    copy_directory_contents(src, dest, remove_dest=True, verbose=True)

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

if __name__ == "__main__":
    main()