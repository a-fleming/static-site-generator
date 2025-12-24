import os
import shutil

from textnode import TextNode, TextType

def main():
    dir_to_delete = input("Path to dir: ")
    if not dir_to_delete.startswith("/"):
        dir_to_delete = os.path.join(os.getcwd(), dir_to_delete)
    
    remove_directory_contents(dir_to_delete, verbose=True)

def remove_directory_contents(path: str | bytes |os.PathLike, verbose=False) -> bool:
    if not os.path.exists(path):
        if verbose:
            print(f"{path} does not exist.")
        return False
    if not os.path.isdir(path):
        if verbose:
            print(f"{path} is not a directory.")
        return False
    try:
        shutil.rmtree(path)
        if verbose:
            print(f"{path} and contents successfully removed.")
    except Exception as e:
        print(f"Error removing {path}: {e}")
        return False
    try:
        os.mkdir(path)
        if verbose:
            print(f"{path} successfully recreated. ")
    except Exception as e:
        print(f"Error recreating {path}: {e}")
        return False
    return True

if __name__ == "__main__":
    main()