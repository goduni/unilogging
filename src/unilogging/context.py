from abc import abstractmethod


class LoggerContext:
    @abstractmethod
    def add_state(self, state: dict):
        raise NotImplementedError()

    @abstractmethod
    def delete_state(self, state: dict):
        raise NotImplementedError()

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError()


class LoggerContextImpl(LoggerContext):
    _context: list[dict]

    def __init__(self, context: list[dict]):
        self._context = context

    def add_state(self, state: dict):
        self._context.append(state)

    def delete_state(self, state: dict):
        self._context.remove(state)

    def to_dict(self) -> dict:
        result = {}
        for state in self._context:
            result.update(state)
        return result
