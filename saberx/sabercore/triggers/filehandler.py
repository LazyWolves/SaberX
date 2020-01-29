"""
.. module:: filehandler
   :synopsis: Module to evaluate file trigger
"""

import os
from itertools import islice
import re


class FileHandler:

    """
        ** Class containing file handling methods **
    """

    @staticmethod
    def is_present(path):

        """
            **Method for checking if the given file exists**

            This method checks whether the given path is valid or not.

            Args:
                path (string): path to the file resource

            Returns:
                bool, string: status, error if any

        """
        if not os.path.exists(path):
            return False, None

        if not os.path.isfile(path):
            return False, None

        return True, None

    @staticmethod
    def is_empty(path):

        """
            **Method for checking if given file is empty**

            Args:
                path (string): path to the file resource

            Returns:
                bool, string: status, error if any
        """
        if os.stat(path).st_size == 0:
            return True, None

        return False, None

    @staticmethod
    def read_from_head(path, regex, limit):

        """
            **Method to read a file from head and see if pattern exists**

            This method reads a given file and checks if the given pattern
            exists in the top 'n' lines where n is given as 'limits'.

            Args:
                path (string): path to the file resource
                regex (string): string representing the pattern to search for
                limit (Integer): Number of lines to query

            Returns:
                bool, string: status , error
        """
        pattern = re.compile(regex)
        with open(path) as file:
            for row in islice(file, 0, limit):
                text = row.strip()
                if pattern.search(text):
                    return True, None

        return False, None

    @staticmethod
    def read_from_tail(path, regex, lines):

        """
            **Method to read a file from end and see if pattern exists**

            This method reads a given file and checks if the given pattern
            exists in the last 'n' lines where n is given as 'lines'.

            Args:
                path (string): path to the file resource
                regex (string): string representing the pattern to search for
                limit (Integer): Number of lines to query

            Returns:
                bool, string: status , error
        """
        pattern = re.compile(regex)

        lines_found = []
        block_counter = -1
        _buffer = min(4096, os.stat(path).st_size)

        with open(path, 'rb') as f:
            while len(lines_found) <= lines:
                try:
                    f.seek(block_counter * _buffer, os.SEEK_END)
                except IOError:
                    f.seek(0)
                    lines_found = f.readlines()
                    break

                lines_found = f.readlines()
                block_counter -= 1

        lines_found = lines_found[-lines:]

        for line in lines_found:
            text = line.decode().strip()
            if pattern.search(text):
                return True, None

        return False, None

    @staticmethod
    def search_keyword(**kwargs):

        """
            **Method to execute the file operation**

            Method to perform the reuired file operations to
            execute the trigger

            Args:
                kwargs (dict): Dict containing path, pattern, limit and
                position to read the file from

            Returns:
                bool, string: status, error if any
        """
        path = kwargs.get("path")
        regex = kwargs.get("regex")
        limit = kwargs.get("limit")
        position = kwargs.get("position")

        # First of all, check if the file resource exists
        is_present, error = FileHandler.is_present(path)

        if not is_present:
            return False, "FILE_DOES_NOT_EXISTS"

        # Next, check if the file is empty
        is_empty, error = FileHandler.is_empty(path)

        if is_empty:
            return False, None

        if position == "head":
            return FileHandler.read_from_head(path, regex, limit)
        else:
            return FileHandler.read_from_tail(path, regex, limit)


if __name__ == "__main__":
    FileHandler.read_from_tail("filetrigger.py", '.*', 10)
