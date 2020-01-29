from saberx.executers.threaddriver import ThreadExecuter
import os


class TestThreadDriver:
    def test_threaddriver(self):

        groups = [
            {
                "groupname": "grp1",
                "actions": [
                    {
                        "actionname": "action_1",
                        "trigger": {
                            "type": "TCP_TRIGGER",
                            "check": "tcp_fail",
                            "host": "127.0.0.1",
                            "port": 8899,
                            "attempts": 3,
                            "threshold": 1
                        },
                        "execute": [
                            "echo test>actionexecuter_test"
                        ]
                    },
                ]
            },
            {
                "groupname": "grp2",
                "actions": [
                    {
                        "actionname": "action_2",
                        "trigger": {
                            "type": "MEMORY_TRIGGER",
                            "attr": "used",
                            "check": "virtual",
                            "threshold": 0.0,
                            "operation": '>='
                        },
                        "execute": [
                            "echo test>actionexecuter_test_2"
                        ]
                    }
                ]
            }
        ]

        threadExecuter = ThreadExecuter(groups=groups)

        status = threadExecuter.spawn_workers("saber.lock")

        assert status

        files = os.listdir(".")

        assert "actionexecuter_test" in files
        assert "actionexecuter_test_2" in files

        with open("actionexecuter_test") as f:
            assert "test" in f.read()

        with open("actionexecuter_test_2") as f:
            assert "test" in f.read()

        os.unlink("actionexecuter_test")
        os.unlink("actionexecuter_test_2")
