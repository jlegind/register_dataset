# register_dataset
This Python project enables you to scrape a webpage with Darwin Core archives and index these datasets into the [GBIF (GLOBAL BIODIVERSITY INFORMATION FACILITY) data portal](http://www.gbif.org/).

The code is written in Python 3 and can be modified to fit any service that is based on a RESTful API platform.

Prerequisites needed for the user:
* An account on the GBIF portal website http://www.gbif.org/
* Editor rights for this account (Please contact the GBIF Secretariat helpdesk@gbif.org)
* Affiliation with an existing publishing organization in the GBIF network

Prerequisites needed to run the package:
* Beatiful Soup 4 - bs4 is a library for parsing HTML and XML files. https://pypi.python.org/pypi/beautifulsoup4
* [Requests](http://docs.python-requests.org/en/master/), a library that deals with HTML requests and handles url encoding  

### Workflow

For the purpose of publishing to GBIF you will need an API url, the url for the web page containg the zip files, the GBIF publisher UUID, the GBIF publisher *installation* UUID, and username/password. 
