"""Package-specific exceptions."""


class ValidationError(ValueError):
    """Raised when input validation fails in the library.

    This subclass exists so callers can distinguish library validation
    errors from generic Python ValueError exceptions.
    """

    pass
