from abc import ABCMeta, abstractmethod


class BaseGenerator(metaclass=ABCMeta):
    @abstractmethod
    def generate(self):
        pass

    def __call__(self):
        self.generate()
