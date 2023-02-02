#!/usr/bin/env bash

# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail
IFS=$'\n\t'

###############################################################################
# Rasberry Pi incubator setup. This script sets up a systemd service and a
# cronjob to disply and record information (respectively) about the incubator.
#
# See https://www.adminschoice.com/crontab-quick-reference for an explanation of
# what a crontab is (or type `man crontab`) and https://crontab.guru/ for a nice
# crontab entry editor.
#
# See https://wiki.debian.org/systemd/Services for info about systemd services.

# Update pip to the latest version so it can find binaries required for package
# installation like `cmake`
sudo pip3 install --upgrade pip

# ensure package data is up to date
sudo apt update

# sqlite stores temperature and humidity data locally. liabatlas is a pandas dependency.
sudo apt install sqlite3 libatlas-base-dev

# Since we're installing files from the directory containing this script, we'll
# store the path in a variable.
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
CURRENT_USER=$(whoami)

# Install python library requirements
pip3 install -r $SCRIPT_DIR/requirements.txt

# Substitue in our variable to our crontab template
cat - $SCRIPT_DIR/crontab.template | sed -e "s|SCRIPT_DIR|$SCRIPT_DIR|" >$SCRIPT_DIR/crontab

# Install the crontab. Either appends the crontab in this folder to the user's
# existing crontab or creates a crontab.
crontab -l -u $CURRENT_USER
CRONTAB_EXITCODE=$?
if [[ $CRONTAB_EXITCODE -eq 0 ]]; then
  crontab -l -u $CURRENT_USER | cat - $SCRIPT_DIR/crontab | crontab -u $CURRENT_USER -
else
  cat $SCRIPT_DIR/crontab | crontab -u $CURRENT_USER -
fi

# Install the systemd service. Sub values into the template and move it into place.
cat incubator_admin.service.template | sed -e "s/USERNAME/$CURRENT_USER/" -e "s|SCRIPT_DIR|$SCRIPT_DIR|" >incubator_admin.service
sudo mv $SCRIPT_DIR/incubator_admin.service /etc/systemd/system/incubator_admin_panel.service

# Launch the service
sudo systemctl daemon-reload
sudo systemctl start incubator_admin_panel.service