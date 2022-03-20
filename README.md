# Final Project Template

The final project for this course has several steps that you must complete. 
To give you an overview of the whole project, all the high-level steps are listed below. 
The project is then divided into several smaller labs that give the detailed instructions for each step. 
You must complete all the labs to successfully complete the project.

## Project Breakdown



**Add user management to the application**
1. Implement user management using the Django user authentication system.
2. Set up continuous integration and delivery

**Implement backend services**
1. Create cloud functions to manage dealers and reviews
2. Create Django models and views to manage car model and car make
3. Create Django proxy services and views to integrate dealers, reviews, and cars together
 
**Add dynamic pages with Django templates**
1. Create a page that shows all the dealers
2. Create a page that show reviews for a selected dealer
3. Create a page that let's the end user add a review for a selected dealer

**Containerize your application**
1. Add deployment artifacts to your application
2. Deploy your application


# Setup 
This project was created in a local development environment rather than in the web-container "Theia" environment provided by IBM.<br>
As such, there are some differences to work around. 
* ###Using Couchimport

Couchimport is a node.js tool that imports data into Cloudant. In this case, we have pre-defined test data that we want to load into our Cloudant instance. We install Couchimport by running `npm install -g couchimport`. 

Set the following environment variables using the service credentials of your Cloudant instance.

`export IAM_API_KEY="REPLACED IT WITH GENERATED <apikey>"`

`export COUCH_URL="REPLACED IT WITH GENERATED <url>"`

From the project root, run `cat cloudant/data/dealerships.json | node node_modules/couchimport/bin/couchimport.bin.js --type "json" --jsonpath "<THE-TABLE-WE-WANT-TO-IMPORT>.*" --database dealerships --url <REPLACE-ME-WITH-CLOUDANT-URL>`.

* ###Setting Up PostgreSQL

Instead of using the instance provided by IBM using their Theia environment, I chose to set up a local instance using Docker Compose. 

In a terminal from the project root, navigate to `storage-docker-configuration` and run `docker-compose up`. On the first run, this will download and install Postgresql into the container and run it. The database will be exposed on the default port `5432` so that we can connect to it. 



