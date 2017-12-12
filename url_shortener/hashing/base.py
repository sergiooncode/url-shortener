import abc


class BaseHasher(abc.ABC):
    """
    Base class to be subclassed by concrete hasher classes. Enforces overriding encode method by raising TypeError if a concrete class doesn't implement it. Decode method is not enforced since is not used.
    """
    @abc.abstractmethod
    def encode(self):
        pass
