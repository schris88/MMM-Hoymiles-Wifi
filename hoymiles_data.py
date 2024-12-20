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
parser.add_argument('--dtu_ip_address', default = '192.168.178.123', type=ip_address, required=True, help = "where DTU-IP-ADDRESS has the format aaa.bbb.ccc.ddd")
parser.add_argument('--max', default = '100', type=int , required=True, help = "Max power your gauge should show")
parser.add_argument('--test', action = "store_true", default=False, required=False, help = "use a test dataset")

args = parser.parse_args()

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
        number={'suffix': " W",'valueformat': '.1f', 'font': {'size': 24}}, # Format the number to one decimal place
        gauge={'axis': {'range': [0, args.max], 'tickcolor': 'white', 'tickfont': {'color': 'white'}},
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
    <body">
        <div>
            {{ gauge_html | safe }} 
        </div>
    </body>
    </html>
    """)

    return (template, gauge_html)

async def get_dtu_data():
    response = None
    if not args.test:
        print(f"Getting data from DTU with IP address: {args.dtu_ip_address}")
        dtu = DTU(str(args.dtu_ip_address))  # Convert IPv4Address to string
        response = await dtu.async_get_real_data_new()

    if args.test:
        try:
            with open(testDataFile, 'r') as file:
                response = json.load(file)
        except (FileNotFoundError, PermissionError, OSError):
            print('ERROR: Cannot open file response_test_data.json')
            return None

    print(f"Response: {response}")

    power = 0
    energy_total = 0
    energy_daily = 0
    
    if response :
        pv_data = response.pv_data
        power = response.dtu_power / 10.0
        energy_total = pv_data[0].energy_total
        energy_daily = response.dtu_daily_energy

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
    html_content = app.run()
    if html_content != 0:
        sys.exit("Exiting program due to error(s)")
