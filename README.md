# About
This is a sample Flask application providing endpoints for exchanging currencies with fake exchange rates, querying rates for a specific base currency etc.

The purpose of this sample project is twofold:

- Showcase Flask and Flask-RESTful as minimal Python frameworks for developing RESTful APIs
- Demonstrate how to containerize, run & test Flask applications with Docker and Kubernetes, all done locally

The following sections go through the process of running and testing the API from within three distinct environments in ascending order of complexity & flexibility:

- [Local environment](#quick-run)
- [Docker Host](#docker)
- [Kubernetes cluster](#kubernetes)

## API features

### Endpoints
The application provides the following endpoints:

- /exchange - POST
- /exchangeMany - POST
- /exchange/{base-currency} - POST
- /currency - GET
- /currencies  - GET

All valid requests and responses are in JSON format.

The app currently supports the following base/target currencies:
- EUR
- GBP
- USD

**DISCLAIMER**: Conversion rates provided and used by this sample API are **NOT** real; they are defined for demonstration purposes.

For examples and details on how to use each endpoint defined above, please refer to the [Postman](#postman-tests) section below.

# Getting started

## Pre-requisites

For local run & testing (without Docker or K8S):
- Python 3.8 (or above)
- PyCharm Community Edition 2020 (or any other modern IDE like VS Code)
- Postman v8.0.5 (or above)
- Git

**Additionally**, to build and run with **Docker**:
- VS Code - optional but **highly recommended**, especially for Windows+WSL2 users, + extensions:
  - Python
  - Docker
  - Remote - Containers
  - Kubernetes
  - Remote - Kubernetes
  - Remote - WSL (for WSL2 users)
- Docker Engine 20.10.3 (or higher)

For Mac users, just download and install the latest version of [Docker Desktop for Mac](https://docs.docker.com/docker-for-mac/install/). 

For Windows users, it is **highly** recommended to install Docker Desktop for Windows with the WSL2 backend enabled. This is also officialy the recommended way of developing Docker apps with Windows going forward; for further details check [this](https://docs.docker.com/docker-for-windows/wsl/) guide.

For Linux users, just install Docker Engine directly by following one of [these](https://docs.docker.com/engine/install/ubuntu/) guides (Ubuntu distro for example).

Finally, to run & test your Dockerized container on a local K8S cluster:

- [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation) (or equivalent clients such as Minikube, K3S)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

## Installation
1. Clone this repo on your local machine
```git
git clone https://github.com/ckarakannas/currency-converter-api.git
```
2. Navigate to the projet directory and create a Python virtual environment. For example with the standard **venv** module:
  - On macOS and Linux:
  ```bash
  python3 -m venv venv
  ```
  - On Windows:
  ```cmd
  py -m venv venv
  ```
3. Activate the virtual environment:
- On macOS and Linux:
```bash
source venv/bin/activate
```
- On Windows:
```cmd
.\venv\Scripts\activate
```
4. Install Python dev dependancies
```bash
pip install -r requirements-dev.txt
```
5. Open the project from the root directory with either PyCharm or VS Code. Remember to point the IDE to the venv Python interpreter.

## Quick run
From the command line or within your IDE, run the ```api.py``` file. The app is now listening on localhost:5000. To check that the app is running, you can navigate to [localhost](http://localhost:5000/) on your web-browser and you should see a "Hello World" welcome message.

# Docker

This repo includes the ``Dockerfile`` used to build the Flask app image, which you can pull from [Docker Hub](https://hub.docker.com/r/chrisk14/currency-exchange). As expected, the image is based on the official Python Docker image. Below is a typical workflow on how to containerize and run a Flask app locally with Docker, purposed for two separate environments - dev & prod.

### Dev example

Building and running the app from source code, on a local dev env is as simple as running

```bash
docker build -t cex-api:dev .
```

followed by

```bash
docker run -it --name cex-api-dev -p 5000:5000 cex-api:dev python api.py
```

Alternatively, you can do this in one go by grabbing the existing dev image from Docker Hub:

```bash
docker run -it --name cex-api-dev -p 5000:5000 chrisk14/currency-exchange:dev python api.py
```

### Prod example

For a production-like image with a Gunicorn server hosting the app instance, build using this command

```bash
docker build -t cex-api:prod . --build-arg API_ENV=Production
```

NOTE: The --build-arg 'API_ENV' is case sensitive and API_ENV=Production instructs Docker to build the image using production dependencies, including Gunicorn. By default, the API_ENV is set to 'Deployment'.

Subsequently, to get a running, production-like container, run

```bash
docker run -it -p 5000:5000 --name cex-api-prod cex-api:prod gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

Again, you can do this in one go by grabbing the existing image from Docker Hub:

```bash
docker run -it -p 5000:5000 --name cex-api-prod chrisk14/currency-exchange:prod gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## Docker-Compose

For your reference, this repo includes docker-compose YAML files. With these, you can build from source code and run with a single command using the ``docker-compose`` client. From the root of the repo, run

```bash
docker-compose up -d --build
```

The above defaults to a local dev container. For a production-like container running Gunicorn WSGI, use this command:

```bash
docker-compose -f docker-compose.yml -f production.yml up -d --build
```

# Kubernetes

You can take this one step further by setting up and running the app within your locally managed K8S cluster.

The instructions below are based on the [kind](https://kind.sigs.k8s.io/) client. Feel free to experiment with other Kubernetes clients, such as Minikube etc.

## Creating a local cluster
1. Install kubectl & [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation) - see [pre-requisites](#pre-requisites)
2. Create a single node cluster with preconfigured port mappings and mounts (for dev env) from:

```bash
kind create cluster --config=kubernetes/cluster-config.yaml --name local
```
The ``cluster-config.yaml`` file includes all the config settings required for local deployment with an interactive dashboard explained below. Feel free to experiment with this, but only if you understand how Kind configuration works.

3. This creates a K8S cluster named ``local``. Verify this by running:

```bash
kind get clusters
```
## Create an interactive K8S dashboard

1. Apply the following resources for an interactive K8S dashboard

  ```bash
  kubectl apply -f kubernetes/dashboard-resources.yaml

  kubectl apply -f kubernetes/dashboard-admin-resources.yaml
  ```

2. Start a kubectl proxy

  ```bash
  kubectl proxy --port=51658
  ```

3. Open another terminal and grab secret token for dashboard login

  ```bash
  kubectl -n kubernetes-dashboard describe secret $(kubectl -n kubernetes-dashboard get secret | grep admin-user | awk '{print $1}')
  ```
4. Access the dashboard through this [link](http://localhost:51658/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/). Copy the token printed in the previous step from your terminal, and paste it to login.

With this dashboard, you will be able to view deployments and any other objects you provision within your local cluster.

### Deployment example in K8S

To deploy the sample Flask app on your local cluster run the following on your terminal

```bash
kubectl apply -f kubernetes/dev/flask-deployment.yaml
kubectl apply -f kubernetes/dev/flask-service.yaml
```
These commands will provision a flask-deployment with 2 replicas serving on localhost:30000.

The deployment YAML files instruct Kubernetes to create pods based on the images hosted on my Docker Hub repo, which were created in the previous steps (see the [Docker](#docker) section). Feel free to experiment with these files under the ``kubernetes`` directory to modify the deployment or services.

To scale up or down run
```bash
kubectl scale deployment flask-deployment --replicas=<INT>
```

Similarly for a production-equivalent Flask app, run

```bash
kubectl apply -f kubernetes/prod/flask-deployment.yaml
kubectl apply -f kubernetes/prod/flask-service.yaml
```

### Access on your webrowser

To access these instances on your web browser, simply go to ``localhost:30000`` for dev Pod instances and ``localhost:32000`` for prod Pod instances.


## Deleting cluster

To spin down the local cluster, just run

```
kind delete cluster --name local
```
This will delete the cluster along with all the resources and objects created in this section.

# Postman & Tests
For usage examples and a test collection, run Postman and import all the json files within the ``postman`` directory, including the environment files.

This includes:
- CEX-API.postman_collection.json - refer to this as the basis for interacting with the API and sending valid requests. Make sure you switch to the right environment when you do so
- Environments:
  - Local (when running on local machine and plain Docker Host)
  - K8S-Local-Dev (when running a Dev Pod instance on your local K8S cluster configured as explained [previously](#deployment-example-in-k8s))
  - K8S-Local-Prod (when running a Prod Pod instance on your local K8S cluster configured as explained [previously](#deployment-example-in-k8s))
- CEX-API-Collection-Tests.postman_collection.json
  - A collection that can be used for testing. You can run this tests collection and check that your deployments of this project are working as follows:
    - Run Postman
    - Switch to the correct environment
    - Open a Runner tab
    - Choose the ``CEX-API-Collection-Tests`` as the collection
    - Where it says `Data`, press `Select File`, browse to the `postman` directory from the root and select test_data.csv
    - Finally run the tests. All tests & iterations should return green, as in succesful

# Contributing

Feel free to contribute to this project. Fork and open a pull request.

# License

[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
