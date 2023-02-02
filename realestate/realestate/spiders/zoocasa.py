import scrapy

import json


class ZoocasaSpider(scrapy.Spider):
    name = 'zoocasa'
    allowed_domains = ['www.zoocasa.com']
    headers={
        'content-type' : 'application/json',
        'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'x-zoocasa-generation' : 'next',
        'x-zoocasa-request-source' : 'zoocasa.com',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.zoocasa.com/toronto-on-real-estate',
        'origin': 'https://www.zoocasa.com',
        'connection': 'keep-alive',
        'cache-control': 'no-cache'
    }
    payload = {
                "filter": {
                    "rental": False,
                    "status": "available",
                    "slug": "toronto-on",
                    "latitude": 43.653226,
                    "longitude": -79.3831843,
                    "zoom": 14,
                    "home-type": {
                        "house-detached": True,
                        "house-semidetached": True,
                        "house-attached": True,
                        "townhouse": True,
                        "condo": True
                    },
                    "price-min": None,
                    "price-max": None,
                    "listed-since": None,
                    "listed-to": None,
                    "bedrooms": "0+",
                    "sqft-min": None,
                    "sqft-max": None,
                    "bathrooms": "1+",
                    "parking-spaces": "0+",
                    "open-house": False,
                    "garage": False,
                    "pool": False,
                    "fireplace": False,
                    "waterfront": False,
                    "additional": {
                        "house": {
                            "single-family": False,
                            "basement-apartment": False,
                            "duplex": False,
                            "triplex": False,
                            "fourplex+": False
                        },
                        "condo-or-townhouse": {
                            "locker": "any",
                            "maintenance-fee": None
                        }
                    },
                    "area-name": "Toronto",
                    "boundary": None
                },
                "page": {
                    "number": 1,
                    "size": 28
                },
                "sort": "-date"
            }

    def start_requests(self):
        yield scrapy.Request(url="https://www.zoocasa.com/services/api/v3/listings",
            method='POST',
            body=json.dumps(self.payload),
            headers=self.headers
        )


    def parse(self, response):
        response_json = json.loads(response.body)
        listings = response_json['data']
        response_meta = response_json['meta']

        if listings:
            for listing in listings:
                listing_att = listing['attributes']
                square_footage = listing_att['square-footage'] if listing_att['square-footage'] else {}
                listing_meta =  {
                    'id' : listing['id'],
                    'address' : f"{listing_att['street-number']} {listing_att['street-name']}",
                    'postal_code' : listing_att['postal-code'],
                    'price' : listing_att['price'],
                    'bedrooms' : listing_att['bedrooms'],
                    'bedrooms_partial' : listing_att['bedrooms-partial'],
                    'bathrooms' : listing_att['bathrooms'],
                    'bathrooms_partial' : listing_att['bathrooms-partial'],
                    'square_footage_min' : square_footage.get('min'),
                    'square_footage_max' : square_footage.get('max'),
                    'unit' : listing_att['unit-number'],
                    'parking' : listing_att['parking'],
                    'city' : listing_att['city'],
                    'province' : listing_att['province'],
                    'added_at' : listing_att['added-at'],
                    'lat' : listing_att['position']['coordinates'][1],
                    'lon' : listing_att['position']['coordinates'][0],
                }

                yield response.follow(
                    url=listing_att['address-path'],
                    headers=self.headers,
                    meta={'listing_meta' : listing_meta},
                    callback=self.parse_listing
                )


            next_page = response_meta['page-number'] + 1
            next_payload = self.payload
            next_payload['page']['number'] = next_page

            yield scrapy.Request(url="https://www.zoocasa.com/services/api/v3/listings",
                method='POST',
                body=json.dumps(next_payload),
                headers=self.headers,
                dont_filter=True
            )

    def parse_listing(self, response):
        res_json = json.loads(
            response.xpath('//*[@id="__NEXT_DATA__"]/text()').get()
        )['props']['pageProps']['props']['listingData']

        listing = response.request.meta['listing_meta']

        listing['type'] = res_json['type']
        listing['garage_type'] = res_json['garage']
        listing['brokerage'] = res_json['brokerage']
        listing['neighbourhood'] = res_json['neighbourhoodName']
        listing['neighbourhood_id'] = res_json['neighbourhood']['id']
        listing['exterior'] = res_json['exterior']
        listing['driveway_type'] = res_json['driveway']
        listing['basement_type'] = res_json['basement']
        listing['features'] = res_json['extras']
        listing['levels'] = res_json['levels']
        listing['rooms_total'] = len(res_json['rooms'])
        listing['desc'] = res_json['description']
        listing['mls_num'] = res_json['mlsNum']

        yield listing