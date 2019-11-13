from saberx.executers.threaddriver import ThreadExecuter

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

        assert status == True
