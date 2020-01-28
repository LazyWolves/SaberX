import os
import threading
from saberx.executers.actionexecuter import ActionExecuter


class TestActionExecuter:
    
    def test_action_executer(self):
        
        action = {
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
        }

        status = ActionExecuter.execute_action(
            action=action, 
            thread_lock=threading.Lock())

        assert status == True

        files = os.listdir()

        assert "actionexecuter_test" in files

        with open("actionexecuter_test") as f:
            assert "test" in f.read()

        os.unlink("actionexecuter_test")
    