class VitalXError(Exception):
    """Base Exception for all VitalX errors"""

    pass


class ValidationError(VitalXError):
    """Raised when data validation fails. E.G. incorrect type being used."""

    pass


class DatabaseError(VitalXError):
    """Raised when underlying database operations fail"""

    pass
