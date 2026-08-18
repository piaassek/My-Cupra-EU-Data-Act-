"""Custom exceptions for pycupra_lib."""

class PyCupraException(Exception):
    """Base exception for pycupra."""
    def __init__(self, status):
        super(PyCupraException, self).__init__(status)
        self.status = status


class PyCupraConfigException(PyCupraException):
    """Raised when Seat/Cupra API client is configured incorrectly."""
    pass


class PyCupraAuthenticationException(PyCupraException):
    """Raised when credentials are invalid during authentication."""
    pass


class PyCupraAccountLockedException(PyCupraException):
    """Raised when account is locked from too many login attempts."""
    pass


class PyCupraTokenExpiredException(PyCupraException):
    """Raised when token has expired and cannot be refreshed."""
    pass


class PyCupraEULAException(PyCupraException):
    """Raised when user must accept terms & conditions."""
    pass


class PyCupraMarketingConsentException(PyCupraException):
    """Raised when user must answer marketing consent questions."""
    pass


class PyCupraThrottledException(PyCupraException):
    """Raised when rate limit is reached."""
    pass


class PyCupraLoginFailedException(PyCupraException):
    """Raised when login flow fails."""
    pass


class PyCupraClientRequestForbidden(PyCupraException):
    """Raised when client request returns 403 Forbidden."""
    pass


class PyCupraInvalidRequestException(PyCupraException):
    """Raised when an invalid request is sent to API."""
    pass


class PyCupraRequestInProgressException(PyCupraException):
    """Raised when a conflicting action is already in progress."""
    pass


class PyCupraServiceUnavailable(PyCupraException):
    """Raised when the remote service is unavailable."""
    pass


class PyCupraEUDAPermissionExpiredException(PyCupraException):
    """Raised when EU Data Act permissions have expired."""
    pass
