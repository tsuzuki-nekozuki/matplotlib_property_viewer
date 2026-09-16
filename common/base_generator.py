from abc import ABC, abstractmethod


class BaseGenerator(ABC):
    @abstractmethod
    def generate(self):
        raise NotImplementedError('Subclasses must implement generate().')

    def __call__(self):
        return self.generate()
