"""Singleton class decorator module"""


class SingletonViolationError(Exception):
    """Raised when more than one instance of class is being created."""
    pass


class Singleton:
    """Prevent class from having more than one instance."""
    def __init__(self, cls):
        """Decorate class.

        Args:
            cls: Class to be decorated.
        """
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        """Create instance.

        Return:
            self.instance: The only one possible instance of class.
        Raises:
            SingletonViolationError: When an additional instance is being created.
        """
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)
        else:
            raise SingletonViolationError()
        return self.instance
