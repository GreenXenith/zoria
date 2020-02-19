#!/bin/bash

printf "Username: "
read NAME

printf "Email: "
read EMAIL

echo "Configuring git..."

git config user.name $NAME
git config user.email $EMAIL

git config credential.username $NAME
git config credential.email $EMAIL

echo "Installing pylint..."
pip3 install pylint

echo "Installing pygame..."
pip3 install pygame