from saberx.sabercore.triggers.tcptrigger import TCPTrigger

class TestTCPTrigger:
    
    def test_non_ssl(self):
        tcpTrigger = TCPTrigger(
            type="TCP_TRIGGER",
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
            type="TCP_TRIGGER",
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
            type="TCP_TRIGGER",
            host="google.com",
            port=80,
            attempts=3,
            threshold=1,
            check="tcp_connect"    
        )

        triggered, error = tcpTrigger.fire_trigger()

        assert triggered == True
        assert error == None

    def test_ssl(self):
        tcpTrigger = TCPTrigger(
            type="TCP_TRIGGER",
            host="127.0.0.1",
            port=80,
            attempts=3,
            threshold=1,
            check="tcp_fail",
            ssl=True
        )

        triggered, error = tcpTrigger.fire_trigger()

        assert triggered == True
        assert error == None

        tcpTrigger = TCPTrigger(
            type="TCP_TRIGGER",
            host="google.com",
            port=443,
            attempts=3,
            threshold=1,
            check="tcp_connect",
            ssl=True
        )

        triggered, error = tcpTrigger.fire_trigger()

        assert triggered == True
        assert error == None
