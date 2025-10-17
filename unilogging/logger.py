import contextlib
import logging
from abc import ABC, abstractmethod
from typing import TypeVar

from .context import LoggerContext

T = TypeVar("T")


class ExceptionFromStack:
    """
    An object that is transmitted if it
    is necessary to receive exception information from the stack.
    """


class Logger[T](ABC):
    """Default logger interface."""

    @abstractmethod
    def bind_scope(self, **params):
        """Add keys to the current context."""
        raise NotImplementedError

    @abstractmethod
    @contextlib.contextmanager
    def begin_scope(self, /, **params):
        """
        Add keys to the current context.

        It is used with the contextmanager and after exiting it,
        the added keys are deleted.
        """
        raise NotImplementedError

    @abstractmethod
    def debug(
            self, msg: str,
            exception: BaseException | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 3,
            **state,
    ):
        """Log message with DEBUG level."""
        raise NotImplementedError

    @abstractmethod
    def info(
            self, msg: str,
            exception: BaseException | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 3,
            **state,
    ):
        """Log message with INFO level."""
        raise NotImplementedError

    @abstractmethod
    def warn(
            self, msg: str,
            exception: BaseException | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 3,
            **state,
    ):
        """Log message with WARNING level."""
        raise NotImplementedError

    @abstractmethod
    def warning(
            self, msg: str,
            exception: BaseException | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 3,
            **state,
    ):
        """Log message with WARNING level."""
        raise NotImplementedError

    @abstractmethod
    def error(
            self, msg: str,
            exception: BaseException | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 3,
            **state,
    ):
        """Log message with ERROR level."""
        raise NotImplementedError

    @abstractmethod
    def exception(
            self, msg: str,
            exception: BaseException | bool | None = True,
            /,
            stack_info: bool = False, stacklevel: int = 3,
            **state,
    ):
        """Log message with ERROR level and exception info."""
        raise NotImplementedError

    @abstractmethod
    def fatal(
            self, msg: str,
            exception: BaseException | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 3,
            **state,
    ):
        """Log message with FATAL level."""
        raise NotImplementedError

    @abstractmethod
    def critical(
            self, msg: str,
            exception: BaseException | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 3,
            **state,
    ):
        """Log message with CRITICAL level."""
        raise NotImplementedError

    @abstractmethod
    def log(
            self, level: int, msg: str,
            exception: BaseException | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 2,
            **state,
    ):
        """Log message."""
        raise NotImplementedError


class LoggerImpl[T](Logger):
    """
    The implementation of the logger interface
    is based on standard python logging library.
    """

    def __init__(
            self,
            logger: logging.Logger,
            context: LoggerContext,
    ):
        """
        :param logger: configured standard logger instance
        :param context: instance of LoggerContext
        """
        self.logger = logger
        self.context = context

    def bind_scope(self, **params):
        """
        Add keys to the current context.

        :param params:
        :return:
        """
        self.context.add_state(params)

    @contextlib.contextmanager
    def begin_scope(self, /, **params):
        """
        Add keys to the current context.

        It is used with the contextmanager and after exiting it,
        the added keys are deleted.
        """
        self.context.add_state(params)
        try:
            yield
        finally:
            self.context.delete_state(params)

    def log(
            self, level: int, msg: str,
            exception: BaseException | bool | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 2,
            **state,
    ):
        """Log message."""
        context = self.context.to_dict() | state
        msg = msg.format_map(context)

        self.logger.log(
            level=level, msg=msg, extra=context,
            exc_info=exception, stack_info=stack_info, stacklevel=stacklevel,
        )

    def debug(
            self, msg: str,
            exception: BaseException | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 3,
            **state,
    ):
        """Log message with DEBUG level."""
        self.log(
            logging.DEBUG, msg, exception,
            stack_info=stack_info, stacklevel=stacklevel,
            **state
        )

    def info(
            self, msg: str,
            exception: BaseException | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 3,
            **state,
    ):
        """Log message with INFO level."""
        self.log(
            logging.INFO, msg, exception,
            stack_info=stack_info, stacklevel=stacklevel,
            **state
        )

    def warn(
            self, msg: str,
            exception: BaseException | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 3,
            **state,
    ):
        """Log message with WARNING level."""
        self.log(
            logging.WARNING, msg, exception,
            stack_info=stack_info, stacklevel=stacklevel,
            **state
        )

    def warning(
            self, msg: str,
            exception: BaseException | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 3,
            **state,
    ):
        """Log message with WARNING level."""
        self.log(
            logging.WARNING, msg, exception,
            stack_info=stack_info, stacklevel=stacklevel,
            **state
        )

    def error(
            self, msg: str,
            exception: BaseException | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 3,
            **state,
    ):
        """Log message with ERROR level."""
        self.log(
            logging.ERROR, msg, exception,
            stack_info=stack_info, stacklevel=stacklevel,
            **state
        )

    def exception(
            self, msg: str,
            exception: BaseException | bool | None = True,
            /,
            stack_info: bool = False, stacklevel: int = 3,
            **state,
    ):
        """Log message with ERROR level and exception info."""
        self.log(
            logging.ERROR, msg, exception,
            stack_info=stack_info, stacklevel=stacklevel,
            **state
        )

    def fatal(
            self, msg: str,
            exception: BaseException | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 3,
            **state,
    ):
        """Log message with FATAL level."""
        self.log(
            logging.FATAL, msg, exception,
            stack_info=stack_info, stacklevel=stacklevel,
            **state
        )

    def critical(
            self, msg: str,
            exception: BaseException | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 3,
            **state,
    ):
        """Log message with CRITICAL level."""
        self.log(
            logging.CRITICAL, msg, exception,
            stack_info=stack_info, stacklevel=stacklevel,
            **state
        )
