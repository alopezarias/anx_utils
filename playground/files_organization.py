import os
from typing import Dict, List, TypeVar, Optional

# Take a folder and organize files by extension
# images (png, jpg, jpeg, gif, webp, svg)
    # compressed
    # raw
#  videos (avi, mp4)
    # compressed
    # raw
# music
    # compressed
    # raw
# documents (pdf)
    # pdf
    # python
    # other (docx, doc, txt)
# installers
# ebooks
# compressed (zip, 7zip, rar, tar)
# images of disc (iso, dd)
# others

CategoryT: TypeVar = TypeVar('CategoryT', bound='Category')


class Category(BaseModel):
    extensions: List[str]
    children: Optional[List[CategoryT]] = []
    name: str
    compress: bool = False


class FilesOrganizer:
    categories: List[Category] = []

    def __init__(self, path: str = None, ignore_presets: bool = False) -> None:
        # Check if path exists
        # Check if path is a folder
        # Check if the folder contains files
        # Check if the organizator contains categories
            # if not, print by screen how to add one
            # if yes, offer the posibility of adding new ones
                # by file
                # by code

    def organize(self, compress: bool = False) -> None:
        # check if there are categories
            # if not, show how to add
        # create folder organized
        # iterate over all files, folders and subfolders
        # if a file extension matches the extension:
            # if the folder exists, insert the file over there
            # if not, create it and insert the file
        # end with a successful result

    def add_category(self, path: str = None, category: Category = None) -> None:
        # if path is not none
        # if category is not none
        # if both are none
            # Exception