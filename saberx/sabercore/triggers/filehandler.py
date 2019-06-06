import os

class FileHandler:

    @staticmethod
    def is_present(path):
        if not os.path.exists(path):
            return False, "PATH_DOES_NOT_EXISTS"

        if not os.path.isfile(path):
            return False, "PATH_IS_NOT_A_FILE"

        return True, None

    @staticmethod
    def is_empty(path):
        is_present, error = FileHandler.is_present(path)

        if not is_present:
            return False, error

        if os.stat(path).st_size == 0:
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
            return False, error
