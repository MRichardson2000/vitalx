class VitalXError(Exception):
    """Base Exception for all VitalX errors"""

    pass


class ValidationError(VitalXError):
    """Raised when data validation fails. E.G. incorrect type being used."""

    pass


class DatabaseError(VitalXError):
    """Raised when underlying database operations fail"""

    pass


class EmptyDictionaryError(VitalXError):
    """Raised when an empty dictionary is passed in and an index value is raised"""

    pass


class EmptyListError(VitalXError):
    """Raised when an empty list is passed in and an index value is raised"""

    pass
