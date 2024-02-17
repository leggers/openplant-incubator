# OpenPlant Incubator (Current)

The pi_incubator contains the latest code running on the Raspberry Pi in the incubators in GenSpace at time of writing (Feb 2024). They record data to an on-device SQLite database and serve the data for visualization using the [Plotly Dash](https://dash.plotly.com/) library to define and serve the website with only a Python installation on the device. Connectivity to the device is a choose-your-own-adventure. We use [Tailscale](https://tailscale.dev/) at Genspace.

## Setup

**NB: This guide assumes you are on the same network as the pi.**

1) (Optional): Flash your device. 64bit ideally. Set up SSH so you don't need a mouse and keyboard to access the device! The [Raspberry Pi Imager](https://www.raspberrypi.com/software/) tool is the recommended way to do this.
2) SSH to the device
3) Install Tailscale by running `curl -fsSL https://tailscale.com/install.sh | sh`. This will allow you to access it from anywhere.
4) Install git by running `sudo apt-get update && sudo apt-get install -y git screen`
5) Clone this repo by running `git clone https://github.com/leggers/openplant-incubator.git`. TODO: update this to point to the `genspace/openplant-incubator` project once this has been approved
6) Check out the `leggers-scratch` branch by running `cd openplant-incubator && git checkout leggers-scratch`
7) Start a `screen` session so you can disconnect from the pi while the setup script is running by running the `screen` command. You can resume your screen later by running `screen -r` from another interactive session.
8) Install the `pi_incubator` code by running `./pi_incubator/setup.sh`. Disconnect from the `screen` session by pressing `ctrl-a` then `d`. The installation script will continue to run in the background.
9) After a while everything should be up and running. You should be able to see the data visualization on port 8000 on the pi. Putting `<pi IP>:8000` into your browser's address bar should show it!

Clone this repo onto the Pi and run `./pi_incubator/setup.sh` from the root of the repo. That should be all that's necessary to start the pi collecting data and serving the data visualization on port 8000!

# OpenPlant Incubator (Previous)

The code in this repository is open sourced and provides tools to develop a plant incubator with cloud-based monitoring services. At Genspace, we run this code to log regular measurements of plants being grown in our incubator after which information is made available for further analysis via direct query of a Postgres database running on an EC2 server as well as a cache of processed images of our samples that are binned in s3. We hope this repository can be used as a model to inspire similar work among other research teams.

![Software Schematic](./software_schematic.png)

https://trello.com/b/W0jccEJs/welcome-to-the-project

Please feel free to get in touch with the team.
