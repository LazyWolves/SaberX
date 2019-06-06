import os

class FileHandler:

    @staticmethod
    def is_present(path):
        if not os.path.exists(path):
            return False, "PATH_DOES_NOT_EXISTS"

        if not os.path.isfile(path):
            return False, "PATH_IS_NOT_A_FILE"

        return True
