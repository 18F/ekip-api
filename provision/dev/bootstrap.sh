#!/usr/bin/env bash

sudo apt-add-repository ppa:nginx/stable -y
sudo apt-get update -y
sudo apt-get install -y nginx
sudo apt-get install python-pip -y
sudo apt-get install git -y

sudo cp /vagrant/provision/dev/nginx_site.conf /etc/nginx/sites-enabled/default
sudo service nginx restart

sudo apt-get install libevent-dev -y
sudo apt-get install libpq-dev -y
sudo apt-get install python-virtualenv -y
sudo apt-get install python-dev -y
sudo apt-get install libbz2-dev -y
sudo apt-get install libsqlite3-dev -y
sudo apt-get install libreadline-dev -y

if [ ! -f /home/vagrant/provision/postgres ]; then

  echo 'deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main' | sudo tee /etc/apt/sources.list.d/pgdg.list

  wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | sudo apt-key add -

  sudo apt-get update
  sudo apt-get install -y \
    postgresql \
    libpq-dev

  sudo -u postgres psql -c "create user ekip with password 'ekip';"
  sudo -u postgres psql -c "alter user ekip with superuser;"
  sudo -u postgres psql -c "CREATE DATABASE ekip;"
  sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ekip TO ekip;"

  su -c "touch /home/vagrant/provision/dev/postgres" vagrant

fi


sudo su vagrant <<'EOF'
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
. ~/.bash_profile
pyenv install 3.4.3
pyenv rehash
pyenv virtualenv 3.4.3 ekip
pyenv rehash
pyenv activate ekip
pip install -r /vagrant/requirements.txt
pip install -r /vagrant/requirements-dev.txt
cd /vagrant/ekip
python manage.py migrate --no-input
echo 'cd /vagrant/ekip' >> ~/.bash_profile
echo 'pyenv activate ekip' >> ~/.bash_profile
EOF