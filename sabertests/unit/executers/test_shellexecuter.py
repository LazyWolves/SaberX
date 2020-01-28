import os
from saberx.sabercore.shellexecutor import ShellExecutor


class TestShellExecuter:
    def test_shell_executer_single(self):

        command = "echo test>shelltest"

        shellExecutor = ShellExecutor(command_list="")

        status, output, proc_exit_code = \
            shellExecutor.execute_shell_single(command)

        assert proc_exit_code == 0
        assert status == True

        files = os.listdir("./")

        assert "shelltest" in files

        with open("shelltest") as f:
            testcontent = f.read()

        assert "test" in testcontent

        command = "cat shelltest"

        status, output, proc_exit_code = \
            shellExecutor.execute_shell_single(command)

        assert proc_exit_code == 0
        assert "test" in output
        assert status == True

        command = "cat invalid"

        status, output, proc_exit_code = \
            shellExecutor.execute_shell_single(command)

        assert proc_exit_code != 0
        assert status == False

        os.unlink("./shelltest")

    def test_shell_executer_list(self):

        command_list = [
            "echo test>shelltest",
            "echo test2>shelltest2"
        ]

        shellExecutor = ShellExecutor(command_list=command_list)

        status = shellExecutor.execute_shell_list()

        assert status == True

        files = os.listdir("./")

        assert "shelltest" in files
        assert "shelltest2" in files

        os.unlink("shelltest")
        os.unlink("shelltest2")

        command_list = [
            "cat invalid",
            "echo test>shelltest"
        ]

        shellExecutor = ShellExecutor(command_list=command_list)

        status = shellExecutor.execute_shell_list()

        assert status == False

        files = os.listdir("./")

        assert "shelltest" not in files
