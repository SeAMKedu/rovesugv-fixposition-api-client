from typing import Any

from pydantic import ValidationError

from fixposition_client.models import APIException


def handle_file_not_found_error(error: FileNotFoundError) -> dict[str, Any]:
    """Handle the FileNotFoundError."""
    return APIException(
        ok=False,
        message="FileNotFoundError",
        errors=[error.strerror]
    ).model_dump(by_alias=True)


def handle_validation_error(error: ValidationError) -> dict[str, Any]:
    """Handle the validation error of the HTTP POST request data."""
    return APIException(
        ok=False,
        message="ValidationError",
        errors=error.errors(),
    ).model_dump(by_alias=True)
