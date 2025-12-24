import shutil

from pathlib import Path

from textnode import TextNode, TextType

def main():
    dest = input("Path to dest: ")
    remove_directory_contents(dest, verbose=True)
    
def remove_directory_contents(directory: str | Path, verbose: bool=False) -> bool:
    if not isinstance(directory, (str, Path)):
        if verbose:
            print(f"'{directory}' must be a string or Path object.")
        return False
    path = Path(directory)
    if path.exists():
        if not path.is_dir():
            if verbose:
                print(f"'{path}' is not a directory.")
            return False
        try:
            shutil.rmtree(path)
            if verbose:
                print(f"'{path}' and contents successfully removed.")
        except Exception as e:
            print(f"Error removing '{path}': {e}")
            return False
    elif verbose:
        print(f"'{path}' does not exist.")
    try:
        path.mkdir(parents=True, exist_ok=True)
        if verbose:
            print(f"'{path}' successfully recreated. ")
    except Exception as e:
        print(f"Error recreating '{path}': {e}")
        return False
    return True

if __name__ == "__main__":
    main()