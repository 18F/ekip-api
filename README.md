Every Kid in a Park (EKIP API)
=======

[![Coverage Status](https://coveralls.io/repos/18F/ekip-api/badge.svg?branch=master&service=github)](https://coveralls.io/github/18F/ekip-api?branch=master)

[![Code Issues](https://www.quantifiedcode.com/api/v1/project/ecb305ac0bfa4e968192621402faface/badge.svg)](https://www.quantifiedcode.com/app/project/ecb305ac0bfa4e968192621402faface)


#Introduction
The [Every Kid in a Park] (https://www.whitehouse.gov/the-press-office/2015/02/19/fact-sheet-launching-every-kid-park-initiative-and-designating-new-natio) initiative is part of President Obama’s commitment to protect our Nation’s unique outdoor spaces and ensure that every American has the opportunity to visit and enjoy them.  This initiative provides all fourth grade students and their families with free admission to National Parks and other federal lands and waters for a full year. 

#About this Site
This is the repository for the Every Kid in a Park website.  The site itself consists of four primary "sections": the **Landing / Home Page, How it Works, Get Your Pass**, and **Plan a Trip**.  A site map can be found [here](https://github.com/18F/ekip/wiki/Site-Map).

#Technical Stuff
The EKIP application used to consist of two parts: a Django based API, and a Jekyll application.  

##Submitting Issues
Interested in working on the site with us?  Great!  We maintain a separate repository for our issue tracking, found [here](https://github.com/18F/ekip/issues).  You can fork our code and suggest additions / enhancements when you have something prepared that you think improves the site.

## ticketing-system
A ticketing system.

## Getting Started

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

Also install the additional modules to watch for SASS pre-processing changes
(using Bourbon and Neat) and to minify the resulting stylesheet:

```
npm install gulp-watch gulp-sass node-neat node-bourbon gulp-minify-css gulp-rename
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

## Loading Data

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


## Deploy Notes

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
