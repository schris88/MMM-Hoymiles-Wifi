# MMM-Hoymiles
MagicMirror module for external web widgets

- This module shows current data for Hoymiles Wifi inverter with the help of the hoymiles-wifi python lib
- Project is based on https://github.com/ulrichwisser/MMM-HTMLSnippet
- The Inverter Data is fetched with https://github.com/suaveolent/hoymiles-wifi
- Whenever the widget refreshes the flask server will call the python script which will render a html with the current data from holymiles-wifi

## Installation
```shell
cd ~/MagicMirror/modules/
git clone https://github.com/schris88/MMM-Hoymiles-Wifi
```

### Config example

```javascript
{
  module: "MMM-Hoymiles-Wifi",
  position: "top_left",
  config: {
    width: "300px",
    height: "320px",
    updateInterval: 60000, // in milli seconds
    frames : [
      { src: 'http://127.0.0.1:5000' },
    ]
  },
},
```

### Hoymiles Example
![Hoymiles Example](mmm-hoymiles.jpg)

## Requirements
Install all Python requirements:
```shell
pip install -r requirements.txt
```

Change IP Address in data file:
```shell
~/MagicMirror/modules/MMM-Hoymiles-Wifi/hoymiles_data.py
Change this line to the address of your DTU:
dtu = DTU(“192.168.178.114”)
```

## Start Flask server by running HoymilesWifi.sh or add it to pm2
To start `HoymilesWifi.sh` manually:
```shell
./HoymilesWifi.sh
```

To add `update.sh` to pm2:
```shell
pm2 start HoymilesWifi.sh
pm2 save
```

