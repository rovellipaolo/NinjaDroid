from abc import ABCMeta, abstractmethod


class UseCase(metaclass=ABCMeta):
    """
    Interface for a use-case representation.
    """

    @abstractmethod
    def execute(self):
        pass
