import sys

from copy_static import copy_directory_recursive
from generate_content import generate_pages_recursive

default_basepath = "/"
static_dir_path = "static"
dest_dir_path = "docs" # used for GitHub pages
# dest_dir_path = "public" # used for local hosting
content_dir_path = "content"
template_path = "template.html"

def main():
    basepath = sys.argv[1] if len(sys.argv) >= 2 else default_basepath

    copy_directory_recursive(static_dir_path, dest_dir_path, remove_dest=True, verbose=True)
    
    if generate_pages_recursive(content_dir_path, template_path, dest_dir_path, basepath, verbose=False):
        print(f"Successfully generated page from '{content_dir_path}' to '{dest_dir_path}' using '{template_path}'")
    else:
        print(f"Failed to generate page from '{content_dir_path}' to '{dest_dir_path}' using '{template_path}'")

if __name__ == "__main__":
    main()