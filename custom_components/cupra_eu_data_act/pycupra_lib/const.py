"""Constants for pycupra library."""

DATA_DIRECTORY = "pycupra_data"

BASE_SESSION = "https://ola.prod.code.seat.cloud.vwgroup.com"
BASE_AUTH = "https://identity.vwgroup.io"

# Data used in communication
CLIENT_LIST = {
    "seat": {
        "CLIENT_ID": "99a5b77d-bd88-4d53-b4e5-a539c60694a3@apps_vw-dilab_com",
        "SCOPE": "openid profile nickname birthdate phone",
        "REDIRECT_URL": "seat://oauth-callback",
        "TOKEN_TYPES": "code id_token token",
    },
    "cupra": {
        "CLIENT_ID": "3c756d46-f1ba-4d78-9f9a-cff0d5292d51@apps_vw-dilab_com",
        "CLIENT_SECRET": "eb8814e641c81a2640ad62eeccec11c98effc9bccd4269ab7af338b50a94b3a2",
        "SCOPE": "openid profile nickname birthdate phone",
        "REDIRECT_URL": "cupra://oauth-callback",
        "TOKEN_TYPES": "code id_token token",
    },
}


XCLIENT_ID = "3c756d46-f1ba-4d78-9f9a-cff0d5292d51@apps_vw-dilab.com"
XAPPVERSION_CUPRA = "2.18.0"
XAPPVERSION_SEAT = "2.18.0"
XAPPNAME_CUPRA = "com.cupra.mycupra"
XAPPNAME_SEAT = "com.seat.myseat"
USER_AGENT_CUPRA = "OLACupra/2.18.0 (Android 14; SM-G960F; samsung) Mobile" 
USER_AGENT_SEAT = "OLASeat/2.18.0 (Android 14; SM-G960F; samsung) Mobile" 
APP_URI = "https://ola.prod.code.seat.cloud.vwgroup.com"

HEADERS_SESSION = {
    "seat": {
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Accept-charset": "UTF-8",
        "Accept": "application/json",
        #'X-Client-Id': XCLIENT_ID,
        #'X-App-Version': XAPPVERSION,
        #'X-App-Name': XAPPNAME,
        "app-version": XAPPVERSION_SEAT,
        "app-brand": "seat",
        "app-market": "android",
        "origin": "app",
        "User-Agent": USER_AGENT_SEAT,
        #'User-ID': '?????', # to be set later
        "Accept-Language": "en_GB",
    },
    "cupra": {
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Accept-charset": "UTF-8",
        "Accept": "application/json",
        #'X-Client-Id': XCLIENT_ID,
        #'X-App-Name': XAPPNAME,
        "app-version": XAPPVERSION_CUPRA,
        "app-brand": "cupra",
        "app-market": "android",
        "origin": "app",
        "User-Agent": USER_AGENT_CUPRA,
        #'User-ID': '?????', # to be set later,
        "Accept-Language": "en_GB",
    },
}

HEADERS_AUTH = {
    "seat": {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": USER_AGENT_SEAT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "x-requested-with": XAPPNAME_SEAT,
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        #'X-App-Name': XAPPNAME
    },
    "cupra": {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": USER_AGENT_CUPRA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "x-requested-with": XAPPNAME_CUPRA,
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        #'X-App-Name': XAPPNAME
    },
}

TOKEN_HEADERS = {
    "seat": {
        "Accept": "application/json",
        "X-Platform": "Android",
        #'X-Language-Id': 'XX',
        #'X-Country-Id': 'XX',
        #'Accept-Language': 'XX',
        "Accept-Charset": "UTF-8",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip",
        "User-Agent": USER_AGENT_SEAT,
        "app-version": XAPPVERSION_SEAT,
        "app-brand": "seat",
        "app-market": "android",
        #'User-ID': '?????', # to be set later
        "Authorization": "Bearer",
    },
    "cupra": {
        "Accept": "application/json",
        "X-Platform": "Android",
        #'X-Language-Id': 'XX',
        #'X-Country-Id': 'XX',
        #'Accept-Language': 'XX',
        "Accept-Charset": "UTF-8",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip",
        "User-Agent": USER_AGENT_CUPRA,
        "app-version": XAPPVERSION_CUPRA,
        "app-brand": "cupra",
        "app-market": "android",
        #'User-ID': '?????', # to be set later
        "Authorization": "Bearer",
    },
}

# ERROR_CODES = {
#    '11': 'Charger not connected'
# }

### API Endpoints below, not yet in use ###
# API AUTH endpoints
AUTH_OIDCONFIG = "https://identity.vwgroup.io/.well-known/openid-configuration"  # OpenID configuration
AUTH_TOKEN = "https://identity.vwgroup.io/oidc/v1/token"  # Endpoint for exchanging code for token
AUTH_REFRESH = "https://ola.prod.code.seat.cloud.vwgroup.com/authorization/api/v1/token"  # Endpoint for token refresh (also used for exchanging code for token for Seat)
AUTH_TOKENKEYS = "https://identity.vwgroup.io/oidc/v1/keys"  # Signing keys for tokens

# API endpoints
API_MBB_STATUSDATA = (
    "https://customer-profile.vwgroup.io/v3/customers/{userId}/mbbStatusData"
)
API_PERSONAL_DATA = (
    "https://customer-profile.vwgroup.io/v3/customers/{userId}/personalData"
)
# Other option for personal data is '{baseurl}/v1/users/{self._user_id}'

API_VEHICLES = "{APP_URI}/v2/users/{userId}/garage/vehicles"  # Garage info
API_MYCAR = "{baseurl}/v5/users/{userId}/vehicles/{vin}/mycar"  # Vehicle status report
API_RANGES = "{baseurl}/v1/vehicles/{vin}/ranges"  # Range information
API_CHARGING = "{baseurl}/v1/vehicles/{vin}/charging"  # Vehicle charging information
API_CHARGING_PROFILES = (
    "{baseurl}/vehicles/{vin}/charging/profiles"  # Vehicle charging profile information
)
# API_OPERLIST = '{homeregion}/api/rolesrights/operationlist/v3/vehicles/{vin}'                       # API Endpoint for supported operations
# API_CHARGER = 'fs-car/bs/batterycharge/v1/{BRAND}/{COUNTRY}/vehicles/{vin}/charger'                 # Charger data
API_CLIMATER_STATUS = (
    "{baseurl}/v1/vehicles/{vin}/climatisation/status"  # Climatisation data
)
API_CLIMATER = "{baseurl}/v2/vehicles/{vin}/climatisation"  # Climatisation data
API_CLIMATISATION_TIMERS = (
    "{baseurl}/vehicles/{vin}/climatisation/timers"  # Climatisation timers
)
API_DEPARTURE_TIMERS = (
    "{baseurl}/v1/vehicles/{vin}/departure-timers"  # Departure timers
)
API_DEPARTURE_PROFILES = (
    "{baseurl}/v1/vehicles/{vin}/departure/profiles"  # Departure profiles
)
API_POSITION = "{baseurl}/v1/vehicles/{vin}/parkingposition"  # Position data
API_POS_TO_ADDRESS = (
    "https://maps.googleapis.com/maps/api/directions/json?origin={lat},{lon}"
    "&destination={lat},{lon}&traffic_model=best_guess&departure_time=now"
    "&language=de&key={apiKeyForGoogle}&mode=driving"
)
API_TRIP_V1 = (
    "{baseurl}/v1/vehicles/{vin}/driving-data/{dataType}?from="
    "1970-01-01T00:00:00Z&to=2099-12-31T09:59:01Z"  
    # Old trip statistics (whole history) SHORT/LONG/CYCLIC (WEEK only with from)
)
API_TRIP = (
    "{baseurl}/v2/vehicles/{vin}/driving-data/CUSTOM?from={startDate}T00:00:00Z"
    "&to={endDateTime}&distanceUnit=km&speedUnit=kmph"  
    # Trip statistics (whole history) SHORT/LONG/CYCLIC (WEEK only with from)
)
API_MILEAGE = "{baseurl}/v1/vehicles/{vin}/mileage"  # Total km etc
API_MAINTENANCE = "{baseurl}/v1/vehicles/{vin}/maintenance"  # Inspection information
API_MEASUREMENTS = "{baseurl}/v1/vehicles/{vin}/measurements/engines"  # ???
API_STATUS = (
    "{baseurl}/v2/vehicles/{vin}/status"  # Status information like locks and windows
)
API_LOCK_UNLOCK_ENABLED = (
    "{baseurl}/settings/api/v2/settings/remote-lock-unlock-enabled?vin={vin}&region=US"
    "&enrolment-country={enrolmentCountry}&user-role={userRole}"  
    # Is remote lock/unlock enabled?
)
API_WARNINGLIGHTS = "{baseurl}/v3/vehicles/{vin}/warninglights"  # ???
API_SHOP = "{baseurl}/v1/shop/vehicles/{vin}/articles"  # ???
# API_ACTION = '{baseurl}/v1/vehicles/{vin}/{action}/requests/{command}'                               # Actions (e.g. ActionCharge="charging", ActionChargeStart="start",ActionChargeStop="stop")
API_RELATION_STATUS = (
    "{baseurl}/v1/users/{userId}/vehicles/{vin}/relation-status"  # ???
)
API_INVITATIONS = "{baseurl}/v1/user/{userId}/invitations"  # ???
API_CAPABILITIES = "{APP_URI}/v1/user/{userId}/vehicle/{vin}/capabilities"  # ???
# API_CAPABILITIES_MANAGEMENT = '{API_CAPABILITIES}/management'                                        # ???
API_IMAGE = "{baseurl}/v2/vehicles/{vin}/renders"
API_HONK_AND_FLASH = "{baseurl}//v1/vehicles/{vin}/honk-and-flash"
API_ACCESS = "{baseurl}//v1/vehicles/{vin}/access/{action}"  # to lock or unlock vehicle
API_REQUESTS = "{baseurl}/vehicles/{vin}/{capability}/requests"
API_REFRESH = "{baseurl}/v1/vehicles/{vin}/vehicle-wakeup/request"
API_SECTOKEN = "{baseurl}/v2/users/{userId}/spin/verify"
API_DESTINATION = "{baseurl}/v1/users/vehicles/{vin}/destination"
API_LITERALS = "{APP_URI}/v1/content/apps/my-cupra/literals/{language}"  # Message texts in different langauages, e.g. 'en_GB'
API_ACTIONS = "{baseurl}/v1/vehicles/{vin}/{capability}/actions"  # capability e.g. 'charging', mode (e.g. 'update-settings') will be added as postfix
API_AUXILIARYHEATING = "{baseurl}/v1/vehicles/{vin}/auxiliary-heating"  # action (start/stop) will be added as postfix

# Still to analyse if needed
#'{baseurl}/settings/api/v1?vin={vin}&vehicle-model=LeonST&region=US&enrolment-country=DE&platform=MOD3'
#'{baseurl}/v1/users/{self._user_id}/vin/{vin}/terms-and-conditions'
#'{baseurl}/v2/subscriptions'
#'{baseurl}/v1/users/{self._user_id}/vehicles/{vin}/leads/history'
#'{baseurl}/v1/users/{self._user-id}/vehicles/{vin}/consents/xxcryptickeyxxx?locale=en_DE' #{"userId":"xxxxxxx","locale":"en_DE","error":{"title":"Consent failed to load.","detail":"CUPRAApp_ME3_Vehicle_VehiclePermissions_MainViewAccepted_Low_Type1_Wrong"}}

API_CONNECTION = "{APP_URI}/v1/vehicles/{vin}/remote-availability"  # until 26.03.2026 '{APP_URI}/vehicles/{vin}/connection'
# API_CONSENTS='{APP_URI}/v1/users/{self._user_id}/consents'
API_PSP = "{baseurl}/v2/users/{userId}/vehicles/{vin}/psp"  # primary service provider (Werkstatt)
API_USER_INFO = "https://identity-userinfo.vwgroup.io/oidc/userinfo"  # {"sub":"xxx","name":"xxx","given_name":"xxx","family_name":"xxx","nickname":"xxx","email":"###","email_verified":true,"birthdate":"###","updated_at":123456789,"picture":"https://customer-pictures.vwgroup.io/v1/###/profile-picture"}

PUBLIC_MODEL_IMAGES_SERVER = "prod-ola-public-bucket.s3.eu-central-1.amazonaws.com"  # non-indivdual model images are on this server

# Constants for firebase connection
FCM_PROJECT_ID = "ola-apps-prod"
FCM_APP_ID = {
    "cupra": "1:530284123617:android:9b9ba5a87c7ffd37fbeea0",
    "seat": "1:530284123617:android:d6187613ac3d7b08fbeea0",
}
FCM_API_KEY = "AIzaSyCoSp1zitklb1EDj5yQumN0VNhDizJQHLk"
FIREBASE_STATUS_NOT_INITIALISED = 0
FIREBASE_STATUS_ACTIVATED = 1
FIREBASE_STATUS_NOT_WANTED = -2
FIREBASE_STATUS_ACTIVATION_FAILED = -1
FIREBASE_STATUS_ACTIVATION_STOPPED = -3

# Sum types for trip statistics
SUMTYPE_DAILY = "daily"
SUMTYPE_MONTHLY = "monthly"

# Constants for EUDA connection
EUDA_CLIENT_LIST= {
    "cupra": {
        "CLIENT_ID": "f85e5b69-e3b2-43aa-9c0d-1b7d0e0b576f@apps_vw-dilab_com",
        "SCOPE": "openid profile cars",
        "REDIRECT_URL": "https://eu-data-act.drivesomethinggreater.com/login",
    },
    "seat": {
        "CLIENT_ID": "f85e5b69-e3b2-43aa-9c0d-1b7d0e0b576f@apps_vw-dilab_com",
        "SCOPE": "openid profile cars",
        "REDIRECT_URL": "https://eu-data-act.drivesomethinggreater.com/login",
    },
    "audi": {
        "CLIENT_ID": "cc29b87a-5e9a-4362-aecf-5adea6b01bbb@apps_vw-dilab_com",
        "SCOPE": "openid profile cars",
        "REDIRECT_URL": "https://eu-data-act.drivesomethinggreater.com/login",
    },
    "skoda": {
        "CLIENT_ID": "3ea88bf9-1d4e-4a68-b3ad-4098c1f1d246@apps_vw-dilab_com",
        "SCOPE": "openid profile cars",
        "REDIRECT_URL": "https://eu-data-act.drivesomethinggreater.com/login",
    },
    "volkswagen_passenger_cars": {
        "CLIENT_ID": "9b58543e-1c15-4193-91d5-8a14145bebb0@apps_vw-dilab_com",
        "SCOPE": "openid profile cars",
        "REDIRECT_URL": "https://eu-data-act.drivesomethinggreater.com/login",
    },
}

EUDA_HEADERS_SESSION = {
    "Connection": "keep-alive",
    "Content-Type": "*/*",  #'application/json',
    "Accept-charset": "UTF-8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
    "Referer": "https://eu-data-act.drivesomethinggreater.com/de/en/user.html",
    #'User-ID': '?????', # to be set later
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
}

EUDA_HEADERS_AUTH = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Referer": "https://eu-data-act.drivesomethinggreater.com/de/en/login.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
}

# Urls for EUDA connection
EUDA_AUTH_OIDC = "https://identity.vwgroup.io/oidc/v1/authorize"  # Authorization endpoint for EUDA login
EUDA_AUTH_ISSUER = "https://identity.vwgroup.io"  # Authorization issuer for EUDA login

EUDA_BASE_URL = "https://eu-data-act.drivesomethinggreater.com"
EUDA_API_VEHICLES = "{baseurl}/proxy_api/consent/me/vehicles?viewPosition={viewPos}"  # Endpoint to get vehicles
EUDA_API_FILE_DOWNLOAD = (
    "{baseurl}/proxy_api/euda-apim/datadelivery/vehicles/{vin}/{id}/download"  # Endpoint to download a data file
)
EUDA_API_FILE_LIST = (
    "{baseurl}/proxy_api/euda-apim/datadelivery/vehicles/{vin}/{id}/list"  # Endpoint to read a list of available files
)
EUDA_API_DATACLUSTERS = (
    "{baseurl}/proxy_api/euda-apim/datarequest/vehicles/{vin}/metadata/{type}"  # Endpoint to read data cluster information
)
EUDA_URL_DETAILS = "{baseurl}/content/euda/de/en/user/details?vin={vin}"

EUDA_API_TOKEN = "{baseurl}/libs/granite/csrf/token.json"
EUDA_API_PERMISSION_CHECK = "{baseurl}/services/permissioncheck"
EUDA_API_LOGOUT = "{baseurl}/services/logout"  # still in test

# Keys for Data of the EUDA portal
EUDA_SHORT_TERM_DATA_START_MILEAGE_KEY = "ecd266dd-f536-39c2-a575-352216b87f39"
EUDA_SHORT_TERM_DATA_MILEAGE_KEY = "9f55581a-4fa2-3570-9c9e-b80d210b9a42"
EUDA_SHORT_TERM_DATA_TRAVEL_TIME_KEY = "f0890c07-e62e-32dc-ab3b-80431f070b13"
EUDA_SHORT_TERM_DATA_AVERAGE_ELECTR_ENGINE_CONSUMPTION_KEY = (
    "3b1bdf91-8e59-333a-93ed-f8e5a980bc96"
)
EUDA_SHORT_TERM_DATA_AVERAGE_FUEL_CONSUMPTION_KEY = (
    "a0ee824b-9a53-34ee-8107-3ed94684efa7"
)
EUDA_SHORT_TERM_DATA_AVERAGE_GAS_CONSUMPTION_KEY = (
    "bdf31409-b799-3969-8199-e305082aabf2"
)
EUDA_LONG_TERM_DATA_START_MILEAGE_KEY = "2bfaa641-c972-3816-ae7c-73459bcd673d"
EUDA_LONG_TERM_DATA_MILEAGE_KEY = "f8eba56b-ee3f-3c48-b852-03c9b956053f"
EUDA_LONG_TERM_DATA_TRAVEL_TIME_KEY = "d2ad181b-511a-37d0-8109-e676e68c86b2"
EUDA_LONG_TERM_DATA_AVERAGE_ELECTR_ENGINE_CONSUMPTION_KEY = (
    "79f1709e-028d-3b3a-936e-bbef63b92969"
)
EUDA_LONG_TERM_DATA_AVERAGE_FUEL_CONSUMPTION_KEY = (
    "df531c6f-8897-3236-a760-5975322e7021"
)
EUDA_LONG_TERM_DATA_AVERAGE_GAS_CONSUMPTION_KEY = (
    "a326ae4c-afe8-3929-bf1a-b95ba7107c2f"
)
EUDA_LONG_TERM_DATA_AVERAGE_SPEED_KEY = "77838f59-786a-36fa-b1d4-47217a9fb40e"
EUDA_OUTSIDE_TEMPERATURE_KEY = "6810b781-e54a-35e8-af98-fcdefb54bac6"
EUDA_PARKING_BRAKE_KEY = "f8bbe94d-06e1-3311-bf8f-c0c99cc67d48"
EUDA_OIL_LEVEL_ADDITIONAL_OIL_LEVEL_KEY = "78e92351-cf56-3c15-96d3-9b63d62ca618"
EUDA_OIL_LEVEL_ACTUAL_LEVEL_KEY = "a3368611-8c63-3b7d-9d19-148a464c7a7b"

EUDA_DATA_CONVERSION_FLOAT = 0
EUDA_DATA_CONVERSION_INT = 1
EUDA_DATA_CONVERSION_BOOL = 2
EUDA_DATA_CONVERSION_DIVIDE_BY_10 = 3
EUDA_DATA_CONVERSION_KELVIN_TO_CELSIUS = 4
EUDA_DATA_CONVERSION_INT_INVERT = 5


EUDA_DATA_DICT = {
    "outside_temperature": {
        "attr": "outside_temperature",
        "name": "Outside temperature",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "device_class": "temperature",
        "key": "6810b781-e54a-35e8-af98-fcdefb54bac6",
        "conversion": EUDA_DATA_CONVERSION_KELVIN_TO_CELSIUS,
    },
    "oil_level": {
        "attr": "oil_level",
        "name": "Oil level",
        "icon": "mdi:oil",
        "unit": "%",
        #"device_class": "temperature",
        "key": "a3368611-8c63-3b7d-9d19-148a464c7a7b",
        "conversion": EUDA_DATA_CONVERSION_FLOAT,
    },
    "parking_brake": {
        "attr": "parking_brake",
        "name": "Parking brake",
        "icon": "mdi:car-brake-parking",
        #"unit": "%",
        #"device_class": "door",
        "key": "f8bbe94d-06e1-3311-bf8f-c0c99cc67d48",
        "conversion": EUDA_DATA_CONVERSION_BOOL,
    },
    "long_term_average_speed": {
        "attr": "long_term_average_speed",
        "name": "Last long average speed",
        "icon": "mdi:speedometer",
        "unit": "km/h",
        "device_class": "speed",
        "key": "77838f59-786a-36fa-b1d4-47217a9fb40e",
        "conversion": EUDA_DATA_CONVERSION_INT,
    },
    "long_term_average_electric_consumption": {
        "attr": "long_term_average_electric_consumption",
        "name": "Last long average electric consumption",
        "icon": "mdi:car-battery",
        "unit": "kWh/100km",
        "device_class": "energy_distance",
        "key": "79f1709e-028d-3b3a-936e-bbef63b92969",
        "conversion": EUDA_DATA_CONVERSION_DIVIDE_BY_10,
    },
    "long_term_average_fuel_consumption": {
        "attr": "long_term_average_fuel_consumption",
        "name": "Last long average fuel consumption",
        "icon": "mdi:fuel",
        "unit": "l/100km",
        #"device_class": "energy_distance",
        "key": "df531c6f-8897-3236-a760-5975322e7021",
        "conversion": EUDA_DATA_CONVERSION_DIVIDE_BY_10,
    },
    "long_term_average_gas_consumption": {
        "attr": "long_term_average_gas_consumption",
        "name": "Last long average gas consumption",
        "icon": "mdi:storage-tank",
        "unit": "kg/100km",
        #"device_class": "energy_distance",
        "key": "a326ae4c-afe8-3929-bf1a-b95ba7107c2f",
        "conversion": EUDA_DATA_CONVERSION_DIVIDE_BY_10,
    },
    "long_term_duration": {
        "attr": "long_term_duration",
        "name": "Last long duration",
        "icon": "mdi:clock",
        "unit": "min",
        "device_class": "duration",
        "key": "d2ad181b-511a-37d0-8109-e676e68c86b2",
        "conversion": EUDA_DATA_CONVERSION_INT,
    },
    "long_term_distance": {
        "attr": "long_term_distance",
        "name": "Last long length",
        "icon": "mdi:map-marker-distance",
        "unit": "km",
        "device_class": "distance",
        "key": "f8eba56b-ee3f-3c48-b852-03c9b956053f",
        "conversion": EUDA_DATA_CONVERSION_INT,
    },
    "short_term_average_electric_consumption": {
        "attr": "short_term_average_electric_consumption",
        "name": "Last short average electric consumption",
        "icon": "mdi:car-battery",
        "unit": "kWh/100km",
        "device_class": "energy_distance",
        "key": "3b1bdf91-8e59-333a-93ed-f8e5a980bc96",
        "conversion": EUDA_DATA_CONVERSION_DIVIDE_BY_10,
    },
    "short_term_average_fuel_consumption": {
        "attr": "short_term_average_fuel_consumption",
        "name": "Last short average fuel consumption",
        "icon": "mdi:fuel",
        "unit": "l/100km",
        #"device_class": "energy_distance",
        "key": "a0ee824b-9a53-34ee-8107-3ed94684efa7",
        "conversion": EUDA_DATA_CONVERSION_DIVIDE_BY_10,
    },
    "short_term_average_gas_consumption": {
        "attr": "short_term_average_gas_consumption",
        "name": "Last short average gas consumption",
        "icon": "mdi:storage-tank",
        "unit": "kg/100km",
        #"device_class": "energy_distance",
        "key": "bdf31409-b799-3969-8199-e305082aabf2",
        "conversion": EUDA_DATA_CONVERSION_DIVIDE_BY_10,
    },
    "short_term_duration": {
        "attr": "short_term_duration",
        "name": "Last short duration",
        "icon": "mdi:clock",
        "unit": "min",
        "device_class": "duration",
        "key": "f0890c07-e62e-32dc-ab3b-80431f070b13",
        "conversion": EUDA_DATA_CONVERSION_INT,
    },
    "short_term_distance": {
        "attr": "short_term_distance",
        "name": "Last short length",
        "icon": "mdi:map-marker-distance",
        "unit": "km",
        "device_class": "distance",
        "key": "9f55581a-4fa2-3570-9c9e-b80d210b9a42",
        "conversion": EUDA_DATA_CONVERSION_INT,
    },
    "battery_level": {
        "attr": "battery_level",
        "name": "Battery level",
        "icon": "mdi:battery",
        "unit": "%",
        "device_class": "battery",
        "key": "dc35366c-f5da-32a7-9674-5495a8082e69",
        "keys": [
            "dc35366c-f5da-32a7-9674-5495a8082e69",
            "506cb83e-f99f-3af3-bbeb-0429b69a78d9",
            "ac1108b1-b8cc-3db9-a663-03d387e42223",
        ],
        "field_names": [
            "battery_state_report.soc",
            "battery_level_HV.value",
            "state_of_charge",
        ],
        "conversion": EUDA_DATA_CONVERSION_INT,
    },
    "electric_range": {
        "attr": "electric_range",
        "name": "Electric range",
        "icon": "mdi:car-electric",
        "unit": "km",
        "device_class": "distance",
        "key": "eb2b3c59-6804-3463-ba3b-bcadc6954e08",
        "keys": [
            "eb2b3c59-6804-3463-ba3b-bcadc6954e08",
            "0ca40e18-0564-3eda-bcc0-7aee9ef44f04",
        ],
        "field_names": ["primary_range", "electric_range", "value"],
        "conversion": EUDA_DATA_CONVERSION_INT,
    },
    "mileage": {
        "attr": "mileage",
        "name": "Odometer",
        "icon": "mdi:speedometer",
        "unit": "km",
        "device_class": "distance",
        "key": "dfbf2da2-96f1-3231-a156-b7015f72aa1e",
        "keys": [
            "dfbf2da2-96f1-3231-a156-b7015f72aa1e",
            "75d65f00-5fa8-334a-826d-e73e91fe5c8d",
            "30cc36fd-71ca-3c09-9296-e94ebd47bd2b",
        ],
        "field_names": ["mileage.value", "mileage"],
        "conversion": EUDA_DATA_CONVERSION_INT,
    },
    "target_soc": {
        "attr": "target_soc",
        "name": "Target SoC",
        "icon": "mdi:battery-charging-90",
        "unit": "%",
        "device_class": "battery",
        "key": "5ec53403-2543-308d-9e95-e80a0e0b25be",
        "keys": [
            "5ec53403-2543-308d-9e95-e80a0e0b25be",
            "b3b04f31-b10e-38aa-b8ad-c0da7c06caea",
        ],
        "field_names": ["settings.target_soc"],
        "conversion": EUDA_DATA_CONVERSION_INT,
    },
    "charging_remaining_time": {
        "attr": "charging_remaining_time",
        "name": "Charging remaining time",
        "icon": "mdi:battery-charging",
        "unit": "min",
        "device_class": "duration",
        "key": "7405c11f-4d20-36d2-8381-18364aa1f444",
        "field_names": [
            "battery_state_report.remaining_charging_time_complete",
            "battery_state_report.remaining_charging_time_bulk",
            "remaining_charging_time",
        ],
        "conversion": EUDA_DATA_CONVERSION_INT,
    },
    "battery_temperature_max": {
        "attr": "battery_temperature_max",
        "name": "HV Battery temperature max",
        "icon": "mdi:thermometer-chevron-up",
        "unit": "°C",
        "device_class": "temperature",
        "key": "152115fd-c8c8-313b-a405-6198595ac699",
        "keys": [
            "152115fd-c8c8-313b-a405-6198595ac699",
            "dc4a4716-2205-352f-802f-8d7d59705c5b",
        ],
        "field_names": ["max_temperature"],
        "conversion": EUDA_DATA_CONVERSION_FLOAT,
    },
    "battery_temperature_min": {
        "attr": "battery_temperature_min",
        "name": "HV Battery temperature min",
        "icon": "mdi:thermometer-chevron-down",
        "unit": "°C",
        "device_class": "temperature",
        "key": "39869626-00af-318d-b5ed-eeff2916cf82",
        "keys": [
            "39869626-00af-318d-b5ed-eeff2916cf82",
            "374014c4-2fd5-3d73-ac75-7c949e726f00",
        ],
        "field_names": ["min_temperature"],
        "conversion": EUDA_DATA_CONVERSION_FLOAT,
    },
    "target_climatisation_temperature": {
        "attr": "target_climatisation_temperature",
        "name": "Target climatisation temperature",
        "icon": "mdi:thermometer-auto",
        "unit": "°C",
        "device_class": "temperature",
        "key": "db47598c-b798-353d-a8a8-9e5866d275de",
        "field_names": ["target_temperature", "target_climatisation_temperature"],
        "conversion": EUDA_DATA_CONVERSION_FLOAT,
    },
    "climatisation_status": {
        "attr": "climatisation_status",
        "name": "Climatisation status",
        "icon": "mdi:air-conditioner",
        "key": "1afa44b8-2dd0-34d0-8fbd-ceebd72dd493",
        "field_names": ["climatisation_state", "climatisation_status"],
    },
    "window_heating": {
        "attr": "window_heating",
        "name": "Window heating",
        "icon": "mdi:car-defrost-rear",
        "key": "59b70274-4df3-3e5c-80d9-10c26c57880e",
        "keys": [
            "59b70274-4df3-3e5c-80d9-10c26c57880e",
            "a894455d-2917-33cf-a9bd-d05846a14cfe",
        ],
        "field_names": ["window_heating_state", "window_heating"],
    },
    "mirror_heating": {
        "attr": "mirror_heating",
        "name": "Mirror heating enabled",
        "icon": "mdi:car-side",
        "key": "6b01af98-9b04-38cb-a2a6-3120cce7a162",
        "field_names": ["mirror_heating_state", "mirror_heating"],
        "conversion": EUDA_DATA_CONVERSION_BOOL,
    },
    "plug_connection_state": {
        "attr": "plug_connection_state",
        "name": "Plug connection state",
        "icon": "mdi:power-plug",
        "key": "17e75411-e651-3ba5-9358-6aab3b022581",
        "field_names": ["plug_state", "charging_plug1_connectionstate", "plug_connection_state"],
    },
    "plug_lock_state": {
        "attr": "plug_lock_state",
        "name": "Plug lock state",
        "icon": "mdi:lock",
        "key": "8ffe9a00-6916-3402-9b7e-fe659cf498e3",
        "field_names": ["lock_state", "plug_lock_state"],
    },
    "trunk_lid_status": {
        "attr": "trunk_lid_status",
        "name": "Trunk status",
        "icon": "mdi:car-back",
        "key": "c1a779dc-6dc7-38dd-8f46-a5ddf0d2c5f5",
        "field_names": ["decklid_status", "trunk_lid_status", "trunk_status"],
    },
    "hood_status": {
        "attr": "hood_status",
        "name": "Hood status",
        "icon": "mdi:car",
        "key": "e4c66263-aa68-3afc-9b9f-af7146c83277",
        "field_names": ["hood_status", "bonnet_status"],
    },
    "window_front_left": {
        "attr": "window_front_left",
        "name": "Window front left",
        "icon": "mdi:car-door",
        "key": "63bbeb15-1b73-3b7f-8c0a-6fac6851f98b",
        "field_names": ["window_front_left", "window_lift_front_left_status"],
    },
    "window_front_right": {
        "attr": "window_front_right",
        "name": "Window front right",
        "icon": "mdi:car-door",
        "key": "8733f7cc-f191-384b-8805-0ecbdb5ff45f",
        "field_names": ["window_front_right", "window_lift_front_right_status"],
    },
    "window_rear_left": {
        "attr": "window_rear_left",
        "name": "Window rear left",
        "icon": "mdi:car-door",
        "key": "d4e79704-e8a0-3e30-a865-5e44ca1d316f",
        "field_names": ["window_rear_left", "window_lift_rear_left_status"],
    },
    "window_rear_right": {
        "attr": "window_rear_right",
        "name": "Window rear right",
        "icon": "mdi:car-door",
        "key": "b95233db-0a75-3846-ba7c-1db17df235f6",
        "field_names": ["window_rear_right", "window_lift_rear_right_status"],
    },
    "service_inspection_days": {
        "attr": "service_inspection_days",
        "name": "Inspection due in",
        "icon": "mdi:wrench-clock",
        "unit": "d",
        "device_class": "duration",
        "key": "6cb4fe86-1407-315e-94c4-79b2d24123ab",
        "field_names": ["maintenance_interval__time_until_inspection.due_date", "service_inspection_days"],
        "conversion": EUDA_DATA_CONVERSION_INT,
    },
    "is_parked": {
        "attr": "is_parked",
        "name": "Is parked",
        "icon": "mdi:car-parking-lights",
        "key": "37af0223-6d24-3ba0-9ce9-f1701d247961",
        "field_names": ["is_parked", "parking_light_left", "parking_light_right"],
        "conversion": EUDA_DATA_CONVERSION_BOOL,
    },
    "is_connected": {
        "attr": "is_connected",
        "name": "Is connected",
        "icon": "mdi:access-point-network",
        "key": "4cbef03f-a75b-3fe9-a22f-f3fbbe8dd003",
        "field_names": ["is_connected", "state"],
        "conversion": EUDA_DATA_CONVERSION_BOOL,
    },
    "position_latitude": {
        "attr": "position_latitude",
        "name": "Parking latitude",
        "icon": "mdi:crosshairs-gps",
        "key": "ec0ab527-361b-3ada-820e-99f601f69d7b",
        "field_names": ["parking_latitude", "position_latitude"],
        "conversion": EUDA_DATA_CONVERSION_FLOAT,
    },
    "position_longitude": {
        "attr": "position_longitude",
        "name": "Parking longitude",
        "icon": "mdi:crosshairs-gps",
        "key": "61be015f-17b5-3b59-9c61-e3c66199514e",
        "field_names": ["parking_longitude", "position_longitude"],
        "conversion": EUDA_DATA_CONVERSION_FLOAT,
    },
}

EUDA_DATA_NO_SHOW_SET = (
    EUDA_LONG_TERM_DATA_START_MILEAGE_KEY,
    EUDA_SHORT_TERM_DATA_START_MILEAGE_KEY,
)
