"""
pycupra_lib - Embedded and optimized Python 3 library for interacting with the Cupra/Seat Connect portal.
"""

from .connection import Connection
from .eudaconnection import EUDAConnection
from .vehicle import Vehicle
from .dashboard import Dashboard
from .exceptions import (
    PyCupraConfigException,
    PyCupraAuthenticationException,
    PyCupraAccountLockedException,
    PyCupraLoginFailedException,
    PyCupraInvalidRequestException,
    PyCupraRequestInProgressException,
    PyCupraClientRequestForbidden,
    PyCupraException,
    PyCupraTokenExpiredException,
    PyCupraEULAException,
    PyCupraMarketingConsentException,
    PyCupraThrottledException,
    PyCupraServiceUnavailable,
    PyCupraEUDAPermissionExpiredException,
)

__all__ = [
    "Connection",
    "EUDAConnection",
    "Vehicle",
    "PyCupraConfigException",
    "PyCupraAuthenticationException",
    "PyCupraAccountLockedException",
    "PyCupraLoginFailedException",
    "PyCupraInvalidRequestException",
    "PyCupraRequestInProgressException",
    "PyCupraClientRequestForbidden",
    "PyCupraException",
    "PyCupraTokenExpiredException",
    "PyCupraEULAException",
    "PyCupraMarketingConsentException",
    "PyCupraThrottledException",
    "PyCupraServiceUnavailable",
    "PyCupraEUDAPermissionExpiredException",
]
