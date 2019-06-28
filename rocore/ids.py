from uuid import uuid4, UUID
from typing import Callable, Any, Generator


IdGenerator = Callable[[], Any]
StringIdFactory = Callable[[], str]
IntIdFactory = Callable[[], int]


def uuid_generator() -> Generator[None, UUID, None]:
    while True:
        yield uuid4()


def int_id_generator(seed: int = 0) -> Generator[None, int, None]:
    while True:
        seed += 1
        yield seed


def uuid_factory() -> UUID:
    return uuid4()


_int_id_generator = int_id_generator()


def int_id_factory() -> int:
    return next(_int_id_generator)
