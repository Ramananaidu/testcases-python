# import time
import logging
from rocore.decorators.logs import log


# logger = logging.getLogger()
# logger.addHandler(logging.StreamHandler())


def test_log_decorator(caplog):
    caplog.set_level(logging.INFO)

    @log()
    def hello_world():
        # time.sleep(0.343)
        return 'Hello World'

    hello_world()

    assert 'hello_world' in caplog.text
    print(caplog.text)


