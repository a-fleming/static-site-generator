import shutil

from pathlib import Path


def copy_directory_recursive(src: str | Path, dest: str | Path, remove_dest: bool=True, verbose: bool = False) -> bool:
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
            copy_directory_recursive(dir_or_file, new_path, False, verbose)
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

