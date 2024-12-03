#!/bin/bash
# Run the Python script to generate the HTML file
# Provide the DTU IP address

# Start mongodb container
sudo docker start mongodb

# Delete the existing data in the database (uncomment for clearing database every day if you restart your mm daily)
#sudo docker exec -it mongodb bash -c "mongosh --eval 'use hoymiles && db.energy_data.drop()'"

# Run the Python script to generate the HTML file
python hoymiles_data.py --dtu_ip_address <DTU-IP-ADDRESS> --max <MAX WATTAGE>
