from abc import ABC, abstractmethod


class LoggerContext(ABC):
    """Interface of the storage class for the current logger context."""

    @abstractmethod
    def add_state(self, state: dict):
        """Adds the passed dictionary to the current context."""
        raise NotImplementedError

    @abstractmethod
    def delete_state(self, state: dict):
        """Removes the passed dictionary from the current context."""
        raise NotImplementedError

    @abstractmethod
    def to_dict(self) -> dict:
        """Combines all the contexts into one dictionary."""
        raise NotImplementedError


class LoggerContextImpl(LoggerContext):
    """The standard storage implementation for storing the logger context."""
    _context: list[dict]

    def __init__(self, context: list[dict]):
        """
        :param context: a list of dictionaries representing the logger context.
        """
        self._context = context

    def add_state(self, state: dict):
        """Adds the passed dictionary to the current context."""
        self._context.append(state)

    def delete_state(self, state: dict):
        """Removes the passed dictionary from the current context."""
        self._context.remove(state)

    def to_dict(self) -> dict:
        """Combines all the contexts into one dictionary."""
        result = {}
        for state in self._context:
            result.update(state)
        return result
