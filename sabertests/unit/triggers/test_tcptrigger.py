from saberx.sabercore.triggers.tcptrigger import TCPTrigger

class TestTCPTrigger:
    
    def test_non_ssl(self):
        tcpTrigger = TCPTrigger(
                        host="127.0.0.1",
                        port=5555,
                        attempts=3,
                        threshold=1,
                        check="tcp_fail"    
                    )

        triggered, error = tcpTrigger.fire_trigger()

        assert triggered == True
        assert error == None

        tcpTrigger = TCPTrigger(
                        host="",
                        port=5555,
                        attempts=3,
                        threshold=1,
                        check="tcp_fail"    
                    )

        triggered, error = tcpTrigger.fire_trigger()

        assert triggered == False
        assert error == "IMPROPER_ARGUMENTS"

        tcpTrigger = TCPTrigger(
                        host="google.com",
                        port=80,
                        attempts=3,
                        threshold=1,
                        check="tcp_connect"    
                    )

        triggered, error = tcpTrigger.fire_trigger()

        assert triggered == True
        assert error == None
