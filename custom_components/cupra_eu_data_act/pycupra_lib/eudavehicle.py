#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Extract information from data files downloaded from the EU Data Act portal of Volkswagen group.
import logging
from datetime import datetime
from typing import Any, TypedDict

from .const import (
    EUDA_DATA_CONVERSION_FLOAT,
    EUDA_DATA_CONVERSION_INT,
    EUDA_DATA_CONVERSION_BOOL,
    EUDA_DATA_CONVERSION_DIVIDE_BY_10,
    EUDA_DATA_CONVERSION_KELVIN_TO_CELSIUS,
    EUDA_DATA_CONVERSION_INT_INVERT,
    EUDA_DATA_DICT,
    EUDA_DATA_NO_SHOW_SET,
)

_LOGGER = logging.getLogger(__name__)


class EUDAVehicle:
    # Init connection class
    def __init__(self, conn, data):
        self._logPrefix = data.get("logPrefix", None)
        if self._logPrefix is not None:
            self._LOGGER = logging.getLogger(__name__ + "_" + self._logPrefix)
        else:
            self._LOGGER = _LOGGER

        self._LOGGER.debug(
            conn.anonymise(f"Creating Vehicle class object with data {data}")
        )
        self._connection = conn
        self._vin = data.get("vin", "")
        self._brand = data.get("brand", "")
        self._nickName = data.get("nickName", "")
        self._dashboard = None
        self._states = {}
        self.currentData = {}
        self.tripData = {}
        self._tripSumDictDay = {}
        self._tripSumDictMonth = {}
        self._defined_EUDA_keys = set()
        for elem in EUDA_DATA_DICT.values():
            if elem.get("key", "") != "":
                self._defined_EUDA_keys.add(elem.get("key", ""))

    def dashboard(self, **config):
        """Returns dashboard, creates new if none exist."""
        if self._dashboard is None:
            # Init new dashboard if none exist
            from .dashboard import Dashboard

            self._dashboard = Dashboard(self, **config)
        elif config != self._dashboard._config:
            # Init new dashboard on config change
            from .dashboard import Dashboard

            self._dashboard = Dashboard(self, **config)
        return self._dashboard

    @property
    def vin(self):
        return self._vin

    @property
    def unique_id(self):
        return self.vin

    @property
    def nickname(self):
        return self._nickName

    @property
    def is_nickname_supported(self) -> bool:
        """Return true if nickname is supported."""
        if self._nickName != "":
            return True
        else:
            return False

    @property
    def brand(self):
        """Return brand"""
        return self._brand

    @property
    def is_brand_supported(self) -> bool:
        """Return true if brand is supported."""
        if self._brand != "":
            return True
        else:
            return False

    @property
    def model(self):
        """Return model"""
        return GetModelFromNickName(self._nickName).lower()

    @property
    def model_year(self):
        """Return model year"""
        return "unknown"

    @property
    def is_model_image_small_supported(self) -> bool:
        return False

    @property
    def is_model_image_large_supported(self) -> bool:
        return False

    @property
    def model_image_small(self):
        return None

    @property
    def model_image_large(self):
        return None

    @property
    def battery_level(self) -> int:
        """Return battery level in %."""
        val = self.getEUDADataFieldValue(
            ["dc35366c-f5da-32a7-9674-5495a8082e69", "506cb83e-f99f-3af3-bbeb-0429b69a78d9", "ac1108b1-b8cc-3db9-a663-03d387e42223"],
            EUDA_DATA_CONVERSION_INT,
            field_names=["battery_state_report.soc", "battery_level_HV.value", "state_of_charge"]
        )
        return int(val) if val else 0

    @property
    def electric_range(self) -> int:
        """Return electric range in km."""
        val = self.getEUDADataFieldValue(
            ["eb2b3c59-6804-3463-ba3b-bcadc6954e08", "0ca40e18-0564-3eda-bcc0-7aee9ef44f04"],
            EUDA_DATA_CONVERSION_INT,
            field_names=["primary_range", "electric_range", "value"]
        )
        return int(val) if val else 0

    @property
    def mileage(self) -> int:
        """Return total odometer mileage in km."""
        val = self.getEUDADataFieldValue(
            ["dfbf2da2-96f1-3231-a156-b7015f72aa1e", "75d65f00-5fa8-334a-826d-e73e91fe5c8d", "30cc36fd-71ca-3c09-9296-e94ebd47bd2b"],
            EUDA_DATA_CONVERSION_INT,
            field_names=["mileage.value", "mileage"]
        )
        return int(val) if val else 0

    @property
    def target_soc(self) -> int:
        """Return target SoC in %."""
        val = self.getEUDADataFieldValue(
            ["5ec53403-2543-308d-9e95-e80a0e0b25be", "b3b04f31-b10e-38aa-b8ad-c0da7c06caea"],
            EUDA_DATA_CONVERSION_INT,
            field_names=["settings.target_soc"]
        )
        return int(val) if val else 0

    @property
    def charging(self) -> bool:
        """Return true if charging."""
        val = self.getEUDADataFieldValue("17e75411-e651-3ba5-9358-6aab3b022581")
        return str(val).upper() == "CONNECTED"

    @property
    def charging_state(self) -> str:
        """Return charging state."""
        return "charging" if self.charging else "disconnected"

    @property
    def charging_time_left(self) -> int:
        return 0

    @property
    def charging_estimated_end_time(self):
        return None

    @property
    def electric_climatisation(self) -> bool:
        return False

    @property
    def climatisation(self) -> bool:
        val = self.getEUDADataFieldValue("1afa44b8-2dd0-34d0-8fbd-ceebd72dd493")
        return str(val).upper() == "ON"

    def getEUDADataFieldValue(self, key: str | list | tuple, conversion: int | None = None, field_names: list | None = None) -> Any:
        """Return value of an EUDA data field identified by key or field_names."""
        if key == "00000000-0000-0000-0000-0000":
            attrs = self.getEUDADataAllUndefinedFields
            return len(attrs)
        elif key == "01000000-0000-0000-0000-0000":
            return self.getEUDAFileTimestamp
        elif isinstance(key, str) and (key.startswith("10000000-0000") or key.startswith("11000000-0000")):
            if key.startswith("10000000-0000"):
                tripSum = self.getLatestTripSumValues("day")
            else:
                tripSum = self.getLatestTripSumValues("month")
            if key.endswith("0000"):
                return tripSum.get("startMileage", 0)
            elif key.endswith("0001"):
                return tripSum.get("fuelConsumption", 0) / 10
            elif key.endswith("0002"):
                return tripSum.get("electricConsumption", 0) / 10
            elif key.endswith("0003"):
                return tripSum.get("gasConsumption", 0) / 10
            elif key.endswith("0004"):
                return tripSum.get("travelTime", 0)
            elif key.endswith("0005"):
                return tripSum.get("distance", 0)
            elif key.endswith("0006"):
                return tripSum.get("tripEnd", 0)
            else:
                self._LOGGER.warning(f"Unknown trip sum value key {key}.")
                return tripSum

        keys_set = set(key) if isinstance(key, (list, tuple, set)) else ({key} if key else set())
        fn_set = set(field_names) if field_names else set()

        for element in reversed(self.currentData.get("Data", [])):
            elem_key = element.get("key", "")
            elem_name = element.get("dataFieldName", "")
            if elem_key in keys_set or (fn_set and elem_name in fn_set):
                if "value" in element:
                    if conversion is None:
                        return element.get("value", "")
                    elif conversion == EUDA_DATA_CONVERSION_FLOAT:
                        try:
                            return float(element.get("value", "0"))
                        except Exception:
                            return 0.0
                    elif conversion == EUDA_DATA_CONVERSION_INT:
                        value = str(element.get("value", "0"))
                        try:
                            if "s" in value:
                                return int(int(value[:value.find("s")]) / 60)
                            elif "min" in value:
                                return int(value[:value.find("min")])
                            return int(float(value))
                        except Exception:
                            return 0
                    elif conversion == EUDA_DATA_CONVERSION_INT_INVERT:
                        try:
                            return -int(float(element.get("value", "0")))
                        except Exception:
                            return 0
                    elif conversion == EUDA_DATA_CONVERSION_BOOL:
                        val_str = str(element.get("value", "")).lower()
                        return val_str in ("true", "on", "locked", "connected", "charging", "charginghvbattery", "open", "valid", "1")
                    elif conversion == EUDA_DATA_CONVERSION_DIVIDE_BY_10:
                        try:
                            return float(element.get("value", "0")) / 10.0
                        except Exception:
                            return 0.0
                    elif conversion == EUDA_DATA_CONVERSION_KELVIN_TO_CELSIUS:
                        try:
                            return float(element.get("value", "0.0")) / 10 - 273.1
                        except Exception:
                            return 0.0
                    else:
                        return element.get("value", "")
        return None

    def isEUDADataFieldSupported(
        self, key: str, values_to_treat_as_unsupported: set=set()
    ) -> bool:
        """Return true if the EUDA data field identified by key is supported."""
        if key == "00000000-0000-0000-0000-0000":
            return True
        elif key == "01000000-0000-0000-0000-0000" and self.currentData != {}:
            return True
        elif (
            key.startswith("10000000-0000") or key.startswith("11000000-0000")
        ) and self.tripData != {}:
            return True
        for element in self.currentData.get("Data", []):
            if element.get("key", "") == key:
                if "value" in element:
                    if element.get("value", "") not in values_to_treat_as_unsupported:
                        return True
        if not self.currentData.get("Data", []):
            return (
                key in self._defined_EUDA_keys
                or key == "00000000-0000-0000-0000-0000"
                or key == "01000000-0000-0000-0000-0000"
            )
        return False

    @property
    def getEUDAFileTimestamp(self) -> datetime | None:
        """Return timestamp form the newest EUDA file (from the filename)."""
        ts = self.currentData.get("timeStamp", None)
        if ts and isinstance(ts, datetime) and ts != datetime.min:
            if ts.tzinfo is None:
                return ts.replace(tzinfo=timezone.utc)
            return ts
        return None

    def getEUDADataFieldTimestamp(self, key: str | None = None) -> str:
        """Return timestamp for an EUDA data field identified by key."""
        for element in self.currentData.get("Data", []):
            if element.get("key", "") == key:
                if "timestampUtc" in element:
                    return element.get("timestampUtc", "unknown")
        return "unknown"

    def getEUDADataFieldUnit(self, key: str) -> str:
        """Return the unit computed from value of an unit EUDA data field identified by key."""
        for element in self.currentData.get("Data", []):
            if element.get("key", "") == key:
                if "value" in element:
                    unitInFile = element.get("value", "")
                    if unitInFile == "MILES":
                        return "mi"
                    elif unitInFile == "KM":
                        return "km"
                    elif unitInFile == "CHARGE_RATE_UNIT_KM_PER_H":
                        return "km/h"
                    elif unitInFile == "CHARGE_RATE_UNIT_KM_PER_MIN":
                        return "km/min"
                    elif unitInFile == "CHARGE_RATE_UNIT_MILES_PER_H":
                        return "mi/h"
                    elif unitInFile == "CHARGE_RATE_UNIT_MILES_PER_MIN":
                        return "mi/min"
                    elif unitInFile == "CHARGE_RATE_UNIT_INVALID":
                        self._LOGGER.info(
                            f"Found unit field {key} in EUDA file, but it had the value {unitInFile}."
                        )
                        return ""
                    else:
                        self._LOGGER.warning(
                            f"Found unit field {key} in EUDA file, but it had the yet unknown value {unitInFile}. Please open an issue."
                        )
                        return ""
                else:
                    self._LOGGER.info(
                        f"Found unit field {key} in EUDA file, but it had no value."
                    )
                    return ""
        self._LOGGER.info(f"Could not find unit field {key} in EUDA file.")
        return ""

    @property
    def getEUDADataAllUndefinedFields(self) -> dict:
        """Return a dictionary of all EUDA data fields found in EUDA files but not defined in EUDA_DATA_DICT."""
        undefinedFields = {}
        for element in self.currentData.get("Data", []):
            if (
                element.get("key", "") not in self._defined_EUDA_keys
                and element.get("key", "") not in EUDA_DATA_NO_SHOW_SET
            ):
                if element.get("dataFieldName", "") != "":
                    undefinedFields[
                        element.get("dataFieldName", "-dataFieldNameMissing-")
                    ] = element.get("value", "")
                else:
                    undefinedFields[element.get("key", "-dataFieldNameMissing-")] = (
                        element.get("value", "")
                    )
        return dict(sorted(undefinedFields.items()))

    def getLatestTripSumValues(self, sumType: str = "day") -> dict:
        """Return the calculated latest daily sum values from the trip history."""
        if sumType == "month":
            if self._tripSumDictMonth == {}:
                self._LOGGER.warning(
                    "tripSumDictMonth is empty when getLatestTripSumValues is called. Recalculating."
                )
                self.calcLatestTripSumValues(sumType=sumType)
            return self._tripSumDictMonth
        else:
            if self._tripSumDictDay == {}:
                self._LOGGER.warning(
                    "tripSumDictDay is empty when getLatestTripSumValues is called. Recalculating."
                )
                self.calcLatestTripSumValues(sumType=sumType)
            return self._tripSumDictDay

    def calcLatestTripSumValues(self, sumType: str = "day"):
        """Calculate the latest daily sum values from the trip history."""
        try:
            SumDictType = TypedDict(
                "SumDictType",
                {
                    "startMileage": int,
                    "fuelConsumption": int,
                    "electricConsumption": int,
                    "gasConsumption": int,
                    "travelTime": int,
                    "distance": int,
                    "tripEnd": datetime,
                },
            )
            sumDict: SumDictType = {
                "startMileage": 1000000,
                "fuelConsumption": 0,
                "electricConsumption": 0,
                "gasConsumption": 0,
                "travelTime": 0,
                "distance": 0,
                "tripEnd": datetime.min,
            }
            if self.tripData != {}:
                element = self.tripData[list(self.tripData)[-1]]
                # Set the minTimeStamp
                latestTripEnd = element.get("tripEnd", datetime.min)
                if sumType == "month":
                    latestTripEnd = latestTripEnd.replace(day=1)
                minTimeStamp = datetime.combine(
                    latestTripEnd.date(), datetime.min.time()
                ).astimezone(None)
                sumDict["tripEnd"] = minTimeStamp

                for element in self.tripData.values():
                    if minTimeStamp <= element.get("tripEnd", ""):
                        if (
                            element.get("startMileage", 1000000)
                            < sumDict["startMileage"]
                        ):
                            sumDict["startMileage"] = element.get(
                                "startMileage", 1000000
                            )
                        sumDict["travelTime"] = sumDict["travelTime"] + element.get(
                            "travelTime", 0
                        )
                        sumDict["distance"] = sumDict["distance"] + element.get(
                            "distance", 0
                        )
                        sumDict["fuelConsumption"] = sumDict[
                            "fuelConsumption"
                        ] + element.get("fuelConsumption", 0) * element.get(
                            "distance", 0
                        )
                        sumDict["electricConsumption"] = sumDict[
                            "electricConsumption"
                        ] + element.get("electricConsumption", 0) * element.get(
                            "distance", 0
                        )
                        sumDict["gasConsumption"] = sumDict[
                            "gasConsumption"
                        ] + element.get("gasConsumption", 0) * element.get(
                            "distance", 0
                        )

                if sumDict["distance"] > 0:
                    sumDict["fuelConsumption"] = int(
                        sumDict["fuelConsumption"] / sumDict["distance"] + 0.5
                    )
                    sumDict["electricConsumption"] = int(
                        sumDict["electricConsumption"] / sumDict["distance"] + 0.5
                    )
                    sumDict["gasConsumption"] = int(
                        sumDict["gasConsumption"] / sumDict["distance"] + 0.5
                    )

            if sumType == "month":
                self._tripSumDictMonth = sumDict
            else:
                self._tripSumDictDay = sumDict
        except Exception as error:
            self._LOGGER.warning(
                f"Failed to calculate latest trip sum values  - {error}"
            )


def GetModelFromNickName(nickName: str) -> str:
    posSeparator = nickName.find(" ")
    if posSeparator > 0 and len(nickName) > posSeparator:
        return nickName[posSeparator + 1 :]
    return ""
