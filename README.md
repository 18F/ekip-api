Every Kid in a Park (EKIP API)
=======

[![Coverage Status](https://coveralls.io/repos/18F/ekip-api/badge.svg?branch=master&service=github)](https://coveralls.io/github/18F/ekip-api?branch=master)


#Introduction
The [Every Kid in a Park] (https://www.whitehouse.gov/the-press-office/2015/02/19/fact-sheet-launching-every-kid-park-initiative-and-designating-new-natio) initiative is part of President Obama’s commitment to protect our Nation’s unique outdoor spaces and ensure that every American has the opportunity to visit and enjoy them.  This initiative provides all fourth grade students and their families with free admission to National Parks and other federal lands and waters for a full year.

#About this site
This is the repository for the Every Kid in a Park website.  The site itself consists of four primary "sections": the **Landing / Home Page, How it Works, Get Your Pass**, and **Plan a Trip**.  Secondary pages include the **About** page, **Parents** page, **Pass Exchange** and **Field Trip** pages. 

###The wiki
Looking for something that you can't find here?  A [site map](https://github.com/18F/ekip/wiki/Site-Map) and other information can be found on the [Every Kid in a Park wiki](https://github.com/18F/ekip/wiki).

##Site structure

###Landing / home
The landing / home section describes the program, how it works, and provides links to resources for fourth grade students, educators and parents.  
Reading grade level: 4.5.

###How it works
This section provides a step-by-step walkthrough of the process for getting and using the pass.  
Reading grade level: 3.7.

###Get your pass
This section walks either the student or the educator through the appropriate process to get a pass.  Fourth grade students are directed to an activity - once the activity is completed they can print the paper pass.  The paper pass can later be redeemed for a plastic pass at participating sites.  
Reading grade level: 2.6.

###Plan your trip
This section includes trip planning resources for students and parents.  For educators, there is also an opportunity to plan field trips from a select subset of sites.  
Reading grade level: 1.3.

###Parents page
The parents page provides information for parents on the rules of the program and trip planning resources.  
Reading grade level: 4.6.

###About page
The about page includes some useful information on partner agencies named in the initiative, press resources, code repository and contact information.  
Reading grade level: 4.6.

###Pass exchange and field trip pages
These pages provide simple lists of sites that will exchange the paper pass for a plastic pass (the pass exchange page) and a subset of field trip suggestions.  The pass exchange locations are derived from the broader [America the Beautiful](http://store.usgs.gov/pass/PassIssuanceList.pdf) pass exchange list maintained on the USGS website.  This list is updated quarterly.  
Reading grade level: 4.6.

#### Field trip data
The field trip suggestions were compiled by the Federal Interagency Council on Outdoor Recreation (FICOR) members.  This is not an exhaustive list of field trip possibilities for EKIP pass holders.  This list is maintained by the EKIP team and FICOR members.  The dataset is maintained as a .csv file, and can be found [here](https://github.com/18F/ekip-api/blob/master/ekip/nationalparks/data/ficor.csv).  It is essential that when editing this document one follows the established conventions, and does not deviate from column types or add / remove columns from the dataset.

For a complete data dictionary, [see the wiki](https://github.com/18F/ekip/wiki/FICOR-Data-Dictionary).

#### Plastic pass data
The plastic pass exchange locations allow a fourth grader to exchange their paper voucher for a durable plastic pass.  These sites are documented in the latest [America the Beautiful](http://store.usgs.gov/pass/PassIssuanceList.pdf) pass exchange list maintained on the USGS website.  Updated quarterly, this list provides a column lookup for sites that will exchange the paper passes for plastic passes.  As of September 2015 the sites that offer the exchange are the same as those that also provide the annual and military passes.  

The data for the plastic pass lookups on the website are in .csv format [here](https://github.com/18F/ekip-api/blob/master/ekip/nationalparks/data/pass-list.csv).  As with the FICOR field trip data, special caution should be taken to ensure that the data remain consistent with the existing schema when adding / removing / editing information.  Columns should not be added or removed from the .csv file.  A simple data dictionary can be found on the [wiki](https://github.com/18F/ekip/wiki/Plastic-Pass-Issuance-List).

One peculiarity to note is that the list maintained by the National Park Service does include some duplicates.  For example, Great Falls Park is listed both under Virginia and DC Metro.  In order to simplify the process of reading in the data directly from the list maintained by the National Park Service, these duplicate entries were maintained - but they also mean that a park may appear more than once in some website queries.

**Format update - May 2016** - In May 2016 the National Park Service updated the way the pass redemption site data is provided.  The format changed in the following ways:

1. NPS has added a number of new USACE= Army Corp of Engineers sites to the list.  This category was not included in the original lauch.  Names, unlike some others in the dataset, are not appended to the name of the site with an identifier, like USACE.  

2. The Annual / Senior columns that used to be broken out into separate columns (see https://store.usgs.gov/pass/PassIssuanceList.pdf), are now condensed under the new format provided by NPS into one column.  So, instead of three columns defining the type of pass(es) accepted at redemption locations, the dataset only includes two.
​
3.  State headers have been removed.  The original document used to include individual state headers - which in the dataset appeared as something like ALABAMA,,,,,,,, 

#Technical stuff
This is a [Django](https://www.djangoproject.com/)-based system and website.  

This site makes use of a number of packages you can download for free if you don't already have them, or haven't worked with them before: [Django](https://www.djangoproject.com/), [Vagrant](https://www.vagrantup.com/) [Gulp](http://gulpjs.com/), [Bourbon](http://bourbon.io/), [Neat](http://neat.bourbon.io/), [sass](https://github.com/medialize/sass.js/) and [NPM](https://www.npmjs.com/).  See the getting started section below for more information and installation guides.

This site also uses [New Relic](http://newrelic.com/) to monitor performance, Google Analytics for site statistics, and AWS for site hosting.

##Submitting issues
Interested in working on the site with us?  Great!  We maintain a separate repository for our issue tracking, found [here](https://github.com/18F/ekip/issues).  You can fork our code and suggest additions / enhancements when you have something prepared that you think improves the site.

## Ticketing system
The ticketing system generates a unique code for each paper pass the system creates.  A corresponding bar code is created during the generation of each paper pass.  Special care is taken to ensure that the codes do not generate offensive character combinations.

## Getting started
Make sure you have `vagrant` installed. For instance, on OS X with Homebrew:

```
$ brew install caskroom/cask/brew-cask
$ brew cask install vagrant
```

Then, ensure you have the appropriate Vagrant Box installed:

```
$ vagrant box add ubuntu/trusty32
```

You can get started with development by running the `Vagrantfile`:

```
$ vagrant up
```

This will provision an entire setup for you pretty quickly (see `provision/dev/bootstrap.sh`). You can access Django and start `runserver` by doing the following:

```
$ vagrant ssh
$ python manage.py runserver
```

From your host computer, going to http://192.168.19.16 will enable you to access the API.


## Front-end Setup
This project uses Gulp to manage CSS pre and post-processing. Make sure Gulp is
installed system wide:

```
npm install --global gulp
```

Next, install the additional modules to watch for SASS pre-processing changes
(using Bourbon and Neat and minifying the results) as well as uglification of JavaScript files:

```
npm install gulp-watch gulp-sass node-neat node-bourbon gulp-minify-css gulp-rename gulp-uglifyjs
```

Then once everything is installed in your project directory, simply invoke the
Gulp command in your terminal:

```
gulp
```

## Testing

To run tests locally:
```
python manage.py test --settings=config.settings.test
```

## Loading data

To load the list of pass-exchange sites, you'll need to run the following
Django management command:

```
python manage.py passes nationalparks/data/pass-list.csv
```

where pass-list.csv is the dataset for the pass exchange sites. The data file
is included in the repository.

To load the list of field trip sites, you'll need to run the following Django
management command:

```
    python manage.py field_trip nationalparks/data/ficor.csv
```

where ficor.csv is the dataset for the field trip sites. The data file is
included in the repository.


## Deploy notes

We use a blue-green deployment system for zero downtime.


### Setting up the applications.
=======
You'll need to set the application to use the production settings file.

```
cf set-env blue DJANGO_SETTINGS_MODULE config.settings.production
cf set-env green DJANGO_SETTINGS_MODULE config.settings.production
```


You'll need to set three environment variables, for both blue and green apps to
use S3 for hosting static files. Do this once.

```
cf set-env blue EKIP_STATIC_BUCKET_NAME <<S3 static files bucket name>>
cf set-env blue EKIP_AWS_ACCESS_KEY_ID <<value>>
cf set-env blue EKIP_AWS_SECRET_ACCESS_KEY <<value>>
cf set-env green EKIP_STATIC_BUCKET_NAME <<S3 static files bucket name>>
cf set-env green EKIP_AWS_ACCESS_KEY_ID <<value>>
cf set-env green EKIP_AWS_SECRET_ACCESS_KEY <<value>>
```


### Running deploys

To actually deploy the application, simply configure for your use case and run:

```
./deployer.sh
```

### Running database migrations

Use cf-ssh to create an instance of the application you can ssh into, and then
run:

```
python manage.py migrate --settings=config.settings.production
```
