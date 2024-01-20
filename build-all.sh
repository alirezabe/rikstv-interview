#!/bin/bash

docker image build -f ./src/kafka/Dockerfile-consumer -t consumer ./src/kafka/
docker image build -f ./src/kafka/Dockerfile-producer -t producer ./src/kafka/
docker image build -f ./src/app/Dockerfile -t app ./src/app/

echo "ALL Build Done"