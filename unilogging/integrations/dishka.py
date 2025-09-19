import logging
from typing import Protocol, runtime_checkable

from dishka import Provider, Scope, provide

from unilogging import Logger, LoggerContext, LoggerContextImpl, LoggerImpl
from unilogging.logger import T


@runtime_checkable
class StdLoggerFactory(Protocol):
    """An interface for implementing the protocol of the standard logger factory."""

    def __call__(self, generic_type: type, default_name: str = ...) -> logging.Logger:
        """
        Standard protocol implementation of the logger factory.

        Implements a feature for substituting the name
        of the class from where the logger was requested.

        :param generic_type: the type of the generic logger to use.
        :param default_name: name of the generic logger to use.
        :return: standard logger instance with substituted logger name.
        """


def default_std_logger_factory(
        generic_type: type,
        default_name: str = "unilogging.Logger",
) -> logging.Logger:
    """
    Standard protocol implementation of the logger factory.

    Implements a feature for substituting the name
    of the class from where the logger was requested.

    :param generic_type: the type of the generic logger to use.
    :param default_name: name of the generic logger to use.
    :return: standard logger instance with substituted logger name.
    """
    if not isinstance(generic_type, type(T)):
        logger_name = f"{generic_type.__module__}.{generic_type.__name__}"
    else:
        logger_name = default_name

    return logging.getLogger(logger_name)


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
            context: LoggerContext,
    ) -> Logger[T]:
        std_logger = self._std_logger_factory(logger_generic_type)
        return LoggerImpl(
            logger=std_logger,
            context=context,
        )
