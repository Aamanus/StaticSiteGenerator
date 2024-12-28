import os
import shutil

from copystatic import copy_files_recursive
from gencontent import generate_page

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating pages...")
    copy_directory_structure(dir_path_content,dir_path_public)
    #generate_page(
    #    os.path.join(dir_path_content, "index.md"),
    #    template_path,
    #    os.path.join(dir_path_public, "index.html"),
    #)

def copy_directory_structure(src_dir, dest_dir):
    # Ensure the destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Loop through all items in the source directory
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_item = item.replace("md","html")
        dest_path = os.path.join(dest_dir, dest_item)

        # If the item is a directory, recursively copy its structure
        if os.path.isdir(src_path):
            copy_directory_structure(src_path, dest_path)
        else:
            # If the item is a file, read its contents and save to the destination

            generate_page(src_path,template_path,dest_path)



main()
