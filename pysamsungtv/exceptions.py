"""Custom exceptions for the Samsung TV client."""

from __future__ import annotations


class SamsungTVError(Exception):
    """Base error for the Samsung TV client."""


class SamsungTVAuthenticationError(SamsungTVError):
    """Raised when an access token is missing or rejected."""


class SamsungTVProtocolError(SamsungTVError):
    """Raised when the JSON-RPC response is invalid."""


class SamsungTVResponseError(SamsungTVError):
    """Raised when the server returns a JSON-RPC error payload."""

    def __init__(self, message: str, code: int | None = None) -> None:
        super().__init__(message)
        self.code = code


class SamsungTVUnknownError(SamsungTVResponseError):
    """Raised when the TV reports an unknown error (-32000)."""


class SamsungTVNotSupportedError(SamsungTVResponseError):
    """Raised when the control is not supported on the current model (-32001)."""


class SamsungTVFailedError(SamsungTVResponseError):
    """Raised when the control execution failed (-32002)."""


class SamsungTVInvalidOperationError(SamsungTVResponseError):
    """Raised when the control has invalid data (-32003)."""


class SamsungTVUnauthorizedError(SamsungTVResponseError):
    """Raised when the client is not authorized (-32010)."""


__all__ = [
    "SamsungTVError",
    "SamsungTVAuthenticationError",
    "SamsungTVProtocolError",
    "SamsungTVResponseError",
    "SamsungTVUnknownError",
    "SamsungTVNotSupportedError",
    "SamsungTVFailedError",
    "SamsungTVInvalidOperationError",
    "SamsungTVUnauthorizedError",
]
