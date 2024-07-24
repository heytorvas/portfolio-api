class ObjectNotFoundError(Exception):
    """Raised when don't found this object in database."""

    def __init__(self, entity: str) -> None:
        super().__init__(f"{entity} not found in database.")


class DatabaseError(Exception):
    """A database error."""


class UnauthorizedHTTPError(Exception):
    """Raised when there's an unauthorized access attempt."""
