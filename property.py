# generated thanks to chatgpt - ask it to create dataclasses for property.json

from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Location:
    latitude: float
    longitude: float


@dataclass
class PropertyImage:
    srcUrl: str
    url: str
    caption: Optional[str]


@dataclass
class PropertyImages:
    images: List[PropertyImage]
    mainImageSrc: str
    mainMapImageSrc: str


@dataclass
class ListingUpdate:
    listingUpdateReason: str
    listingUpdateDate: str


@dataclass
class DisplayPrice:
    displayPrice: str
    displayPriceQualifier: str


@dataclass
class Price:
    amount: int
    frequency: str
    currencyCode: str
    displayPrices: List[DisplayPrice]


@dataclass
class Customer:
    branchId: int
    brandPlusLogoURI: str
    contactTelephone: str
    branchDisplayName: str
    branchName: str
    brandTradingName: str
    branchLandingPageUrl: str
    development: bool
    showReducedProperties: bool
    commercial: bool
    showOnMap: bool
    enhancedListing: bool
    developmentContent: Optional[str]
    buildToRent: bool
    buildToRentBenefits: List[str]
    brandPlusLogoUrl: str


@dataclass
class ProductLabel:
    productLabelText: str
    spotlightLabel: bool


@dataclass
class Property:
    id: int
    bedrooms: int
    bathrooms: int
    numberOfImages: int
    numberOfFloorplans: int
    numberOfVirtualTours: int
    summary: str
    displayAddress: str
    countryCode: str
    location: Location
    propertyImages: PropertyImages
    propertySubType: str
    listingUpdate: ListingUpdate
    premiumListing: bool
    featuredProperty: bool
    price: Price
    customer: Customer
    distance: Optional[float]
    transactionType: str
    productLabel: ProductLabel
    commercial: bool
    development: bool
    residential: bool
    students: bool
    auction: bool
    feesApply: bool
    feesApplyText: str
    displaySize: str
    showOnMap: bool
    propertyUrl: str
    contactUrl: str
    staticMapUrl: Optional[str]
    channel: str
    firstVisibleDate: str
    keywords: List[str]
    keywordMatchType: str
    saved: bool
    hidden: bool
    onlineViewingsAvailable: bool
    lozengeModel: Dict[str, List[str]]
    hasBrandPlus: bool
    displayStatus: str
    enquiredTimestamp: Optional[str]
    heading: str
    propertyTypeFullDescription: str
    addedOrReduced: str
    formattedBranchName: str
    isRecent: bool
    formattedDistance: str
    enhancedListing: bool
