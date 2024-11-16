import sys
import argparse
from ipaddress import ip_address
from hoymiles_wifi.dtu import DTU
import json
import asyncio
from flask import Flask, render_template_string
import plotly.graph_objects as go
from jinja2 import Template

#####################
# ***** ARGS ****** #
#####################

parser = argparse.ArgumentParser(
    prog = 'hoymiles_data.py',
    description = 'Get data from Hoymiles inverter'
    )
parser.add_argument('--dtu_ip_address', default = '', type=ip_address, required=True, help = "where DTU-IP-ADDRESS has the format aaa.bbb.ccc.ddd")
parser.add_argument('--debug', action = "store_true", default=False, required=False, help = "turn on debugging")
parser.add_argument('--test', action = "store_true", default=False, required=False, help = "use a test dataset")

args = parser.parse_args()
if args.dtu_ip_address:
    dtuIpAddress = str(args.dtu_ip_address)
else:
    dtuIpAddress = ''

####################
# ***** VARS ***** #
####################

testDataFile = './response_test_data.json'

app = Flask(__name__)

####################
# ***** DEFS ***** #
####################

def createGaugeGraphic(power, energy_total, energy_daily):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=power,
        title={'text': "Power (W)", 'font': {'color': 'white', 'size': 16}},
        number={'suffix': " W",'valueformat': '.1f', 'font': {'size': 24}}, # Format the number to one decimal place
        gauge={'axis': {'range': [0, 800], 'tickcolor': 'white', 'tickfont': {'color': 'white'}},
               'bar': {'color': 'white'},
               'bgcolor': 'black',
               'borderwidth': 2,
               'bordercolor': 'white'},
        domain={'x': [0, 1], 'y': [0.8, 1]}  # Adjust vertical positioning
    ))

    # Add additional trace for energy daily
    fig.add_trace(go.Indicator(
        mode="number",
        value=energy_daily,
        title={'text': "Today", 'font': {'color': 'white', 'size': 16}},
        number={'suffix': " Wh", 'font': {'size': 12}},
        domain={'x': [0.2, 0.4], 'y': [0.65, 0.75]}  # Adjust vertical positioning
    ))

    # Add additional trace for energy total
    fig.add_trace(go.Indicator(
        mode="number",
        value=energy_total,
        title={'text': "Total", 'font': {'color': 'white', 'size': 16}},
        number={'suffix': " Wh", 'font': {'size': 12}},
        domain={'x': [0.6, 0.8], 'y': [0.65, 0.75]}  # Adjust vertical positioning
    ))
    
    # Update layout
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white", 'family': "Arial"},
        margin=dict(t=50, b=0, l=0, r=0)  # Small margins around the plot
    )

    # Save the gauge graphic as an HTML div
    gauge_html = fig.to_html(full_html=False)

    # HTML template
    template = Template("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DTU Data</title>
    </head>
    <body>
        <div>
            {{ gauge_html | safe }} 
        </div>
    </body>
    </html>
    """)

    return (template, gauge_html)

def parse_dtu_data(testDataFile):
    response = ''
    (def_result, power, energy_total, energy_daily) = (0, 0, 0, 0)
    try:
        with open(testDataFile, 'r') as file:
            try:
                response = json.load(file)
            except (IOError, OSError):
                print('ERROR: Cannot open file response_test_data.json')
    except (FileNotFoundError, PermissionError, OSError):
        print('ERROR: Cannot open file response_test_data.json')

    # Print the response to the console
    print(f"DTU Response:")
    print(f"{json.dumps(response, indent=2)}")

    if response:
        ## !! NOTE: the output from the hoymiles-wifi command
        ##          is different that from the Python dtu.async_get_real_data_new() call
        ##          sgData == sgs_data
        ##          pvData == pv_data
        ##          portNumber = port_number
        ##          etc.
        try:
            port_number_0 = int(response['pvData'][0]['portNumber'])
        except KeyError:
            port_number_0 = 0
        try:
            power_0 = int(response['pvData'][0]['power']) / 10
        except KeyError:
            power_0 = 0
        try:
            energy_total_0 = int(response['pvData'][0]['energyTotal'])
        except KeyError:
            energy_total_0 = 0
        try:
            energy_daily_0 = int(response['pvData'][0]['energyDaily'])
        except KeyError:
            energy_daily_0 = 0
        try:
            current_0 = int(response['pvData'][0]['current']) / 10
        except KeyError:
            current_0 = 0
        try:
            port_number_1 = int(response['pvData'][1]['portNumber'])
        except KeyError:
            port_number_1 = 0
        try:
            power_1 = int(response['pvData'][1]['power']) / 10
        except KeyError:
            power_1 = 0
        try:
            energy_total_1 = int(response['pvData'][1]['energyTotal'])
        except KeyError:
            energy_total_1 = 0
        try:
            energy_daily_1 = int(response['pvData'][1]['energyDaily'])
        except KeyError:
            energy_daily_1 = 0
        try:
            current_1 = int(response['pvData'][1]['current']) / 10
        except KeyError:
            current_1 = 0
    else:
        # Unable to get response!
        port_number_0 = 0
        power_0 = 0
        energy_total_0 = 0
        energy_daily_0 = 0
        current_0 = 0
        port_number_1 = 0
        power_1 = 0
        energy_total_1 = 0
        energy_daily_1 = 0
        current_1 = 0

    print(f"port_number_0: {port_number_0}")
    print(f"power_0: {power_0}")
    print(f"energy_total_0: {energy_total_0}")
    print(f"energy_daily_0: {energy_daily_0}")
    print(f"current_0: {current_0}")
    print(f"port_number_1: {port_number_1}")
    print(f"power_1: {power_1}")
    print(f"energy_total_1: {energy_total_1}")
    print(f"energy_daily_1: {energy_daily_1}")
    print(f"current_1: {current_1}")

    power = power_0 + power_1
    energy_total = energy_total_0 + energy_total_1
    energy_daily = energy_daily_0 + energy_daily_1
    print(f"power: {power}")
    print(f"energy_total: {energy_total}")
    print(f"energy_daily: {energy_daily}")

    return (def_result, power, energy_total, energy_daily)

async def get_dtu_data():
    if not args.test:
        dtu = DTU(dtuIpAddress)
        response = await dtu.async_get_real_data_new()

        if args.debug: print(f"DTU Response:")
        if args.debug: print(f"{response}")

        if response:
            # Panel 1 (pv_data[0])
            pv_data_0 = response.pv_data[0]
            power_0 = pv_data_0.power / 10.0
            try:
                energy_total_0 = pv_data_0.energy_total
            except KeyError:
                energy_total_0 = 0
            energy_daily_0 = pv_data_0.energy_daily
            #current_0 = pv_data_0.current / 10
            # Panel 2 (pv_data[1])
            pv_data_1 = response.pv_data[1]
            power_1 = pv_data_1.power / 10.0
            energy_total_1 = pv_data_1.energy_total
            energy_daily_1 = pv_data_1.energy_daily
            #current_1 = pv_data_1.current / 10

            power = power_0 + power_1
            energy_total = energy_total_0 + energy_total_1
            energy_daily = energy_daily_0 + energy_daily_1
        else:
            # Unable to get response!
            power = 0
            energy_total = 0
            energy_daily = 0
            #current = 0

        print(f"power: {power}")
        print(f"energy_total: {energy_total}")
        print(f"energy_daily: {energy_daily}")

    if args.test:
        if args.debug: print(f"DEBUG: test run using dataset is {args.test}")
        (def_result, power, energy_total, energy_daily) = parse_dtu_data(testDataFile)
        if def_result != 0:
            (power, energy_total, energy_daily) = (0, 0, 0, 0)
    
    (template, gauge_html) = createGaugeGraphic(power, energy_total, energy_daily)

    # Render the HTML with the gauge graphic and energy total
    html_content = template.render(gauge_html=gauge_html, energy_total=energy_total, energy_daily=energy_daily)

    return html_content

@app.route('/')
def index():
    html_content = asyncio.run(get_dtu_data())
    return render_template_string(html_content)

####################
# ***** MAIN ***** #
####################

if __name__ == '__main__':
    html_content = app.run(debug=args.debug)
    if html_content != 0:
        sys.exit("Exiting program due to error(s)")
