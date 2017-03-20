#!/bin/bash

# Detect if we have the autopilot plugin
if ! $(cf plugins | grep -q zero-downtime-push)
then
  echo "Please install autopilot plugin to allow for zero downtime deployments."
  echo "More details here: https://github.com/contraband/autopilot"
  exit 1
fi

# Detect that we have enough arguments
if [ $# -ne 1 ]
then
  echo "Please provide the space to deploy as an argument"
  echo "Usage:"
  echo -e "\t./deploy.sh <space>"
  echo
  echo "Example:"
  echo -e "\t./deploy.sh prod"
  exit 1
fi

# Detect that we have the right arguments
case "$1" in
  "prod")
    MANIFEST_FILE="manifest-prod.yml"
    ;;
  "staging")
    MANIFEST_FILE="manifest-staging.yml"
    ;;
  "dev")
    MANIFEST_FILE="manifest-dev.yml"
    ;;
  *)
    echo "Unknown space '$1'"
    exit 1
    ;;
esac

echo "Using manifest file $MANIFEST_FILE to deploy to space $1."
echo
echo

# Let's try to get deployer credentials from the environment.
# There's a pattern to follow for using variables
# The username should be set to a variable named 'CF_USERNAME_<SPACE>'
# The password should be set to a variable named 'CF_PASSWORD_<SPACE>'
# Example:
# Given we are trying to deploy to the "prod" space. The variables to use are:
# CF_USERNAME_PROD and CF_PASSWORD_PROD
# If the appropriate variables are not found, will use the credentials for the
# currently logged in user. Helpful for manual deploys by developer.
CF_USERNAME_VARIABLE_NAME=$(echo CF_USERNAME_$1 | awk '{print toupper($0)}')
CF_PASSWORD_VARIABLE_NAME=$(echo CF_PASSWORD_$1 | awk '{print toupper($0)}')
echo "Looking for the following envionment variables to be set:"
echo "Deployer username should be set via '$CF_USERNAME_VARIABLE_NAME'"
echo "Deployer password should be set via '$CF_PASSWORD_VARIABLE_NAME'"
echo
echo

eval "CF_USERNAME=\$$CF_USERNAME_VARIABLE_NAME"
eval "CF_PASSWORD=\$$CF_PASSWORD_VARIABLE_NAME"

if [ ! -z "$CF_PASSWORD" ] && [ ! -z "$CF_USERNAME" ]
then
  echo "Found $CF_USERNAME_VARIABLE_NAME and $CF_PASSWORD_VARIABLE_NAME"
  echo "Will try to login with those credentials."
  cf login -a "https://api.fr.cloud.gov" -u "$CF_USERNAME" -p "$CF_PASSWORD" -o "doi-ekip" -s $1
else
  echo "No deployer credentials found."
  echo "Will use the credentials of current user."
  cf target -o "doi-ekip" -s $1
fi
cf zero-downtime-push ekip -f $MANIFEST_FILE
