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
