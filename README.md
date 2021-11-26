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
5. GIT_COMMIT
   * The git ref to use when pulling the code to deploy. e.g. 'main', 'develop'
6. VUE_APP_BASE_URL
   * The configured API URL

## Setup Steps
1. Create .env file and set environment variables
2. Run docker-compose using provided docker-compose file
3. Run alembic migrations on database - 'pipenv run alembic upgrade head'
4. Restart API service in docker-compose