# Home Applications

This project contains backend API developement for home-oriented applications for personal use. These are all developed with Python 3.7, Django 2.4 and Django REST Framework 3.9.

## Food Tracking API

The food tracking API provides a REST API endpoint that allows retrievel of food and food composition data based on USDA Nutrition Database.

Source of the data:

U.S. Department of Agriculture, Agricultural Research Service. 20xx. USDA Branded Food Products Database. Nutrient Data Laboratory Home Page, http://ndb.nal.usda.gov

The API provides the following services:

* retrieve foods (based on filtering and search options) from the database
* create new foods based on existing foods by defining recipes
* internally derive nutrient counts for all custom food created
* add entries to a daily log of consumed foods
* internally track all nutrients consumed each day
* log food purchases with their price (in different currencies)
* create nutrition profiles that sets daily nutrient targets to reach that can be tracked

An automatically generated browsable API is available that can be used to disocver all the API's functions.
