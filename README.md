# ticketing-system
A ticketing system. 


# Setting up the database. 

```
sudo su - postgres

postgres@precise64:~$ psql
psql (9.1.14)
Type "help" for help.

postgres=# create database ekip with encoding 'UTF8' LC_COLLATE='en_US.UTF8' LC_CTYPE='en_US.UTF8' TEMPLATE=template0;
postgres=# psql -d ekip -c "CREATE USER ekip WITH password '<<PASSWORD>>';"
```
