import os

from amadeus import Client, ResponseError
from dotenv import load_dotenv

load_dotenv()


class AmadeusFlightService:
    def __init__(self):
        self.api_key, self.api_secret = self.get_amadeus_credentials()

        try:
            self.amadeus = Client(client_id=self.api_key, client_secret=self.api_secret)
        except Exception as e:
            raise Exception(f"Failed to create Amadeus client: {str(e)}")

    @staticmethod
    def get_amadeus_credentials() -> tuple[str, str]:
        api_key = os.getenv("AMADEUS_API_KEY")
        api_secret = os.getenv("AMADEUS_API_SECRET")
        if not api_key or not api_secret:
            raise ValueError("Amadeus API credentials not configured")
        return api_key, api_secret

    def search_flights(self, request_body: dict) -> dict:
        try:
            response = self.amadeus.shopping.flight_offers_search.post(request_body)
            # print('Amadeus API response:', response)
            return response

        except ResponseError as api_error:
            raise Exception(f"{api_error}")

    # def confirm_price(self):
    def confirm_price(self, request_body: dict):
        # def confirm_price(self, ):
        try:
            # flights = self.amadeus.shopping.flight_offers_search.get(
            #     originLocationCode='NYC',
            #     destinationLocationCode='LON',
            #     departureDate='2025-11-19', adults=1
            # ).data
            #
            # print(flights[0]) #-> 주석에 보관 request schema로 만들어야함

            # response_one_flight = self.amadeus.shopping.flight_offers.pricing.post(flights[0])
            response = self.amadeus.shopping.flight_offers.pricing.post(request_body)
            return response.data

            # print(response_one_flight.data)
            # {'type': 'flight-offers-pricing', 'flightOffers': [
            #     {'type': 'flight-offer', 'id': '1', 'source': 'GDS', 'instantTicketingRequired': False,
            #      'nonHomogeneous': False, 'paymentCardRequired': False, 'lastTicketingDate': '2025-11-19', 'itineraries': [
            #         {'segments': [{'departure': {'iataCode': 'EWR', 'terminal': 'B', 'at': '2025-11-19T19:35:00'}, 'arrival'
        except ResponseError as error:
            raise error

        # traveler = {
        #     'id': '1',
        #     'dateOfBirth': '1982-01-16',
        #     'name': {
        #         'firstName': 'JORGE',
        #         'lastName': 'GONZALES'
        #     },
        #     'gender': 'MALE',
        #     'contact': {
        #         'emailAddress': 'jorge.gonzales833@telefonica.es',
        #         'phones': [{
        #             'deviceType': 'MOBILE',
        #             'countryCallingCode': '34',
        #             'number': '480080076'
        #         }]
        #     },
        #     'documents': [{
        #         'documentType': 'PASSPORT',
        #         'birthPlace': 'Madrid',
        #         'issuanceLocation': 'Madrid',
        #         'issuanceDate': '2015-04-14',
        #         'number': '00000000',
        #         'expiryDate': '2027-04-14',
        #         'issuanceCountry': 'ES',
        #         'validityCountry': 'ES',
        #         'nationality': 'ES',
        #         'holder': True
        #     }]
        # }

    def create_flight_order(self, request_body: dict):
        try:
            # Flight Offers Search to search for flights from MAD to ATH
            # flight_search = self.amadeus.shopping.flight_offers_search.get(
            #     originLocationCode='LON',
            #     destinationLocationCode='NYC',
            #     departureDate='2025-11-20',
            #     adults=1
            # ).data
            # #
            # print("request_body", request_body)
            # print("Flight Search Result[0] json:", json.dumps(flight_search[0]))
            # print("Traveler json:", json.dumps(traveler))

            # price_confirm = self.amadeus.shopping.flight_offers.pricing.post(
            #     flight_search[0]).data
            # request_body).data

            # print("price_confirm done.")

            flight_offer = request_body.get("flight_offer")
            travelers = request_body.get("travelers")
            # print("flight_offer", flight_offer)
            # print("travelers", travelers)

            if not flight_offer:
                raise ValueError("flight_offer is required in request body")
            if not travelers:
                raise ValueError("travelers information is required")

            booked_flight = self.amadeus.booking.flight_orders.post(
                flight_offer, travelers
            )

            return booked_flight.data
        except ResponseError as error:
            raise error

    def search_flights_get(self, request_body: dict) -> dict:
        try:
            response = self.amadeus.shopping.flight_offers_search.get(**request_body)
            print("Amadeus API response: data", response.data)
            return response.data

        except ResponseError as api_error:
            raise Exception(f"{api_error}")


amadeus_flight_service = AmadeusFlightService()

# flights[0] : confirm_price request  sample data
"""
{
  "type": "flight-offer",
  "id": "1",
  "source": "GDS",
  "instantTicketingRequired": false,
  "nonHomogeneous": false,
  "oneWay": false,
  "isUpsellOffer": false,
  "lastTicketingDate": "2025-11-19",
  "lastTicketingDateTime": "2025-11-19",
  "numberOfBookableSeats": 9,
  "itineraries": [
    {
      "duration": "PT18H55M",
      "segments": [
        {
          "departure": {
            "iataCode": "EWR",
            "terminal": "B",
            "at": "2025-11-19T19:35:00"
          },
          "arrival": {
            "iataCode": "KEF",
            "at": "2025-11-20T06:15:00"
          },
          "carrierCode": "FI",
          "number": "622",
          "aircraft": {
            "code": "7M9"
          },
          "operating": {
            "carrierCode": "FI"
          },
          "duration": "PT5H40M",
          "id": "228",
          "numberOfStops": 0,
          "blacklistedInEU": false
        },
        {
          "departure": {
            "iataCode": "KEF",
            "at": "2025-11-20T16:20:00"
          },
          "arrival": {
            "iataCode": "LHR",
            "terminal": "2",
            "at": "2025-11-20T19:30:00"
          },
          "carrierCode": "FI",
          "number": "454",
          "aircraft": {
            "code": "7M8"
          },
          "operating": {
            "carrierCode": "FI"
          },
          "duration": "PT3H10M",
          "id": "229",
          "numberOfStops": 0,
          "blacklistedInEU": false
        }
      ]
    }
  ],
  "price": {
    "currency": "EUR",
    "total": "159.84",
    "base": "5.00",
    "fees": [
      {
        "amount": "0.00",
        "type": "SUPPLIER"
      },
      {
        "amount": "0.00",
        "type": "TICKETING"
      }
    ],
    "grandTotal": "159.84"
  },
  "pricingOptions": {
    "fareType": [
      "PUBLISHED"
    ],
    "includedCheckedBagsOnly": false
  },
  "validatingAirlineCodes": [
    "FI"
  ],
  "travelerPricings": [
    {
      "travelerId": "1",
      "fareOption": "STANDARD",
      "travelerType": "ADULT",
      "price": {
        "currency": "EUR",
        "total": "159.84",
        "base": "5.00"
      },
      "fareDetailsBySegment": [
        {
          "segmentId": "228",
          "cabin": "ECONOMY",
          "fareBasis": "XJ1QUSLT",
          "brandedFare": "LIGHT",
          "brandedFareLabel": "ECONOMY LIGHT",
          "class": "X",
          "includedCheckedBags": {
            "quantity": 0
          },
          "includedCabinBags": {
            "quantity": 1
          },
          "amenities": [
            {
              "description": "CHECKED BAG UP TO 23KG",
              "isChargeable": true,
              "amenityType": "BAGGAGE",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            },
            {
              "description": "ALCOHOLIC DRINK",
              "isChargeable": true,
              "amenityType": "MEAL",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            },
            {
              "description": "NON ALCOHOLIC DRINK",
              "isChargeable": false,
              "amenityType": "MEAL",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            },
            {
              "description": "MEAL",
              "isChargeable": true,
              "amenityType": "MEAL",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            },
            {
              "description": "USB POWER",
              "isChargeable": false,
              "amenityType": "ENTERTAINMENT",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            },
            {
              "description": "BASIC SEAT",
              "isChargeable": true,
              "amenityType": "BRANDED_FARES",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            }
          ]
        },
        {
          "segmentId": "229",
          "cabin": "ECONOMY",
          "fareBasis": "XJ1QUSLT",
          "brandedFare": "LIGHT",
          "brandedFareLabel": "ECONOMY LIGHT",
          "class": "X",
          "includedCheckedBags": {
            "quantity": 0
          },
          "includedCabinBags": {
            "quantity": 1
          },
          "amenities": [
            {
              "description": "CHECKED BAG UP TO 23KG",
              "isChargeable": true,
              "amenityType": "BAGGAGE",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            },
            {
              "description": "ALCOHOLIC DRINK",
              "isChargeable": true,
              "amenityType": "MEAL",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            },
            {
              "description": "NON ALCOHOLIC DRINK",
              "isChargeable": false,
              "amenityType": "MEAL",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            },
            {
              "description": "MEAL",
              "isChargeable": true,
              "amenityType": "MEAL",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            },
            {
              "description": "USB POWER",
              "isChargeable": false,
              "amenityType": "ENTERTAINMENT",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            },
            {
              "description": "BASIC SEAT",
              "isChargeable": true,
              "amenityType": "BRANDED_FARES",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            }
          ]
        }
      ]
    }
  ]
}
"""

# traveler : create_flight_order request  sample data 1/2
"""
{
  "id": "1",
  "dateOfBirth": "1982-01-16",
  "name": {
    "firstName": "JORGE",
    "lastName": "GONZALES"
  },
  "gender": "MALE",
  "contact": {
    "emailAddress": "jorge.gonzales833@telefonica.es",
    "phones": [
      {
        "deviceType": "MOBILE",
        "countryCallingCode": "34",
        "number": "480080076"
      }
    ]
  },
  "documents": [
    {
      "documentType": "PASSPORT",
      "birthPlace": "Madrid",
      "issuanceLocation": "Madrid",
      "issuanceDate": "2015-04-14",
      "number": "00000000",
      "expiryDate": "2027-04-14",
      "issuanceCountry": "ES",
      "validityCountry": "ES",
      "nationality": "ES",
      "holder": true
    }
  ]
}
"""
# flight_search[0] : create_flight_order request  sample data 2/2
"""
{
  "type": "flight-offer",
  "id": "1",
  "source": "GDS",
  "instantTicketingRequired": false,
  "nonHomogeneous": false,
  "oneWay": false,
  "isUpsellOffer": false,
  "lastTicketingDate": "2025-11-19",
  "lastTicketingDateTime": "2025-11-19",
  "numberOfBookableSeats": 9,
  "itineraries": [
    {
      "duration": "PT18H55M",
      "segments": [
        {
          "departure": {
            "iataCode": "EWR",
            "terminal": "B",
            "at": "2025-11-19T19:35:00"
          },
          "arrival": {
            "iataCode": "KEF",
            "at": "2025-11-20T06:15:00"
          },
          "carrierCode": "FI",
          "number": "622",
          "aircraft": {
            "code": "7M9"
          },
          "operating": {
            "carrierCode": "FI"
          },
          "duration": "PT5H40M",
          "id": "228",
          "numberOfStops": 0,
          "blacklistedInEU": false
        },
        {
          "departure": {
            "iataCode": "KEF",
            "at": "2025-11-20T16:20:00"
          },
          "arrival": {
            "iataCode": "LHR",
            "terminal": "2",
            "at": "2025-11-20T19:30:00"
          },
          "carrierCode": "FI",
          "number": "454",
          "aircraft": {
            "code": "7M8"
          },
          "operating": {
            "carrierCode": "FI"
          },
          "duration": "PT3H10M",
          "id": "229",
          "numberOfStops": 0,
          "blacklistedInEU": false
        }
      ]
    }
  ],
  "price": {
    "currency": "EUR",
    "total": "159.84",
    "base": "5.00",
    "fees": [
      {
        "amount": "0.00",
        "type": "SUPPLIER"
      },
      {
        "amount": "0.00",
        "type": "TICKETING"
      }
    ],
    "grandTotal": "159.84"
  },
  "pricingOptions": {
    "fareType": [
      "PUBLISHED"
    ],
    "includedCheckedBagsOnly": false
  },
  "validatingAirlineCodes": [
    "FI"
  ],
  "travelerPricings": [
    {
      "travelerId": "1",
      "fareOption": "STANDARD",
      "travelerType": "ADULT",
      "price": {
        "currency": "EUR",
        "total": "159.84",
        "base": "5.00"
      },
      "fareDetailsBySegment": [
        {
          "segmentId": "228",
          "cabin": "ECONOMY",
          "fareBasis": "XJ1QUSLT",
          "brandedFare": "LIGHT",
          "brandedFareLabel": "ECONOMY LIGHT",
          "class": "X",
          "includedCheckedBags": {
            "quantity": 0
          },
          "includedCabinBags": {
            "quantity": 1
          },
          "amenities": [
            {
              "description": "CHECKED BAG UP TO 23KG",
              "isChargeable": true,
              "amenityType": "BAGGAGE",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            },
            {
              "description": "ALCOHOLIC DRINK",
              "isChargeable": true,
              "amenityType": "MEAL",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            },
            {
              "description": "NON ALCOHOLIC DRINK",
              "isChargeable": false,
              "amenityType": "MEAL",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            },
            {
              "description": "MEAL",
              "isChargeable": true,
              "amenityType": "MEAL",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            },
            {
              "description": "USB POWER",
              "isChargeable": false,
              "amenityType": "ENTERTAINMENT",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            },
            {
              "description": "BASIC SEAT",
              "isChargeable": true,
              "amenityType": "BRANDED_FARES",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            }
          ]
        },
        {
          "segmentId": "229",
          "cabin": "ECONOMY",
          "fareBasis": "XJ1QUSLT",
          "brandedFare": "LIGHT",
          "brandedFareLabel": "ECONOMY LIGHT",
          "class": "X",
          "includedCheckedBags": {
            "quantity": 0
          },
          "includedCabinBags": {
            "quantity": 1
          },
          "amenities": [
            {
              "description": "CHECKED BAG UP TO 23KG",
              "isChargeable": true,
              "amenityType": "BAGGAGE",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            },
            {
              "description": "ALCOHOLIC DRINK",
              "isChargeable": true,
              "amenityType": "MEAL",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            },
            {
              "description": "NON ALCOHOLIC DRINK",
              "isChargeable": false,
              "amenityType": "MEAL",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            },
            {
              "description": "MEAL",
              "isChargeable": true,
              "amenityType": "MEAL",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            },
            {
              "description": "USB POWER",
              "isChargeable": false,
              "amenityType": "ENTERTAINMENT",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            },
            {
              "description": "BASIC SEAT",
              "isChargeable": true,
              "amenityType": "BRANDED_FARES",
              "amenityProvider": {
                "name": "BrandedFare"
              }
            }
          ]
        }
      ]
    }
  ]
}
"""
