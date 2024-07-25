import json
import os
from os import listdir, makedirs
from os.path import exists as path_exists, isdir as path_isdir, join as join_path
from typing import Dict, List, TypeVar, Optional, Tuple
from pydantic import BaseModel
from shutil import copyfile
from pathlib import Path

CategoryT: TypeVar = TypeVar('CategoryT', bound='Category')


class Category(BaseModel):
    extensions: List[str]
    children: Optional[List[CategoryT]] = []
    name: str
    compress: bool = False


class CustomList(List):
    def remove_list(self, items: List[str]) -> List[str]:
        for item in items:
            self.remove(item)
        return items

    def append_list(self, items: List[str]) -> List[str]:
        for item in items:
            self.append(item)
        return items


class FilesOrganizer:
    categories: List[Category] = []
    __preset_categories: str = 'C:/Users/anglo/Documents/github/anx_utils/playground/file_categories.json'
    __path: str = None
    __dest_path: str = None

    def __init__(self, path: str = None, ignore_presets: bool = False) -> None:
        # Check if path exists
        if not path_exists(path):
            raise Exception(f'Path does not exist {path}')

        # Check if path is a folder
        if not path_isdir(path):
            raise Exception(f'Path is not a directory {path}')

        # Check if the folder contains files
        if not len(listdir(path)):
            raise Exception(f'Path does not contain files {path}')

        self.__path = path

        # Add preset categories
        if not ignore_presets:
            self.add_categories(path=self.__preset_categories)

        # Check if the organizer contains categories
        if not self.has_categories():
            raise Exception(f'FilesOrganizer does not have categories. Add them')

    def organize(self, compress: bool = False) -> None:
        # check if there are categories
        # if not, show how to add
        if not self.has_categories():
            raise Exception('There are no categories')

        # create folder organized
        self.__dest_path = join_path(self.__path, 'organized')
        makedirs(self.__dest_path, exist_ok=True)

        # iterate over all files, folders and subfolders
        files: List[str] = []
        for root, dirs, files_path in os.walk(self.__path):
            for file in files_path:
                files.append(os.path.join(root, file))

        # if a file extension matches the extension:
        for category in self.categories:
            files = self.move_files(category=category, files=files)

        # if there are files left, they will be inserted in other
        if len(files):
            other_path: str = join_path(self.__dest_path, 'other')
            makedirs(other_path, exist_ok=True)
            self.copy_files(files=files, destination=other_path)

        # end with a successful result
        print(f'Finished organizer at {self.__path}')

    @staticmethod
    def copy_files(files: List[str], destination: str) -> None:
        for file_to_copy in files:
            copyfile(src=file_to_copy, dst=join_path(destination, Path(file_to_copy).name))

    def move_files(self, category: Category, files: List[str], parent: str = None) -> List[str]:
        # filter files by extensions
        filtered_files: List[str]
        filtered_files, files = self.filter_files(files=files, extensions=category.extensions)

        # if the folder exists, insert the file over there
        if len(filtered_files):
            destination_path: str = join_path(self.__dest_path, parent) if parent is not None else self.__dest_path
            destination_path = join_path(destination_path, category.name)
            if not path_exists(destination_path):
                makedirs(destination_path, exist_ok=True)

            self.copy_files(files=filtered_files, destination=destination_path)

            # Iterate by children
            for child in category.children:
                parent_path: str = join_path(parent, category.name) if parent is not None else category.name
                files = self.move_files(category=child, files=files, parent=parent_path)
        return files

    @staticmethod
    def filter_files(files: List[str], extensions: List[str]) -> Tuple[List[str], List[str]]:
        files: CustomList[str] = CustomList(files)
        filtered: CustomList[str] = CustomList()
        for extension in extensions:
            filtered_files: List[str] = list(filter(lambda x: x.endswith(extension), files))
            files.remove_list(filtered_files)
            filtered.append_list(filtered_files)
        return filtered, files

    def add_category(self, category: Category = None) -> None:
        if category is None:
            raise Exception('Cannot add None category')
        self.categories.append(category)

    def add_categories(self, path: str = None, categories: List[Category] = None):
        if path is None and (categories is None or not len(categories)):
            raise Exception('There is no category to add')

        if path is not None:
            with open(path) as json_file:
                presets: List[Dict] = json.load(json_file)
                for preset in presets:
                    self.add_category(category=Category(**preset))
        if categories is not None and len(categories):
            for category in categories:
                self.add_category(category=category)

    def has_categories(self) -> bool:
        return len(self.categories) != 0


organizer: FilesOrganizer = FilesOrganizer(path='C:/Users/anglo/Desktop')
organizer.organize()
