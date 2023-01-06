
# Find Your Garage

Web application written in django to manage car workshops and find them
on the map. The application provides simple decoding of the vin number
when creating the vehicle and uses the google maps API to determine the
longitude and latitude of the workshop

This project was made for the purposes of studies. This is my engineering thesis.

Online Version available at:

https://www.znajdzwarsztacik.pl


## Tech Stack

The application is hosted on the Heroku platform. 

**Client:** 

- CSS(SCSS) + Bootstrap 
- JavaScript
- Apexcharts.js

**Server:** 

- Python (Django 4.0.6)
- PostgreSQL
- Azure BLOB storage





## Features

- Completely working login/signup system using allauth django libary
- Adding own garage and determine longitude and latitude of its position using google maps API
- Adding own car using VIN decoder to find information about selected car
- Usage of SMTP protocol to send emails, for example to activate user account
- Usage of Apexcharts.js libary to show information about car/garage


## To Do

- Create notification system after sucessfully actions
- Dockerize application
- Create tests for functions