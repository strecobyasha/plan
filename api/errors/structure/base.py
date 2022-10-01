from abc import ABC, abstractproperty


class BaseErrors(ABC):
    @abstractproperty
    def NOT_EXISTS(self):
        """Element does not exist"""

    @abstractproperty
    def ALREADY_EXISTS(self):
        """Element already exists"""
