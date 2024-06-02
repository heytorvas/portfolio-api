class ObjectNotFoundError(Exception):
    """Raised when don't found this object in database."""


class DatabaseError(Exception):
    """A database error."""


class UnauthorizedHTTPError(Exception):
    """Raised when there's an unauthorized access attempt."""
