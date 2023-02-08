from abc import abstractmethod, ABCMeta


class IReporter(metaclass=ABCMeta):
    @abstractmethod
    def debug(self, msg: str, *args, **kwargs):
        "Debug level of logging"

    @abstractmethod
    def info(self, msg: str, *args, **kwargs):
        "Info level of logging"

    @abstractmethod
    def warning(
        self, exc: Exception, context: str = None, cause: Exception = None,
    ):
        "Warning level of logging"

    def error(
        self, exc: Exception, context: str = None, cause: Exception = None,
    ):
        logger.error(
            "[%s] %s: %s", exc.__class__.__name__, exc, exc_info=True,
        )
