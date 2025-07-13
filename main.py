# Rightmove API scraper
# Daniel Evans

# to get this going you need need to create a cloud app here, set up the oauth consent screen and credentials - which ultimately lets you download a credentials.json for the app.
# https://console.cloud.google.com/getting-started?authuser=1

# Requires a credentials.json for the gmail api. Should be able to look it up but feel free to ask me

# if set up properly, running the script should prompt an authentication window in the browser
# to allow the app to send emails on your behalf

# note that `send emails on your behalf` needs to be enabled in the google dev application, and the email you want to use needs to be registered.


from __future__ import annotations

__pkgname__ = "rm-scraper"
__version__ = "0.0.1"
__author__ = "D Evans"
__built_for__ = "BUILT_FOR_NAME_PENDING"


def disable_quickedit():
    '''
    Disable quickedit mode on Windows terminal. quickedit prevents script to
    run without user pressing keys..'''
    import os
    if not os.name == 'posix':
        try:
            import msvcrt
            import ctypes
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            device = r'\\.\CONIN$'
            with open(device, 'r') as con:
                hCon = msvcrt.get_osfhandle(con.fileno())
                kernel32.SetConsoleMode(hCon, 0x0080)
        except Exception as e:
            print('Cannot disable QuickEdit mode! ' + str(e))
            print('.. As a consequence the script might be automatically\
            paused on Windows terminal')

    pass

disable_quickedit()

import requests
import time
from datetime import datetime
import tomllib
from dataclasses import dataclass, field
import sys
import traceback
from property import Property
import send_email
from pathlib import Path

MIN_TIME_BETWEEN_REQUESTS = 60

if getattr(sys, "frozen", False):
    BASE_PATH = Path(sys._MEIPASS)
    WD = Path(sys.executable).parent
else:
    BASE_PATH = Path(__file__).parent
    WD = Path(__file__).parent

CREDENTIALS_FP = BASE_PATH / "credentials.json"
CONFIG_FP = WD / "config.toml"
MAIN_LOG_FP = WD / "main.log"


@dataclass
class Config:
    recipients: str
    subject: str

    locationIdentifier: str
    maxBedrooms: int
    minBedrooms: int
    maxPrice: int
    radius: float
    numberOfPropertiesPerPage: int = field(default=500)
    sortType: int = field(default=6)
    index: int = field(default=24)
    includeLetAgreed: str = field(default="false")
    viewType: str = field(default="LIST")
    channel: str = field(default="RENT")
    areaSizeUnit: str = field(default="sqft")
    currencyCode: str = field(default="GBP")
    isFetching: str = field(default="false")

    timeBetweenRequests: int = field(default=60)

    @staticmethod
    def load():
        try:
            with open(CONFIG_FP, "rb") as f:
                data = tomllib.load(f)
            return Config(**data)
        except FileNotFoundError as e:
            print(f"File not found at {CONFIG_FP}")
            raise

    @property
    def paramsdict(self):
        d = {
            "locationIdentifier": self.locationIdentifier,
            "maxBedrooms": self.maxBedrooms,
            "minBedrooms": self.minBedrooms,
            "maxPrice": self.maxPrice,
            "radius": self.radius,
            "numberOfPropertiesPerPage": self.numberOfPropertiesPerPage,
            "sortType": self.sortType,
            "index": self.index,
            "includeLetAgreed": self.includeLetAgreed,
            "viewType": self.viewType,
            "channel": self.channel,
            "areaSizeUnit": self.areaSizeUnit,
            "currencyCode": self.currencyCode,
            "isFetching": self.isFetching,
        }
        return d


CFG = Config.load()
PARAMS = CFG.paramsdict

URL = "https://www.rightmove.co.uk/api/_search"

# most of the headers aren't needed
HEADERS = {
    "Accept": "application/json, text/plain, */*",
}


def property_summary(prop: Property) -> str:
    # writes the property summary in trash html but does the trick
    s = f"""
<p>
    <h2>{prop.summary}</h2>
    <li>Price: {prop.price['amount']}</li>
    <li>Bedrooms: {prop.bedrooms}</li>
    <li>Bathrooms: {prop.bathrooms}</li>
    <li>Display Address: {prop.displayAddress}</li>
    <li>Property URL: <a href='{"rightmove.co.uk" + str(prop.propertyUrl)}'>{"rightmove.co.uk" + str(prop.propertyUrl)}</a></li>
    <img src={prop.propertyImages["mainImageSrc"]} alt="" width="400" height="300">
</p>
"""
    return s


def create_message(properties: list[Property]) -> str:
    # creates html for a list of properties
    string = ""

    for p in properties:
        string = string + property_summary(p)
    pass
    return string


def main(history_ids: set[str]) -> tuple[list[Property], list[Property]]:
    properties = []

    response = requests.get(URL, headers=HEADERS, params=PARAMS)
    data = response.json()

    # print(len(data["properties"]))

    for kwargs in data["properties"]:
        properties.append(Property(**kwargs))

    prev_properties_id = history_ids
    # new properties should have an id not in the history variable
    new_properties_id = set([p.id for p in properties]).difference(prev_properties_id)

    new_properties = list(
        filter(
            lambda p: p.id in new_properties_id,
            properties,
        )
    )

    # print(f"{len(new_properties)} new properties {datetime.now()}")

    return (
        properties,
        new_properties,
    )


properties = []
not_first = False

history_ids = set()

res = ""

msg = f"""
                                                    
     ___  _____  ___  ___  ___  ___  ___  ___  ___  ___ 
    |  _||     ||___||_ -||  _||  _|| .'|| . || -_||  _|
    |_|  |_|_|_|     |___||___||_|  |__,||  _||___||_|  
                                         |_|            
    
    {__pkgname__} v{__version__}
    Copyright 2025 (c) D.Evans 

    Use is exclusively reserved for {__built_for__}.

    Enjoy :)

"""
if __name__ == "__main__":
    send_email.initialize(CREDENTIALS_FP)

    print(msg)

    try:
        print("Will send emails to the following:")
        print(f"{CFG.recipients}")

        while True:
            properties, new_properties = main(history_ids)
            time_at_response = datetime.now()

            with open(MAIN_LOG_FP, "a") as f:
                print(f"{len(new_properties)} found at {datetime.now()}...")
                f.write(
                    f"LOG {time_at_response}:{len(new_properties)} found, {[p.id for p in new_properties]}\n"
                )

            history_ids = history_ids.union([p.id for p in properties])

            if new_properties:
                html_content = create_message(new_properties)
                html_content = html_content + f"<p>{time_at_response}</p>"
                print(f"Sending email...")
                if not_first:
                    send_email.send_html_email(
                        subject=CFG.subject,
                        recipient=CFG.recipients,
                        html_content=html_content,
                    )
                    print(f"Email sent")
                    print("")
            else:
                print("No new properties found.")
                print("")

            not_first = True
            time.sleep(max(MIN_TIME_BETWEEN_REQUESTS, CFG.timeBetweenRequests))

    except KeyboardInterrupt as e:
        print(f"Keyboard Interrupt {e}")
        input("Press Enter to Exit...")
        print("Exiting...")
        sys.exit(0)
    except Exception as e:
        print("")
        print(f"Exception occurred: {e}")
        _, _, tb = sys.exc_info()
        trace = traceback.format_exc()
        print("")
        print("Traceback:")
        print(trace)
        print("")
        input("Press Enter to Exit...")
        print("Exiting...")
        sys.exit(0)
