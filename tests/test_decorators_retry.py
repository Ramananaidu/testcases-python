import pytest
import asyncio
from pytest import raises
from typing import Any
from rocore.decorators import retry


class CrashTest(RuntimeError):

    def __init__(self, value: Any = ''):
        super().__init__('Crash!' + (f' {value}' if value else ''))
        self.value = value

    def __eq__(self, other):
        if isinstance(other, str):
            return str(self) == other
        if isinstance(other, CrashTest):
            return self.value == other.value
        return NotImplemented


def test_retry_decorator():
    i = 0

    @retry()
    def crashing():
        nonlocal i
        i += 1
        if i < 3:
            raise CrashTest()

        return i

    x = crashing()
    assert i == 3
    assert x == 3


@pytest.mark.asyncio
async def test_retry_decorator_async():
    i = 0

    @retry()
    async def crashing():
        nonlocal i
        i += 1
        if i < 3:
            raise CrashTest()

        return i

    x = await crashing()
    assert i == 3
    assert x == 3


def test_retry_decorator_no_delay():
    i = 0

    @retry(delay=0)
    def crashing():
        nonlocal i
        i += 1
        if i < 3:
            raise CrashTest()

        return i

    x = crashing()
    assert i == 3
    assert x == 3


def test_retry_decorator_exact_exceptions():

    @retry(catch_exceptions_types=CrashTest)
    def crashing():
        return 1 / 0

    with raises(ZeroDivisionError):
        crashing()


@pytest.mark.asyncio
async def test_retry_decorator_exact_exceptions_async():

    @retry(catch_exceptions_types=CrashTest)
    async def crashing():
        return 1 / 0

    with raises(ZeroDivisionError):
        await crashing()


def test_retry_decorator_exceeding_attempts_raises():
    i = 0

    @retry(times=3)
    def crashing():
        nonlocal i
        i += 1

        if i < 5:
            raise CrashTest(i)

        return True

    with raises(CrashTest, match='Crash! 4'):
        crashing()


@pytest.mark.asyncio
async def test_retry_decorator_exceeding_attempts_raises_async():
    i = 0

    @retry(times=3)
    async def crashing():
        nonlocal i
        i += 1

        if i < 5:
            raise CrashTest(i)

        return True

    with raises(CrashTest, match='Crash! 4'):
        await crashing()


def test_retry_decorator_callback():
    exceptions = []

    def callback(ex, attempt):
        exceptions.append((ex, attempt))

    i = 0

    @retry(on_exception=callback)
    def crashing():
        nonlocal i
        i += 1
        if i < 3:
            raise CrashTest(i)

        return i

    crashing()

    assert len(exceptions) == 2
    assert [(CrashTest(1), 1),
            (CrashTest(2), 2)] == exceptions


@pytest.mark.asyncio
async def test_retry_decorator_callback_async():
    exceptions = []

    def callback(ex, attempt):
        exceptions.append((ex, attempt))

    i = 0

    @retry(on_exception=callback)
    async def crashing():
        nonlocal i
        i += 1
        if i < 3:
            raise CrashTest(i)

        return i

    await crashing()

    assert len(exceptions) == 2
    assert [(CrashTest(1), 1),
            (CrashTest(2), 2)] == exceptions


@pytest.mark.asyncio
async def test_retry_decorator_callback_async_callback():
    exceptions = []

    async def callback(ex, attempt):
        await asyncio.sleep(0)
        exceptions.append((ex, attempt))

    i = 0

    @retry(on_exception=callback)
    async def crashing():
        nonlocal i
        i += 1
        if i < 3:
            raise CrashTest(i)

        return i

    await crashing()

    assert len(exceptions) == 2
    assert [(CrashTest(1), 1),
            (CrashTest(2), 2)] == exceptions
