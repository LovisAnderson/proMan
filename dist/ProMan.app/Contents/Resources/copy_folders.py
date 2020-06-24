import shutil
import os


def copy_directory(src_directory, destination):
    shutil.copytree(src_directory, destination)


def create_empty_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    pass

