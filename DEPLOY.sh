#!/usr/bin/env bash
set -e

echo "Deploying Ardent Update"

cd /home/ubuntu/Ardent

echo "Pulling latest code"
git pull

echo "Updating dependencies"
.venv/bin/python -m pip install -r requirements.txt

echo "Restarting Ardent"
sudo systemctl restart ardent

echo "Checking service"
sudo systemctl status ardent --no-pager

echo "--Deployment complete--"