import contextlib
import logging
from abc import abstractmethod, ABC
from typing import overload, TypeVar

from .context import LoggerContext

T = TypeVar("T")


class ExceptionFromStack:
    pass


class Logger[T](ABC):
    @abstractmethod
    def bind_scope(self, **params):
        raise NotImplementedError()

    @abstractmethod
    @contextlib.contextmanager
    def begin_scope(self, /, **params):
        raise NotImplementedError

    @overload
    def debug(self, msg: str, /, stacklevel: int = 1, **state):
        ...

    @abstractmethod
    def debug(self, msg: str, *args, **kwargs):
        raise NotImplementedError()

    @overload
    def info(self, msg: str, /, stacklevel: int = 1, **state):
        ...

    @abstractmethod
    def info(self, msg: str, *args, **kwargs):
        raise NotImplementedError()

    @overload
    def warn(self, msg: str, /, stacklevel: int = 1, **state):
        ...

    @abstractmethod
    def warn(self, msg: str, *args, **kwargs):
        raise NotImplementedError()

    @overload
    def warning(self, msg: str, /, stacklevel: int = 1, **state):
        ...

    @abstractmethod
    def warning(self, msg: str, *args, **kwargs):
        raise NotImplementedError()

    @overload
    def error(self, msg: str, /, stacklevel: int = 1, **state):
        ...

    @abstractmethod
    def error(self, msg: str, *args, **kwargs):
        raise NotImplementedError()

    @overload
    def exception(self, msg: str, /, stacklevel: int = 1, **state):
        ...

    @abstractmethod
    def exception(self, msg: str, *args, exc_info=True, **kwargs):
        raise NotImplementedError()

    @overload
    def fatal(self, msg: str, /, stacklevel: int = 1, **state):
        ...

    @abstractmethod
    def fatal(self, msg: str, *args, **kwargs):
        raise NotImplementedError()

    @overload
    def critical(self, msg: str, /, stacklevel: int = 1, **state):
        ...

    @abstractmethod
    def critical(self, msg: str, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def log(self, level, msg: str, *args, **kwargs):
        raise NotImplementedError()


class LoggerImpl[T](Logger):
    def __init__(
            self,
            logger: logging.Logger,
            context: LoggerContext,
    ):
        self.logger = logger
        self.context = context

    def bind_scope(self, **params):
        self.context.add_state(params)

    @contextlib.contextmanager
    def begin_scope(self, /, **params):
        self.context.add_state(params)
        try:
            yield
        finally:
            self.context.delete_state(params)

    def log(
            self, level: int | str, msg: str,
            exception: BaseException | ExceptionFromStack | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 1,
            **state
    ):
        context = self.context.to_dict() | state
        msg = msg.format_map(context)

        self.logger.log(
            level=level, msg=msg, extra=context,
            exc_info=exception, stack_info=stack_info, stacklevel=stacklevel,
        )

    def debug(
            self, msg: str,
            exception: BaseException | ExceptionFromStack | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 1,
            **state
    ):
        self.log(logging.DEBUG, msg, exception, stack_info=stack_info, stacklevel=stacklevel, **state)

    def info(
            self, msg: str,
            exception: BaseException | ExceptionFromStack | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 1,
            **state
    ):
        self.log(logging.INFO, msg, exception, stack_info=stack_info, stacklevel=stacklevel, **state)

    def warn(
            self, msg: str,
            exception: BaseException | ExceptionFromStack | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 1,
            **state
    ):
        self.log(logging.WARN, msg, exception, stack_info=stack_info, stacklevel=stacklevel, **state)

    def warning(
            self, msg: str,
            exception: BaseException | ExceptionFromStack | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 1,
            **state
    ):
        self.log(logging.WARNING, msg, exception, stack_info=stack_info, stacklevel=stacklevel, **state)

    def error(
            self, msg: str,
            exception: BaseException | ExceptionFromStack | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 1,
            **state
    ):
        self.log(logging.ERROR, msg, exception, stack_info=stack_info, stacklevel=stacklevel, **state)

    def exception(
            self, msg: str,
            exception: BaseException | ExceptionFromStack | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 1,
            **state
    ):
        self.log(logging.ERROR, msg, exception, stack_info=stack_info, stacklevel=stacklevel, **state)

    def fatal(
            self, msg: str,
            exception: BaseException | ExceptionFromStack | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 1,
            **state
    ):
        self.log(logging.FATAL, msg, exception, stack_info=stack_info, stacklevel=stacklevel, **state)

    def critical(
            self, msg: str,
            exception: BaseException | ExceptionFromStack | None = None,
            /,
            stack_info: bool = False, stacklevel: int = 1,
            **state
    ):
        self.log(logging.FATAL, msg, exception, stack_info=stack_info, stacklevel=stacklevel, **state)
