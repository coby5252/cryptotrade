# cryptotrade

# Description

This is a simple API to make automated trades on [Gemini](https://gemini.com/).

## Settings

api/GeminiRequest.py contains all of the methods needed to make requeests.  For requests to be made, settings.config must be set up with an API key, and a private key to sign requests.

## Algorithms

algortithms/ contains 2 trivial trading algorithms.  To begin trading, simply run the appropriate python script for the algorithm you want to use.

## Database

database/Database.py provides a method for logging price.  This method is invoked by capture_price.py to keep historical records of the price of ether.
