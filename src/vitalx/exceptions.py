class VitalXError(Exception):
    """Base Exception for all VitalX errors"""

    pass


class ValidationError(VitalXError):
    """Raised when data validation fails. E.G. incorrect type being used."""

    pass


class DatabaseError(VitalXError):
    """Raised when underlying database operations fail"""

    pass


class CsvExportError(VitalXError):
    """Raised when underlying csv export operations fail"""

    pass


class CsvImportError(VitalXError):
    """Raised when underlying csv import operations fail"""

    pass


class DupeEntryPreventionError(VitalXError):
    """Raised when more than 1 entry is attempted to be written into the database in one day"""

    pass

class ReadSqlAsTextError(VitalXError):
    """Raised when there is an issue reading a .sql file as text"""

    pass
