import io
import json
import logging

from pythonjsonlogger.json import JsonFormatter

from unilogging import LoggerImpl, LoggerContextImpl

logging.basicConfig(level=logging.NOTSET)
std = logging.getLogger("default")

logger = LoggerImpl(
    logger=std,
    context=LoggerContextImpl(context=[])
)


def test_logger(caplog):
    caplog.set_level(logging.NOTSET)

    log_stream = io.StringIO()

    handler = logging.StreamHandler(log_stream)
    handler.setFormatter(JsonFormatter(
        "%(name)s %(levelname)s %(message)s"
    ))

    std.addHandler(handler)

    with logger.begin_scope(meow="meow"):
        logger.info("log with INFO level")
        logger.debug("log with DEBUG level")
        logger.warn("log with WARN level")
        logger.warning("log with WARNING level")
        logger.error("log with ERROR level")

        try:
            raise Exception("cat not found food at expected time")
        except Exception as e:
            logger.exception(str(e), exception=e)

        logger.fatal("log with FATAL level")
        logger.critical("log with CRITICAL level")

    logger.bind_scope(via_bind="meow")
    logger.info("meow")

    log_messages = [json.loads(x) for x in log_stream.getvalue().splitlines()]

    assert len(log_messages) == 9

    assert log_messages[0] == {"name": "default", "levelname": "INFO", "message": "log with INFO level", "meow": "meow"}
    assert log_messages[1] == {"name": "default", "levelname": "DEBUG", "message": "log with DEBUG level", "meow": "meow"}
    assert log_messages[2] == {"name": "default", "levelname": "WARNING", "message": "log with WARN level", "meow": "meow"}
    assert log_messages[3] == {"name": "default", "levelname": "WARNING", "message": "log with WARNING level", "meow": "meow"}
    assert log_messages[4] == {"name": "default", "levelname": "ERROR", "message": "log with ERROR level", "meow": "meow"}

    assert log_messages[5].pop("exc_info", None) is not None
    assert log_messages[5].pop("exception", None) is not None
    assert log_messages[5] == {"name": "default", "levelname": "ERROR", "message": "cat not found food at expected time", "meow": "meow"}

    assert log_messages[6] == {"name": "default", "levelname": "CRITICAL", "message": "log with FATAL level", "meow": "meow"}
    assert log_messages[7] ==  {"name": "default", "levelname": "CRITICAL", "message": "log with CRITICAL level", "meow": "meow"}

    assert log_messages[8] ==  {"name": "default", "levelname": "INFO", "message": "meow", "via_bind": "meow"}
