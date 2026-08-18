import logging
import asyncio
import os
import json
import string
import secrets
from typing import Any

try:
    from firebase_messaging import FcmPushClient, FcmRegisterConfig
except ImportError:
    FcmPushClient = None
    FcmRegisterConfig = None

from .const import (
    DATA_DIRECTORY,
)

FCM_PROJECT_ID = "ola-app-prod"
FCM_API_KEY = ""
FCM_APP_ID = {"cupra": "com.cupra.mycupra", "seat": "com.seat.myseat"}

_LOGGER = logging.getLogger(__name__)
globalFirebaseCredentialsFileName = ""


class Firebase:
    def __init__(self, logPrefix=None):
        self._pushClient = None
        if logPrefix is not None:
            self._LOGGER = logging.getLogger(__name__ + "_" + logPrefix)
        else:
            self._LOGGER = _LOGGER

    async def firebaseStart(
        self, onNotificationFunc, firebaseCredentialsFileName: str, brand="cupra"
    ) -> bool:
        """Starts the firebase cloud messaging receiver"""
        if FcmPushClient is None:
            self._LOGGER.debug("firebase-messaging not installed, skipping push notifications")
            return False
        try:
            loop = asyncio.get_running_loop()
            credentials = await loop.run_in_executor(
                None, readFCMCredsFile, firebaseCredentialsFileName
            )
            global globalFirebaseCredentialsFileName
            globalFirebaseCredentialsFileName = firebaseCredentialsFileName

            fcm_project_id = FCM_PROJECT_ID
            fcm_app_id = FCM_APP_ID.get(brand, "com.cupra.mycupra")
            fcm_api_key = FCM_API_KEY
            chars = string.ascii_letters + string.digits
            fcmMessageSenderId = "".join(secrets.choice(chars) for _ in range(16))
            fcmMessageSenderId = "fxpWQ_" + fcmMessageSenderId

            fcm_config = FcmRegisterConfig(
                fcm_project_id, fcm_app_id, fcm_api_key, fcmMessageSenderId
            )
            self._pushClient = FcmPushClient(
                onNotificationFunc, fcm_config, credentials, syncOnFCMCredentialsUpdated
            )
            fcm_token = await self._pushClient.checkin_or_register()
            self._LOGGER.debug(f"Firebase registered token: {fcm_token}")
            await self._pushClient.start()
            await asyncio.sleep(5)
            return self._pushClient.is_started()
        except Exception as e:
            self._LOGGER.error(f"Error in firebaseStart: {e}")
            return False

    async def firebaseStop(self) -> bool:
        """Stops the firebase cloud messaging receiver"""
        try:
            if self._pushClient:
                await self._pushClient.stop()
                self._pushClient = None
            return True
        except Exception as e:
            self._LOGGER.error(f"Error in firebaseStop: {e}")
            return False


def readFCMCredsFile(credsFile) -> dict[str, Any]:
    """Reads the firebase cloud messaging credentials from file"""
    try:
        if os.path.isfile(credsFile):
            with open(credsFile, "r") as f:
                credString = f.read()
            return json.loads(credString)
        else:
            return {}
    except Exception as e:
        _LOGGER.warning(f"readFCMCredsFile() not successful: {e}")
        return {}


def writeFCMCredsFile(creds, firebaseCredentialsFileName) -> None:
    """Saves the firebase cloud messaging credentials to a file for future use"""
    try:
        with open(firebaseCredentialsFileName, "w") as f:
            f.write(json.dumps(creds))
    except Exception as e:
        _LOGGER.warning(f"writeFCMCredsFile() not successful: {e}")


def syncOnFCMCredentialsUpdated(creds: dict[str, Any]) -> None:
    asyncio.get_event_loop().create_task(onFCMCredentialsUpdated(creds))


async def onFCMCredentialsUpdated(creds: dict[str, Any]) -> None:
    """Is called from firebase-messaging package"""
    global globalFirebaseCredentialsFileName
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(
        None, writeFCMCredsFile, creds, globalFirebaseCredentialsFileName
    )
