from pydantic import BaseModel, Field


class FlightOrderRequest(BaseModel):
    flight_offer: dict = Field(
        ...,
        description="Pre-selected and price-confirmed flight offer from the search/pricing endpoints",
    )
    travelers: list[dict] = Field(
        ...,
        description="List of traveler details including personal information and documents",
    )
