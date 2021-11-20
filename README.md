#Avengers API

## Required Environment Variables (.env file)
1. DATABASE_PASSWORD 
   * The database password used on initialization of a new database, and/or to access an existing database
2. DATABASE_USER
   * The default username for initializing a new database and/or the username to use when connecting to an existing 
   database
3. DATABASE_NAME
   * The default database name when initializing a new database and/or the name of the database which to connect to
4. ENV
   * The running environment for the application, e.g. 'development' or 'production'

## Setup Steps
1. Create .env file and set environment variables
2. Run docker-compose using provided docker-compose file