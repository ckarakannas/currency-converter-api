# Currency Converter Flask

## Docker

Running with Docker on local dev env is as simple as

``docker build -t cex-api:dev .``

followed by

``docker run -it --name cex-api-dev -p 5000:5000 cex-api:dev python api.py``

For a production image with an inbuilt Gunicorn server run

``docker build -t cex-api:prod . --build-arg API_ENV=Production``

NOTE: The --build-arg 'API_ENV' is case sensitive and API_ENV=Production instructs Docker and Python to use production dependencies, including Gunicorn. By default, the API_ENV is set to 'Deployment'.

Subsequently, to get a running, production-like container, run

``docker run -it -p 5000:5000 --name cex-api-prod cex-api:prod gunicorn -w 4 -b 0.0.0.0:5000 run:app``

## Docker-Compose

You can also build and run with a single command using docker-compose:

``docker-compose up -d``

The above default to a local dev container. For Production with Gunicorn WSGI, use this command:

``docker-compose -f docker-compose.yml -f production.yml up -d``
