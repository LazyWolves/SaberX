from saberx.sabercore.triggers.memorytrigger import MemoryTrigger


class TestMemoryTrigger:

    def test_memory_trigger(self):
        memoryTrigger = MemoryTrigger(
            type="MEMORY_TRIGGER",
            attr="used",
            threshold=10.0,
            operation='>',
            check="virtual"
        )

        triggered, error = memoryTrigger.fire_trigger()

        assert triggered
        assert error is None

        memoryTrigger = MemoryTrigger(
            type="MEMORY_TRIGGER",
            attr="used",
            threshold=0.0,
            operation='>=',
            check="swap"
        )

        triggered, error = memoryTrigger.fire_trigger()

        assert triggered
        assert error is None
