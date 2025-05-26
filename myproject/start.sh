#!/bin/bash

echo "== DO you want to open intitail Docker? =="
read -p "DO you want to open intitail Docker? (y/n): " install_req
if [[ $install_req == "y" ]]; then
    docker compose --profile server up -d
fi

echo "== docker compose build cli? =="
read -p "docker compose build cli? (y/n): " install_req
if [[ $install_req == "y" ]]; then
    docker compose build cli
fi

echo "== docker compose run cli? =="
read -p "docker compose run cli? (y/n): " install_req
if [[ $install_req == "y" ]]; then
    docker compose run cli
fi