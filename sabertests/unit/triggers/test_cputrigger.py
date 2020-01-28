from saberx.sabercore.triggers.cputrigger import CPUTrigger

class TestCPUTrigger:

    def test_cputrigger(self):
        cpuTrigger = CPUTrigger(
            type="CPU_TRIGGER",
            check="loadaverage",
            operation=">=",
            threshold=[0.0, 0.0, 0.0]
        )

        trigerred, error = cpuTrigger.fire_trigger()

        assert trigerred == True
        assert error == None

        cpuTrigger = CPUTrigger(
            type="CPU_TRIGGER",
            check="loadaverage",
            operation=">=",
            threshold=["invalid", 0.0, 0.0]
        )

        trigerred, error = cpuTrigger.fire_trigger()

        assert trigerred == False
        assert error == "INVALID_ARGUMENTS"
