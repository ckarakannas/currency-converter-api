# Currency Converter Sample
This is a simple Flask API with endpoints for exchanging currencies with fake exchange rates.

The purpose of this project is to demonstrate how to go about running, testing and using a Flask app from within three distinct environments in ascending order of complexity & flexibility:

- Local machine or server
- Docker Engine
- Kubernetes cluster

Instructions on how to run this app on a local Docker engine and local K8S cluster with Kind are provided.

The app supports the following currencies:
- EUR
- GBP
- USD

Endpoints:

- /exchange - POST
- /exchangeMany - POST
- /exchange/{base-currency} -POST
- /currency - GET
- /currencies  - GET

For examples and details on how to use each endpoint above, please refer to the [Postman](#postman-tests) section below.

DISCLAIMER: Provided conversion rates by this sample API are **NOT** real, they merely exist for demonstration purposes.

## Pre-requisites
## Postman Tests
## Docker

Running with Docker on local dev env is as simple as

``docker build -t cex-api:dev .``

followed by

``docker run -it --name cex-api-dev -p 5000:5000 cex-api:dev python api.py``

Or simply do this in one go by grabbing the image from Docker Hub:

``docker run -it --name cex-api-dev -p 5000:5000 chrisk14/currency-exchange:dev python api.py``

For a production image with an inbuilt Gunicorn server run

``docker build -t cex-api:prod . --build-arg API_ENV=Production``

NOTE: The --build-arg 'API_ENV' is case sensitive and API_ENV=Production instructs Docker and Python to use production dependencies, including Gunicorn. By default, the API_ENV is set to 'Deployment'.

Subsequently, to get a running, production-like container, run

``docker run -it -p 5000:5000 --name cex-api-prod cex-api:prod gunicorn -w 4 -b 0.0.0.0:5000 run:app``

Again, you can do this in one go by grabbing the image from Docker Hub:

``docker run -it -p 5000:5000 --name cex-api-prod chrisk14/currency-exchange:prod gunicorn -w 4 -b 0.0.0.0:5000 run:app``

## Docker-Compose

You can also build from source code and run with a single command using docker-compose:

``docker-compose up -d --build``

The above defaults to a local dev container. For a production-like container running Gunicorn WSGI, use this command:

``docker-compose -f docker-compose.yml -f production.yml up -d --build``

## K8S

A basic setup of K8S locally with dashboard access is given below.

- Install kubectl [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
- Create a single node cluster with preconfigured port mappings and mounts (for dev env):

  `kind create cluster --config=kubernetes/cluster-config.yaml --name local`

This creates a K8S cluster named local. Verify this by running:

`kind get clusters`

Apply resources for an interactive dashboard

  ```
  kubectl apply -f kubernetes/dashboard-resources.yaml

  kubectl apply -f kubernetes/dashboard-admin-resources.yaml
  ```

- Start a kubectl proxy

  ``kubectl proxy --port=51658``

- Open another terminal and grab secret token for dashboard login

  ```
  kubectl -n kubernetes-dashboard describe secret $(kubectl -n kubernetes-dashboard get secret | grep admin-user | awk '{print $1}')
  ```
- Access the dashboard through this [link](http://localhost:51658/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/). Copy the token generated in the previous step, and paste it to login.

### Deploy

To deploy the sample Flask app on your local K8S cluster run the following on your terminal

``` 
kubectl apply -f kubernetes/dev/flask-deployment.yaml
kubectl apply -f kubernetes/dev/flask-service.yaml
```

These will provision a deployment with 2 replicas serving on localhost:30000. To scale up or down run

```
kubectl scale deployment flask-deployment --replicas=<INT>
```

Similarly for the production equivalent Flask app, run

``` 
kubectl apply -f kubernetes/prod/flask-deployment.yaml
kubectl apply -f kubernetes/prod/flask-service.yaml
```

### Access on your webrowser

To access these instances on your web browser, simply go to localhost:30000 for dev Pod instances and localhost:32000 for prod Pod instances.


## Deleting cluster

To delete the local K8S cluster just run

```
kind delete cluster --name local
```
