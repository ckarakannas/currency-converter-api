FROM python:3.8
ARG API_ENV=Development
ENV API_ENV=${API_ENV}
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements requirements/
RUN pip install --no-cache-dir -r requirements/${API_ENV}.txt
COPY ./ /usr/src/app