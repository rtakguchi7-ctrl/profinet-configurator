# profinet-config-ui

Web UI and backend for detecting and configuring PROFINET devices via MAC address.

## Features

- Identify devices via MAC address using `profi-dcp`
- Set IP, subnet, gateway, and station name
- Lookup vendor name from MAC address
- Deployable via Portainer using docker-compose

## Usage

1. Clone this repository
2. Deploy using Portainer with `docker-compose.yml`
3. Access backend API at `http://<host>:8000`
