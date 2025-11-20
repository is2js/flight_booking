from typing import Any

from pydantic import BaseModel


# RESPONSE MODELS
class FlightOffer(BaseModel):
    type: str
    id: str
    source: str
    instantTicketingRequired: bool
    nonHomogeneous: bool
    oneWay: bool
    isUpsellOffer: bool
    lastTicketingDate: str
    lastTicketingDateTime: str
    numberOfBookableSeats: int
    itineraries: list[dict[str, Any]]
    price: dict[str, Any]
    pricingOptions: dict[str, Any]
    validatingAirlineCodes: list[str]
    travelerPricings: list[dict[str, Any]]

    # Optional fields that may not always be present
    totalPrice: str | None = None
    totalPriceBase: str | None = None
    fareType: str | None = None


class FlightSearchResponse(BaseModel):
    data: list[FlightOffer]
    dictionaries: dict[str, Any] | None = None
    meta: dict[str, Any] | None = None


class FlightPricingResponse(BaseModel):
    data: dict[str, Any] | None = None
    result: dict[str, Any] | None = None
    meta: dict[str, Any] | None = None
