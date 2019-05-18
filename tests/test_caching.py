from rocore.caching import Cache


def test_cache_item():
    cache = Cache()
    item = cache.get('cat')

    assert item is None

    cache.set('cat', 'Celine')
    item = cache.get('cat')

    assert 'Celine' == item.value


def test_cache_max_size():
    cache = Cache(max_size=20)

    for i in range(30):
        cache.set(f'key_{i}', i)

    for i in range(10):
        assert f'key_{i}' not in cache

    for i in range(10, 30):
        assert f'key_{i}' in cache


def test_cache_len():
    cache = Cache(max_size=20)

    for i in range(30):
        cache.set(f'key_{i}', i)

    assert 20 == len(cache)


def test_cache_iterable():
    cache = Cache()

    for i in range(20):
        cache.set(i, i * i)

    j = 0
    for key, item in cache:
        assert j == key
        assert item.value == j * j
        j += 1


def test_expiration_policy():
    cache = Cache(expiration_policy=lambda item: item.value > 5)

    for i in range(10):
        cache.set(i, i)

    expired = cache.get(6)
    assert expired is None

    assert 6 not in cache
