from saberx.sabercore.triggers.memorytrigger import MemoryTrigger
import os

class TestFileTrigger:

    def create_file(self):
        content = """
                    This function creates a file for
                    testing file trigger. This string will be
                    dumped in a file. The file will then be passed as
                    a parameter to file trigger to test the read from head
                    and read from tail features with limit.
                  """

        with open("filetrigger.test", "w") as f:
            f.write(content)

    def remove_file(self, filename):
        os.unlink(filename)

    def test_filetrigger(self):
        
        file_name = "filetrigger.test"
