#!/bin/bash
# Run the Python script to generate the HTML file
# Provide the DTU IP address
sudo docker start mongodb
python hoymiles_data.py --dtu_ip_address <DTU-IP-ADDRESS> --max <MAX WATTAGE>
