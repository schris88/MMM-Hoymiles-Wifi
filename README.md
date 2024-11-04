# MMM-Hoymiles
MagicMirror module for external web widgets

- This module shows current data for Hoymiles Wifi inverter with the help of the hoymiles-wifi python lib
- Project is based on https://github.com/ulrichwisser/MMM-HTMLSnippet
- The Inverter Data is fetched with https://github.com/suaveolent/hoymiles-wifi
- Whenever the widget refreshes the flask server will call the python script which will render a html with the current data from holymiles-wifi

## Installation
```shell
cd ~/MagicMirror/modules/
git clone https://github.com/stengelchristian/MMM-Hoymiles.git
```

### Config example

```javascript
{
  module: "MMM-HTMLSnippet",
  position: "top_left",
  config: {
    width: "180px",
    height: "100px",
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

## Start update.sh or add it to pm2
To start `update.sh` manually:
```shell
./update.sh
```

To add `update.sh` to pm2:
```shell
pm2 start update.sh
```

