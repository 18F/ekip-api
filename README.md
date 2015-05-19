EKIP API
=======
# ticketing-system
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