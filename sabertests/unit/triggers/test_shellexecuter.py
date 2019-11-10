import os
from saberx.sabercore.shellexecutor import ShellExecutor

class TestShellExecuter:
    def test_shell_executer_single(self):

        command = "echo test>shelltest"

        shellExecutor = ShellExecutor(command_list="")

        status, output, proc_exit_code = shellExecutor.execute_shell_single(command)

        assert proc_exit_code == 0
        assert status == True

        files = os.listdir("./")

        assert "shelltest" in files

        with open("shelltest") as f:
            testcontent = f.read()

        assert "test" in testcontent

        command = "cat shelltest"

        status, output, proc_exit_code = shellExecutor.execute_shell_single(command)

        assert proc_exit_code == 0
        assert "test" in output
        assert status == True

        command = "cat invalid"

        status, output, proc_exit_code = shellExecutor.execute_shell_single(command)

        assert proc_exit_code != 0
        assert status == False

        os.unlink("./shelltest")
