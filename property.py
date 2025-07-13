from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Location:
    latitude: float
    longitude: float


@dataclass
class Image:
    url: str
    caption: Optional[str]
    srcUrl: str


@dataclass
class PropertyImages:
    images: List[Image]
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
    productLabelText: Optional[str]
    spotlightLabel: bool


@dataclass
class LozengeModel:
    matchingLozenges: List[str]


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
    price: Price
    premiumListing: bool
    featuredProperty: bool
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
    lozengeModel: LozengeModel
    hasBrandPlus: bool
    displayStatus: str
    enquiredTimestamp: Optional[str]
    enquiryAddedTimestamp: Optional[str]
    enquiryCalledTimestamp: Optional[str]
    heading: str
    isRecent: bool
    enhancedListing: bool
    addedOrReduced: str
    formattedBranchName: str
    formattedDistance: str
    propertyTypeFullDescription: str
