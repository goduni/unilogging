import logging

from dishka import make_container

from unilogging import Logger
from unilogging.integrations.dishka import UniloggingProvider

container = make_container(UniloggingProvider())


def test_logger(caplog):
    caplog.set_level(logging.NOTSET)

    with container() as app_container:
        with app_container() as request_container:
            logger = request_container.get(Logger)
            logger.info("Meow!")

            assert caplog.records[0].message == "Meow!"
            assert caplog.records[0].name == "unilogging.Logger"
            caplog.clear()

            logger = request_container.get(Logger[str])
            logger.info("Meow!")

            assert caplog.records[0].name == "builtins.str"
