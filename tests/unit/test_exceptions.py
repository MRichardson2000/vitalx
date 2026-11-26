"""Unit tests for vitalx.exceptions custom exception classes.

What to test:
- Each exception class can be instantiated with a message
- Each exception is a subclass of VitalXError (the base exception)
- Each exception can be caught by catching VitalXError (polymorphic catching)
- Each exception can be caught individually by its specific class
- The str() representation of each exception returns the message

Exceptions to test:
- VitalXError (base)
- ValidationError
- DatabaseError
- CsvExportError
- CsvImportError
- DupeEntryPreventionError
- ReadSqlAsTextError

Suggested mocks: None needed - these are simple exception classes.
"""

from vitalx.exceptions import (
    VitalXError,
    ValidationError,
    DatabaseError,
    CsvExportError,
    CsvImportError,
    DupeEntryPreventionError,
    ReadSqlAsTextError,
)


def test_vitalx_error_base_can_be_raised_and_caught():
    """
    VitalXError should be instantiable and catchable.
    Hint: raise VitalXError("msg") and catch it, assert str(exc) == "msg".
    """
    pass


def test_validation_error_is_subclass_of_vitalx_error():
    """
    ValidationError should inherit from VitalXError.
    Hint: assert issubclass(ValidationError, VitalXError).
    """
    pass


def test_database_error_is_subclass_of_vitalx_error():
    """
    DatabaseError should inherit from VitalXError.
    """
    pass


def test_csv_export_error_is_subclass_of_vitalx_error():
    """
    CsvExportError should inherit from VitalXError.
    """
    pass


def test_csv_import_error_is_subclass_of_vitalx_error():
    """
    CsvImportError should inherit from VitalXError.
    """
    pass


def test_dupe_entry_prevention_error_is_subclass_of_vitalx_error():
    """
    DupeEntryPreventionError should inherit from VitalXError.
    """
    pass


def test_read_sql_as_text_error_is_subclass_of_vitalx_error():
    """
    ReadSqlAsTextError should inherit from VitalXError.
    """
    pass


def test_catching_base_catches_all_subclasses():
    """
    Catching VitalXError should catch any subclass exception.
    Hint: raise ValidationError(...) and catch it as VitalXError.
    """
    pass


def test_exception_message_is_preserved():
    """
    The message passed to each exception should be accessible via str(exc).
    Test at least two different exception types.
    """
    pass
