import logging
from typing import runtime_checkable, Protocol

from dishka import Provider, Scope, provide

from unilog import Logger, LoggerImpl, LoggerContextImpl, LoggerContext
from unilog.logger import T


@runtime_checkable
class StdLoggerFactory(Protocol):
    def __call__(self, generic_type: type, default_name: str = ...) -> logging.Logger:
        ...


def default_std_logger_factory(
        generic_type: type,
        default_name: str = "unilog.Logger"
) -> logging.Logger:
    if generic_type != T:
        logger_name = f"{generic_type.__module__}.{generic_type.__name__}"
    else:
        logger_name = default_name

    logger = logging.getLogger(logger_name)
    return logger


class UniloggingProvider(Provider):
    def __init__(
            self,
            scope: Scope = Scope.REQUEST,
            std_logger_factory: StdLoggerFactory = default_std_logger_factory,
            initial_context: dict | None = None,
    ):
        super().__init__(scope=scope)
        self._std_logger_factory = std_logger_factory
        self._initial_context = initial_context

    @provide
    def get_logger_context(self) -> LoggerContext:
        return LoggerContextImpl(context=[self._initial_context or {}])

    @provide
    def get_logger(
            self,
            logger_generic_type: type[T],
            context: LoggerContext
    ) -> Logger[T]:
        std_logger = self._std_logger_factory(logger_generic_type)
        logger = LoggerImpl(
            logger=std_logger,
            context=context
        )
        return logger
