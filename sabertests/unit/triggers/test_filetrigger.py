from saberx.sabercore.triggers.filetrigger import FileTrigger
import os

class TestFileTrigger:

    def create_file(self):
        content = """This function creates a file for
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
        self.create_file()
        
        file_name = "filetrigger.test"

        fileTrigger = FileTrigger(
                        type="FILE_TRIGGER",
                        check="regex",
                        path=file_name,
                        regex="func[a-z]io[mmn]",
                        limit=10,
                        position="head"
                    )

        trigerred, error = fileTrigger.fire_trigger()

        assert trigerred == True
        assert error == None

        fileTrigger = FileTrigger(
                        type="FILE_TRIGGER",
                        check="regex",
                        path=file_name,
                        regex="testing",
                        limit=1,
                        position="head"
                    )

        trigerred, error = fileTrigger.fire_trigger()

        assert trigerred == False
        assert error == None

        fileTrigger = FileTrigger(
                        type="FILE_TRIGGER",
                        check="regex",
                        path=file_name,
                        regex=".*trigger",
                        limit=2,
                        position="tail"
                    )

        trigerred, error = fileTrigger.fire_trigger()

        assert trigerred == True
        assert error == None

        fileTrigger = FileTrigger(
                        type="FILE_TRIGGER",
                        check="regex",
                        path=file_name,
                        regex="dumped",
                        limit=2,
                        position="tail"
                    )

        trigerred, error = fileTrigger.fire_trigger()

        assert trigerred == False
        assert error == None

        self.remove_file(file_name)

    def test_file_presence(self):
        self.create_file()

        file_name = "./filetrigger.test"

        fileTrigger = FileTrigger(
                        type="FILE_TRIGGER",
                        check="present",
                        path=file_name,
                    )

        trigerred, error = fileTrigger.fire_trigger()

        assert trigerred == True
        assert error == None

        self.remove_file(file_name)

    def test_file_absence(self):
        self.create_file()

        fileTrigger = FileTrigger(
                        type="FILE_TRIGGER",
                        check="present",
                        path="/home/travis/invalid.txt",
                    )

        trigerred, error = fileTrigger.fire_trigger()

        assert trigerred == False
        assert error == None
