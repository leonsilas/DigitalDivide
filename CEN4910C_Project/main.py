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
from waitress import serve

import os


#Choropleth color options Changes Here
colorscales = px.colors.named_colorscales()


# System Date and Time
now = datetime.now()
dt = now.strftime("%d/%m/%Y %H:%M:%S")

# Read geojson files
d1 = open(r"backend_resources/results/orlando_averaged_2019-01-01.geojson")
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
app.title = "Digital Divide" # set the app title in the browser tab

# a favicon is the 16x16px icon displayed in the browser tab
# Orlando's fountain icon may only be used with permission from the city
# app._favicon = ("path_to/icon.ico")

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

# Logo image

logo = html.Img(src=app.get_asset_url('DigitalDivide_logo_320x240.png'), style={
                                      "position": "absolute",
                                      "top": "-40px",
                                      "height": "180px",
                                      "opacity": "67%"
                                 })

# Banner with titles and reset button
banner = html.Div([
    html.H3(dcc.Link(logo, href='/'),
            className="titleName",
            style={
            "position": "relative",
            "left": "60",
            }
            ),  # ------- First Title
    html.H3(["A comprehensive look at the internet speeds throughout Orlando, Florida and its city districts."],
            className="titleDescription",
            style={
            #"text-align": "right",
            "position": "relative",
            "left": "256px",
            "top": "10px",
            "marginRight": "300px",
            "fontSize": "25pt",
            "font-family": "Trebuchet MS",
            "color": "white",
            "opacity": "67%",
            "max-width": "80%"
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

image = html.Img(src='assets/upSpeed.png', style={
                                    "margin": "0 auto",
                                    "display": "block",
                                    "borderRadius": "1vw",
                                    "position": "relative",
                                    "zIndex": "999",
                                })
image2 = html.Img(src=app.get_asset_url('downSpeed.png'), style={
                                     "margin": "0 auto",
                                     "borderRadius": "1vw",
                                     "display": "block",
                                     "position": "relative",
                                     "zIndex": "999",
                                 })
image3 = html.Img(src=app.get_asset_url('highIncome.png'), style={
                                     "margin": "0 auto",
                                     "borderRadius": "1vw",
                                     "display": "block",
                                     "position": "relative",
                                     "zIndex": "999",
                                 })
image4 = html.Img(src=app.get_asset_url('lowIncome.png'), style={
                                        "margin": "0 auto",
                                        "borderRadius": "1vw",
                                        "display": "block",
                                        "position": "relative",
                                        "zIndex": "999",
                                 })

# Background image

BGimage = html.Img(src=app.get_asset_url('orlando-cityscape.jpg'), style={
                                         "alignment": "center",
                                         "bottom": "0px",
                                         "opacity": "25%",
                                         "position": "fixed",
                                         "min-height": "100%",
                                         "zIndex": "0",
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
                            "width": "190px", "color": "grey",
                           "font-family": "Trebuchet MS"},
    )],
    style={
    "borderColor": "black",
    "display": "inline-block",
},
)
#Changes Here
colors = html.Div([
    dcc.Dropdown(
        id="colors",
        options=colorscales,
        value='tempo',
        style={
            "width": "190px",
            "color": "grey",
            "font-family": "Trebuchet MS"
        },
        placeholder="Colors"
    )
])
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
            "width": "190px",
            "color": "grey",
            "font-family": "Trebuchet MS"
        },
    )],
    style={
    "borderColor": "black",
    "display": "inline-block",
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
            "width": "190px",
            "color": "grey",
            "font-family": "Trebuchet MS"
        },
    )
],
    style={
    "borderColor": "red",
    "display": "inline-block",
})


# Choropleth Map element

final_map = html.Div([dcc.Graph(id="map")],
                     style={

    "width": "911px",
    "height": "300px",
    "margin": "0 auto"    

})

# UI layout design (Include the formating, colors and the way drop downs will be arranged in the dashboard)


container_0 = html.Div([
    NeighHood_names,
    drop_down, speed,colors #Changes Here
],
    style={
    "display": "flex",
    "justify-content": "space-evenly",
    "width": "911px",
    "backgroundColor": "#192734",
    "paddingTop": "20px",
    "paddingBottom": "20px",
    "border-width": "thick thick thick thick",
    "margin": "0 auto",
    "position": "relative", # keeps background color intact
    "zIndex": "999",
    },
    id="heatMap"
    )

container_3 = html.Div([
    image, image2, image3, image4
],
    style={
    "display": "flex",
    "flex-direction": "column",
    "row-gap": "30px",
    "margin": "50px",
    "zIndex": "999",
})


# Last updated element 

Last_updated = html.Div(
    id='date', style={"position": "absolute",
                      "marginLeft": "50px",
                      "display": "none",
                      "marginTop": "10px",
                      "color": "white",
                      "opacity": "67%",
                      "font-family": "Trebuchet MS"})


# Graphs link
graphs = html.H3(["VIEW GRAPHS"],
                 className="graphsLink",
                 style={
                 "position": "relative",
                 "top": "160px",
                 "width": "100%",
                 "textAlign": "center",
                 "fontSize": "25pt",
                 "font-family": "Trebuchet MS",
                 "color": "white",
                 "opacity": "67%",
                 })

# Home link
home = html.H3(["BACK"],
               className="homeLink",
               style={
               "position": "relative",
               "width": "100%",
               "textAlign": "center",
               "fontSize": "25pt",
               "font-family": "Trebuchet MS",
               "color": "white",
               "opacity": "67%",
               })





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
        dcc.Link(graphs, href='/graphs'),

    ],
        style={
        "position": "absolute",
        "top": "0px",
        "left": "0px",
        "right": "0px",
        "bottom": "0px",
        "width": "100%",
        "backgroundColor": "#15202B",
        "margin": "0",
        "padding": "0"
    },
    id = "bodyBackgroundColor"
    ),

    
])

container_2 = html.Div([
    html.Div([
        BGimage,
        banner,
        container_3,
        dcc.Link(home, href='/'),
        html.Br(),

    ],
        style={
        "position": "absolute",
        "top": "0px",
        "left": "0px",
        "right": "0px",
        "bottom": "0px",
        "width": "100%",
        "height": "1607px",
        "backgroundColor": "#15202B",
        "margin": "0",
        "padding": "0"
    },
    id = "bodyBackgroundColor"
    ),

    
])

# Final Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

home_page = html.Div([container_1])

graphs_layout = html.Div([container_2])

@app.callback(Output('graphs-content', 'children'),
                  [Input('url', 'pathname')])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/graphs':
        return graphs_layout
    else:
        return home_page


# App callback
@app.callback(
    [Output('map', "figure"), Output('date', "children")],
    [Input('time', 'value'), Input("Neigh_names",                        #Changes Here
                                   "value"), Input("internet", "value"), Input("colors", "value")],
    prevent_initial_callbacks=True
)
# call back function
def update_map(qrt, name, int_speed, colors):
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
                               color_continuous_scale=colors, #Changes Here
                               mapbox_style="carto-positron", zoom=10)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    #date and time
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")

    return fig, dt

if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False)
    serve(app)
