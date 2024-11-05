##########################################################################################
# Canonical AI Inc.
# Author: founders@canonical.chat
# Usage: ./kompose.sh
# Description: This script is used to generate
##########################################################################################

# first, check if secrets dir exists, if not, instruct the user to create it
if [ ! -d "secrets" ]; then
  echo "Please create your secrets directory by running the following command: cp -r secrets.example/ secrets"
  echo "After creating the secrets directory, update the values in each file and then run this script again."
  exit 1
fi

# create the app's secret key
export key=$(openssl rand -base64 64)
echo $key > secrets/secretkey.txt

kompose -f compose.yml convert --out ./k8s/
# amend volume mounts
python kompose.py ./k8s/db-deployment.yaml
python kompose.py ./k8s/web-deployment.yaml

kompose -f compose.yml convert -c --out charts
# amend volume mounts
python kompose.py ./charts/templates/db-deployment.yaml
python kompose.py ./charts/templates/web-deployment.yaml