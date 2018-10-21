import time
import pytest
from rocore.diagnostics import StopWatch


def test_stopwatch():
    a = StopWatch()
    a.start()

    time.sleep(0.01)

    a.stop()
    assert pytest.approx(0.01, .1) == a.elapsed_s
    assert pytest.approx(a.elapsed_ms, .1) == a.elapsed_s * 1000


def test_stopwatch_with_context_manager():
    with StopWatch() as a:
        time.sleep(0.01)

    assert pytest.approx(0.01, .1) == a.elapsed_s
    assert pytest.approx(a.elapsed_ms, .1) == a.elapsed_s * 1000