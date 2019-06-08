import os
from itertools import islice
import re
import traceback

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

        if not is_present(path):
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
    def read_from_tail(path, regex, lines):
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
        path = kwargs.get("path")
        regex = kwargs.get("regex")
        limit = kwargs.get("limit")
        position = kwargs.get("position")

        is_present, error = FileHandler.is_present(path)

        if not is_present(path):
            return False, "FILE_DOES_NOT_EXISTS"

        if is_empty(path):
            return False, None

        if position == "head":
            return read_from_head(path, regex, lines)
        else:
            return read_from_tail(path, regex, lines)

if __name__ == "__main__":
    FileHandler.read_from_tail("filetrigger.py", '.*', 10)
