import os
from os import path as osp
import argparse
from glob import glob
import random

def rename_files_in_folder(folder_path):
    # Get the list of all files in the folder using glob
    file_list = glob(osp.join(folder_path, '*'))

    # Filter out directories and keep only files
    files_only = [f for f in file_list if osp.isfile(f)]

    # Shuffle the list of files randomly
    random.shuffle(files_only)

    # Rename each file with a sequential number followed by its original extension
    for idx, old_file_path in enumerate(files_only):
        # Get the directory and file name from the path
        dir_name, file_name = osp.split(old_file_path)

        # Split the file name into name and extension
        _, file_extension = osp.splitext(file_name)

        # Create a new file name with sequential number and original extension
        new_file_name = f"{idx+1}{file_extension}"
        new_file_path = osp.join(dir_name, new_file_name)

        # Rename the file
        os.rename(old_file_path, new_file_path)
        print(f"Renamed '{old_file_path}' to '{new_file_path}'")


if __name__ == "__main__":
    # Specify the folder path where you want to rename files
    parser = argparse.ArgumentParser()
    parser.add_argument('--src_dir', type=str, required=True, help='Path to source directory')
    
    args = parser.parse_args()

    # Call the function to rename files in the specified folder
    rename_files_in_folder(args.src_dir)