from typing import Optional

from pydantic import BaseModel, Field


class DepartureDateTimeRange(BaseModel):
    date: str
    time: str


class OriginDestination(BaseModel):
    id: str
    originLocationCode: str
    destinationLocationCode: str
    departureDateTimeRange: DepartureDateTimeRange


class Traveler(BaseModel):
    id: str
    travelerType: str
    associatedAdultId: str | None = None


class AdditionalInformation(BaseModel):
    chargeableCheckedBags: bool
    brandedFares: bool
    fareRules: bool


class PricingOptions(BaseModel):
    includedCheckedBagsOnly: bool


class CarrierRestrictions(BaseModel):
    blacklistedInEUAllowed: bool
    includedCarrierCodes: list[str]


class CabinRestriction(BaseModel):
    cabin: str
    coverage: str
    originDestinationIds: list[str]


class ConnectionRestriction(BaseModel):
    airportChangeAllowed: bool
    technicalStopsAllowed: bool


#  TODO: 필수로 포함해서 넘겼더니 에러남. -> 정상이면 Optional 처리 / 아니라면 제거


class FlightFilters(BaseModel):
    # crossBorderAllowed: Optional[bool] = None
    # moreOvernightsAllowed: Optional[bool] = None
    # returnToDepartureAirport: Optional[bool] = None
    # railSegmentAllowed: Optional[bool] = None
    # busSegmentAllowed: Optional[bool] = None
    # carrierRestrictions: Optional[CarrierRestrictions] = None
    # connectionRestriction: Optional[ConnectionRestriction] = None

    cabinRestrictions: list[CabinRestriction]


class SearchCriteria(BaseModel):
    excludeAllotments: Optional[bool] = None
    addOneWayOffers: Optional[bool] = None
    allowAlternativeFareOptions: Optional[bool] = None
    oneFlightOfferPerDay: Optional[bool] = None
    additionalInformation: Optional[AdditionalInformation] = None
    pricingOptions: Optional[PricingOptions] = None
    maxFlightOffers: int
    flightFilters: FlightFilters


class FlightSearchRequestPost(BaseModel):
    currencyCode: str
    originDestinations: list[OriginDestination]
    travelers: list[Traveler]
    sources: list[str]
    searchCriteria: SearchCriteria


class FlightSearchRequestGet(BaseModel):
    originLocationCode: str
    destinationLocationCode: str
    departureDate: str
    adults: int = Field(default=1)
    max: int = Field(default=5)
    returnDate: str | None = None
    children: int | None = None
    infants: int | None = None
    travelClass: str | None = None
    includedAirlineCodes: str | None = None
    excludedAirlineCodes: str | None = None
    nonStop: bool | None = None
    currencyCode: str = Field(default="USD")
    maxPrice: int | None = None
