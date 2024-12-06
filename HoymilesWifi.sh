#!/bin/bash
# Run the Python script to generate the HTML file
# Provide the DTU IP address

# Start mongodb container
sudo docker start mongodb

# Run the Python script to generate the HTML file
python hoymiles_data.py --dtu_ip_address <DTU-IP-ADDRESS> --max <MAX WATTAGE>
