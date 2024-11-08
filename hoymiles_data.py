import asyncio
from flask import Flask, render_template_string
from hoymiles_wifi.dtu import DTU
import plotly.graph_objects as go
from jinja2 import Template

app = Flask(__name__)

async def get_dtu_data():
    dtu = DTU("192.168.178.114")
    response = await dtu.async_get_real_data_new()

    # Print the response to the console
    print(f"DTU Response: {response}")

    if response:
        # Assuming you want to process the first pv_data entry
        pv_data = response.pv_data[0]
        power = pv_data.power / 10.0
        energy_total = pv_data.energy_total
        energy_daily = pv_data.energy_daily
        current = pv_data.current / 10

        # Create gauge graphic
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=power,
            number={'suffix': " W",'valueformat': '.1f', 'font': {'size': 24}},  # Format the number to one decimal place
            gauge={'axis': {'range': [0, 420], 'tickcolor': 'white', 'tickfont': {'color': 'white'}},
                   'bar': {'color': 'blue'},
                   'bgcolor': 'black',
                   'borderwidth': 2,
                   'bordercolor': 'white'},
            domain={'x': [0, 1], 'y': [0.8, 1]}  # Adjust vertical positioning
        ))

        # Add additional trace for energy daily
        fig.add_trace(go.Indicator(
            mode="number",
            value=energy_daily,
            title={'text': "Heute", 'font': {'color': 'white', 'size': 16}},
            number={'suffix': " Wh", 'font': {'size': 12}},
            domain={'x': [0.3, 0.5], 'y': [0.65, 0.75]}  # Adjust vertical positioning
        ))

        # Add additional trace for energy daily
        fig.add_trace(go.Indicator(
            mode="number",
            value=energy_daily,
            title={'text': "Heute", 'font': {'color': 'white', 'size': 16}},
            number={'suffix': " Wh", 'font': {'size': 12}},
            domain={'x': [0.2, 0.4], 'y': [0.65, 0.75]}  # Adjust vertical positioning
        ))

        # Add additional trace for energy total
        fig.add_trace(go.Indicator(
            mode="number",
            value=energy_total,
            title={'text': "Gesamt", 'font': {'color': 'white', 'size': 16}},
            number={'suffix': " Wh", 'font': {'size': 12}},
            domain={'x': [0.6, 0.8], 'y': [0.65, 0.75]}  # Adjust vertical positioning
        ))

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

        # Render the HTML with the gauge graphic and energy total
        html_content = template.render(gauge_html=gauge_html, energy_total=energy_total, energy_daily=energy_daily)

        return html_content
    else:
        return "Unable to get response!"

@app.route('/')
def index():
    html_content = asyncio.run(get_dtu_data())
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True)