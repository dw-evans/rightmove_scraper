# Rightmove API scraper
# Daniel Evans

# to get this going you need need to create a cloud app here, set up the oauth consent screen and credentials - which ultimately lets you download a credentials.json for the app.
# https://console.cloud.google.com/getting-started?authuser=1

# Requires a credentials.json for the gmail api. Should be able to look it up but feel free to ask me

# if set up properly, running the script should prompt an authentication window in the browser
# to allow the app to send emails on your behalf

# note that `send emails on your behalf` needs to be enabled in the google dev application, and the email you want to use needs to be registered.


from __future__ import annotations

import requests

import time
from datetime import datetime

from property import Property

from send_email import send_html_email

url = "https://www.rightmove.co.uk/api/_search"

# most of the headers aren't needed
headers = {
    "Accept": "application/json, text/plain, */*",
    # 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    # 'Connection': 'keep-alive',
    # 'Cookie': 'permuserid=2305231MSYX8HQ0AJCOW1HC39PQEDJOP; rmsessionid=1e20ab00-0309-40a3-8990-633b4444eeea; beta_optin=N:85:-1; RM_Register=C; TS019c0ed0=012f990cd36bb9684f9b9ff544d982bbe272668dbb85a9e9e31e42de9d346c796e20a9695a33e024446e196246f64395cacb5769ba; TS01826437=012f990cd36bb9684f9b9ff544d982bbe272668dbb85a9e9e31e42de9d346c796e20a9695a33e024446e196246f64395cacb5769ba; TPCmaxPrice=1400; TS01aff9d4=012f990cd34dbc4f309a7541c24046fef1c0102d69f48def0403cc2e1a5b01eefb53833a431da12bb8da523a3fd5aa1d0acbda8bb9; _gaRM1_ga=GA1.1.1996025758.1684826662; _gaRM=GA1.3.1996025758.1684826662; _gaRM_gid=GA1.3.148442785.1684826662; _dc_gtm_UA-3350334-63=1; TS01a07bd2=012f990cd36bb9684f9b9ff544d982bbe272668dbb85a9e9e31e42de9d346c796e20a9695a33e024446e196246f64395cacb5769ba; OptanonConsent=isIABGlobal=false&datestamp=Tue+May+23+2023+08%3A24%3A50+GMT%2B0100+(British+Summer+Time)&version=5.11.0&landingPath=https%3A%2F%2Fwww.rightmove.co.uk%2Fproperty-to-rent%2Ffind.html%3FsearchType%3DRENT%26locationIdentifier%3DREGION%255E219%26insId%3D1%26radius%3D0.0%26minPrice%3D%26maxPrice%3D1400%26minBedrooms%3D1%26maxBedrooms%3D2%26displayPropertyType%3D%26maxDaysSinceAdded%3D%26sortByPriceDescending%3D%26_includeLetAgreed%3Don%26primaryDisplayPropertyType%3D%26secondaryDisplayPropertyType%3D%26oldDisplayPropertyType%3D%26oldPrimaryDisplayPropertyType%3D%26letType%3D%26letFurnishType%3D%26houseFlatShare%3D&groups=1%3A1%2C3%3A0%2C4%3A0; _gaRM1_ga_G0CW62CSDJ=GS1.1.1684826662.1.1.1684826695.0.0.0',
    # 'Referer': 'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E219&maxBedrooms=2&minBedrooms=1&maxPrice=1400&index=24&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords=',
    # 'Sec-Fetch-Dest': 'empty',
    # 'Sec-Fetch-Mode': 'cors',
    # 'Sec-Fetch-Site': 'same-origin',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    # 'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"'
}

# this is a search across Bristol for 1-2 beds under £1400 pcm
params = {
    "locationIdentifier": "REGION^219",
    "maxBedrooms": 2,
    "minBedrooms": 1,
    "maxPrice": 1400,
    # this is capped at 500 - I never ran into more than around 160 so never needed send multiple requests or anything
    "numberOfPropertiesPerPage": 500,
    "radius": 0.0,
    "sortType": 6,
    "index": 24,
    "includeLetAgreed": "false",
    "viewType": "LIST",
    "channel": "RENT",
    "areaSizeUnit": "sqft",
    "currencyCode": "GBP",
    "isFetching": "false",
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


def create_message(properties: list[properties]) -> str:
    # creates html for a list of properties
    string = ""

    for p in properties:
        string = string + property_summary(p)
    pass

    return string


def main(history_ids: set[str]) -> tuple[list[Property], list[Property]]:
    properties = []

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    print(len(data["properties"]))

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

    print(f"{len(new_properties)} new properties {datetime.now()}")

    return (
        properties,
        new_properties,
    )


properties = []
not_first = False

history_ids = set()

res = ""


if __name__ == "__main__":
    try:
        while True:
            properties, new_properties = main(history_ids)
            time_at_response = datetime.now()

            with open("main.log", "a") as f:
                print(f"{len(new_properties)} found... sending email")
                f.write(
                    f"LOG {time_at_response}:{len(new_properties)} found, {[p.id for p in new_properties]}\n"
                )

            history_ids = history_ids.union([p.id for p in properties])

            if new_properties:
                html_content = create_message(new_properties)
                html_content = html_content + f"<p>{time_at_response}</p>"
                if not_first:
                    send_html_email(
                        subject="New Properties On Rightmove!",
                        recipient="   ENTER RECIPIENTS HERE SEPARATED BY COMMAS   ",
                        html_content=html_content,
                    )
                    print(f"email sent!")
                    print("")
            not_first = True

            time.sleep(1 * 60)

    except KeyboardInterrupt:
        quit()
    except Exception:
        quit()


print("Done")
