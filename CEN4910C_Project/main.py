# Magnificent 7
# -*- coding: utf-8 -*-

import dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import json
from datetime import datetime

# System Date and Time
now = datetime.now()
dt = now.strftime("%d/%m/%Y %H:%M:%S")

# Read geojson files
d1 = open(r"backend_resources\results\orlando_averaged_2019-01-01.geojson")
data = json.load(d1)
d2 = data["features"][0]

# Extract data from JSON file
d3 = pd.json_normalize(data, record_path=['features'])
base = d3.loc[:, ["properties.NeighName", 'properties.avg_d_mbps']]
base.columns = ["NeighName", "Avg Mbps"]  # change column name

# Function to generate drop-down list (Neighborhood names)

def Neigh_names():

    global base
    base["label"] = base.loc[:, "NeighName"]
    base["value"] = base.loc[:, "NeighName"]
    col_list = base.loc[:, ["label", "value"]]
    col_list = col_list.drop_duplicates("label")
    base = base.drop(["label", "value"], axis=1)  # removing the added coloumn
    new_row = {'label': 'All', 'value': "All"}
    col_list = col_list.append(new_row, ignore_index=True)
    return col_list.to_dict("records")
# ----------Dash App---------------------------------------

app = dash.Dash(__name__)


# reset button
reset_data = html.A(html.Button('Click Here to Reset Map',
                                style={
                                    "position": "absolute",
                                    "top": "825px",
                                    "left": "760.5px",
                                    "right": "842.5px",
                                    "backgroundColor": "white",
                                    "color": "black",
                                    "width": "175px",
                                    "borderRadius": "1vw",
                                    "display": "block",
                                }

                                ), href='/')

# Banner with titles and reset button
banner = html.Div([
    html.H3(["The Digital Divide"],
            className="titleName",
            style={
            "position": "relative",
            "text-align": "left",
            "fontSize": "30pt",
            "color": "#8f9daa",
            "left": "80",
            }
            ),  # ------- First Title
    html.H3(["A comprehensive look at the internet speeds throughout Orlando, Florida and its city districts."],
            className="titleDescription",
            style={
            "text-align": "center",
            "fontSize": "25pt",
            "font-family": "Trebuchet MS",
            "color": "#8f9daa",
            "right": "-100",
            }
            ),  # -----------Second Title
    html.Button("Light Mode", className="colorButton",            
                style={
                    "position": "relative",
                    "float": "right",
                    "font-family": "Trebuchet MS"
                }
                ),

    reset_data  # -----Reset button

],
id="headerDiv",
    style={
        "position": "relative",
        "overflow": "hidden",
        "top": "0",
        "left": "0",
        "right": "0",        
        "backgroundColor": "#1d2b37",
}
)

# images of graphs

image = html.Img(src=app.get_asset_url('up.png'), style={
                                    "position": "absolute",
                                    "left": "600.5px",
                                    "right": "842.5px",
                                    "top": "860px",
                                    "borderRadius": "1vw",
                                    "display": "block",
                                })
image2 = html.Img(src=app.get_asset_url('down.png'), style={
                                     "position": "absolute",
                                     "left": "583.5px",
                                     "right": "842.5px",
                                     "top": "1150px",
                                     "borderRadius": "1vw",
                                     "display": "block",
                                 })
image3 = html.Img(src=app.get_asset_url('highinc.png'), style={
                                     "position": "absolute",
                                     "left": "600.5px",
                                     "right": "842.5px",
                                     "top": "1440px",
                                     "borderRadius": "1vw",
                                     "display": "block",
                                 })
image4 = html.Img(src=app.get_asset_url('lowinc.png'), style={
                                        "position": "absolute",
                                        "left": "600.5px",
                                        "right": "842.5px",
                                        "top": "1780px",
                                        "borderRadius": "1vw",
                                        "display": "block",
                                 })

# Background image

BGimage = html.Img(src=app.get_asset_url('orlando-981748_1920.jpg'), style={
                                         "alignment": "center",
                                         "bottom": "0px",
                                         "opacity": "25%",
                                         "position": "fixed",
                                         "width": "100%",
                                         "height": "auto"
                                 })
# ---Quarter Drop Down element

drop_down = html.Div([
    dcc.Dropdown(
        id="time",
        options=[
            {'label': 'Q1 2019', 'value': '2019-01-01'},
            {'label': 'Q2 2019', 'value': '2019-04-01'},
            {'label': 'Q3 2019', 'value': '2019-07-01'},
            {'label': 'Q4 2019', 'value': '2019-10-01'},
            {'label': 'Q1 2020', 'value': '2020-01-01'},
            {'label': 'Q2 2020', 'value': '2020-04-01'},
            {'label': 'Q3 2020', 'value': '2020-07-01'},
            {'label': 'Q4 2020', 'value': '2020-10-01'},
            {'label': 'Q1 2021', 'value': '2021-01-01'},
            {'label': 'Q2 2021', 'value': '2021-04-01'},
            {'label': 'Q3 2021', 'value': '2021-07-01'},

        ],
        value="2021-07-01",
        searchable=True,
        placeholder="Select a Quarter from drop-down",
                    style={"margin": "10px,0,10px,0",
                            "width": "200px", "color": "grey",
                           "font-family": "Trebuchet MS"},
    )],
    style={
    "borderColor": "black",
    "display": "inline-block",
    "marginLeft": "50px"
},
)

# Download and Upload speed dropdown element
speed = html.Div([
    dcc.Dropdown(
        id="internet",
        options=[
            {'label': 'Upload Speeds', 'value': 'avg_u_mbps'},
            {'label': 'Download Speeds', 'value': 'avg_d_mbps'}


        ],
        value="avg_d_mbps",
        searchable=True,
        placeholder="Upload/Download Select",
        style={
            "marginLeft": "10px",
            "width": "200px",
            "color": "grey",
            "font-family": "Trebuchet MS"
        },
    )],
    style={
    "borderColor": "black",
    "display": "inline-block",
    "marginLeft": "50px"
},
)

# Neighborhood names dropdown (this uses the function defined at the top)
NeighHood_names = html.Div([

    dcc.Dropdown(
        id="Neigh_names",
        options= sorted(Neigh_names(), key=lambda item: item.get("label")),  # function calling
        value="All",
        searchable=True,
        placeholder="Select neighborhood",
        style={
            "width": "200px",
            "color": "grey",
            "marginLeft": "10px",
            "font-family": "Trebuchet MS"
        },
    )
],
    style={
    "borderColor": "red",
    "display": "inline-block",
    "marginLeft": "100px"
})


# Choropleth Map element

final_map = html.Div([dcc.Graph(id="map")],
                     style={


    "position": "absolute",
    "top": "354px",
    "left": "387.5px",
    "right": "387.5px",
    "width": "910px",
    "height": "300px",
    "display": "inline-block"

})

# UI layout design (Include the formating, colors and the way drop downs will be arranged in the dashboard)


container_0 = html.Div([
    NeighHood_names,
    drop_down, speed,
    html.Br()
],
    style={
    "position": "absolute",
    "top": "274px",
    "left": "338px",
    "right": "295px",
    "width": "911px",
    "backgroundColor": "#192734",
    "paddingTop": "20px",
    "paddingBottom": "20px",
    "border-width": "thick thick thick thick",
    "display": "inline-block",
    "marginLeft": "50px",

})

# Last updated element 

Last_updated = html.Div(
    id='date', style={"position": "absolute",
                      "marginLeft": "50px",
                      "marginTop": "10px",
                      "color": "#8f9daa",
                      "font-family": "Trebuchet MS"})





# Final layout container with graphs and other elements

container_1 = html.Div([
    html.Div([
        BGimage,
        banner,
        Last_updated,
        html.Br(),
        html.Br(),
        html.Br(),
        container_0,
        final_map,
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        image,
        image2,
        image3,
        image4

    ],
        style={
        "position": "absolute",
        "top": "0px",
        "left": "0px",
        "right": "0px",
        "bottom": "0px",
        "width": "100%",
        "height": "2200px",
        "backgroundColor": "#15202B",
        "margin": "0",
        "padding": "0"
    },
    id = "bodyBackgroundColor"
    ),

    
])

# Final Layout
app.layout = html.Div([container_1])

# App callback
@app.callback(
    [Output('map', "figure"), Output('date', "children")],
    [Input('time', 'value'), Input("Neigh_names",
                                   "value"), Input("internet", "value")],
    prevent_initial_callbacks=True
)
# call back function
def update_map(qrt, name, int_speed):
    d1 = open(r"backend_resources\results\orlando_averaged_" + qrt + ".geojson")
    data = json.load(d1)
    base = pd.json_normalize(data, record_path=['features'])
    base = base.iloc[:, [6, 7, 8]]
    base.columns = ["NeighName", "avg_d_mbps", "avg_u_mbps"]
    if name != "All":
        base = base.loc[base.loc[:, "NeighName"] == name, ]

    # Plotly Choropleth Graph
    fig = px.choropleth_mapbox(base, geojson=data, locations="NeighName", color=int_speed, featureidkey="properties.NeighName",
                               center={"lat": 28.488137, "lon": -81.331054},
                               color_continuous_scale="tempo",
                               mapbox_style="carto-positron", zoom=10)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    #date and time
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")

    return fig, dt

if __name__ == '__main__':
    app.run_server(debug=True)