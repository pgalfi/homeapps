# Home Applications

This project contains backend API development for home-oriented applications for personal use. These are all developed with Python 3.7, Django 2.4 and Django REST Framework 3.9.

## Food Tracking API

The food tracking API provides a REST API endpoint that allows retrieval of food and food composition data based on USDA Nutrition Database.

Source of the data:

U.S. Department of Agriculture, Agricultural Research Service. 2019. USDA Branded Food Products Database. Nutrient Data Laboratory Home Page, http://ndb.nal.usda.gov

The API provides the following services:

* retrieve foods and their detailed nutrition composition (based on filtering and search options) from the USDA dataset
* create new foods based on existing foods by defining recipes
* internally derive nutrient counts for all custom food created
* add entries to a daily log of consumed foods
* internally track all nutrients consumed each day
* log food purchases with their price (in different currencies)
* create nutrition profiles that can be used to set daily nutrient targets 

An automatically generated browsable API is available that can be used to discover all the API's functions.

## Housing API and demo front end

The Housing API provides a REST API endpoint allowing retrieval of advertised housing properties. It provides the following filtering:

* location (based on postal code ranges)
* advertised price
* property size
* number of rooms
* key words in the description

The API keeps track of user based "views" and "likes". A view is counted when a user clicks on a detailed profile information of a property (linked to external advertiser). A user based "like" list is maintained that can be controlled through "Like" and "Not Like" buttons. The API provides two simple actions for adding or removing properties from this list.

The API's listing call can then also filter against the viewed or liked list as needed.

