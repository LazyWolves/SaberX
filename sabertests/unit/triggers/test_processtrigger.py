from saberx.sabercore.triggers.processtrigger import ProcessTrigger


class TestProcessTrigger:

    def test_process_present(self):
        processTrigger = ProcessTrigger(
            type="PROCESS_TRIGER",
            check="cmdline",
            regex=".*init.*",
            count=1,
            operation='>='
        )

        trigered, error = processTrigger.fire_trigger()

        assert trigered
        assert error is None

        processTrigger = ProcessTrigger(
            type="PROCESS_TRIGER",
            check="cmdline",
            regex=".*pytest.*",
            count=2,
            operation='>=',
            negate=True
        )

        trigered, error = processTrigger.fire_trigger()

        assert trigered
        assert error is None
