import os
from itertools import islice
import re

class FileHandler:

    @staticmethod
    def is_present(path):
        if not os.path.exists(path):
            return False, None

        if not os.path.isfile(path):
            return False, None

        return True, None

    @staticmethod
    def is_empty(path):
        is_present, error = FileHandler.is_present(path)

        if not is_present:
            return False, "FILE_DOES_NOT_EXISTS"

        if os.stat(path).st_size == 0:
            return True, None

        return False, None

    @staticmethod
    def read_from_head(path, regex, limit):
        pattern = re.compile(regex)
        with open(path) as file:
            for row in islice(file, 0, limit):
                text = row.strip()
                if pattern.search(text):
                    return True, None

        return False, None


    @staticmethod
    def search_keyword(**kwargs):
        path = kwargs.get("path")
        regex = kwargs.get("regex")
        limit = kwargs.get("limit")
        position = kwargs.get("position")

        is_present, error = FileHandler.is_present(path)

        if not is_present:
            return False, "FILE_DOES_NOT_EXISTS"

if __name__ == "__main__":
    FileHandler.read_from_head("filetrigger.py", '.*', 100)
