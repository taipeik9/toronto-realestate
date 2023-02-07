# toronto-realestate
Analysis and future analytics on the Toronto Real Estate Market using python, Linear Regression analysis and webscrapers

## Analysis

All of the data analysis and model creation are in the toronto-realestate.ipynb

Attempted Data Sources:

1. Remax - Unused
2. Realtor.ca - Unused
3. Zillow - Unused
4. Zoocasa
5. Trreb

## Zoocasa.com

This scraper was quite difficult to develop, the method I used is one that I find to be effective when scraping sites with JS pagination. I request directly to the API for the JSON data which includes the listings per page, and then request directly to each listing link for further features which are not displayed on the listings search page. All the scrapers follow this similar pattern.

Scraping Stats:
- No Download Delay
- ~7 min to scrape
- 3856 items
- 1 KeyError
- 139 POST Reqs
- 3857 GET Reqs

Scraping Stats v2 (Available):
- No Download Delay
- ~10.5 min to scrape (On Brainstation Wifi)
- 4003 items
- 1 500 Internal Server Error
- 145 POST Reqs
- 4006 GET Reqs

Scraping Stats v2 (Sold):
- No Download Delay
- ~71 min to scrape
- 24195 items
- 16 Timeout Server Errors
- 9 500 Internal Server Error
- 869 POST Reqs
- 24220 GET Reqs

## Realtor.ca

This site had a lot of protections from bots and scrapers. The actual site couldn't be sent any requests without JS enabled with being intercepted by Incapsula. So a lot of workarounds had to be used so that the scraper was only using Realtor.ca's API. This actually made the scraper a lot faster, due to working solely with JSON reqs.

Scraping Stats:
- No Download Delay
- ~2 min to scrape
- 4046 items
- 22 POST Reqs
- 4046 GET Reqs

## Trreb.ca

This site was by far the easiest to scrape. It was scraped purely using the API, which was fairly unprotected. Although it has the least amount of detail and lowest listing count

Scraping Stats:
- No Download Delay
- 47 sec to scrape
- 1495 items
- 1497 GET Reqs