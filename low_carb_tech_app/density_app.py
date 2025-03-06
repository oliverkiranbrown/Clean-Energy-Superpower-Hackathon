import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from load_data import load_data
import json
import numpy as np

from dash.dash_table.Format import Format, Scheme

# Sample data (replace with your actual data)
with open("data/gsp_regions_processed.geojson") as f:  # Replace with your GeoJSON file path
    geojson_data = json.load(f)
with open("data/gsp_group_central_location.json") as f:  
    central_location_gsp_group = json.load(f)
# Create DataFrame
df = load_data()
gsp_level_predictions = pd.read_csv("data/gsp_level_predictions.csv")
gsp_level_predictions = gsp_level_predictions[gsp_level_predictions["pred_sum"] > 0]
gsp_group_level_predictions = gsp_level_predictions.groupby("GSPGroup")[["pred_sum", "area_km2"]].sum().reset_index()
gsp_level_predictions["log_pred_normalized"] = np.log10(gsp_level_predictions["pred_sum"] + 1)
gsp_level_predictions.rename(columns={"pred_sum": "Predicted No Of EVs"}, inplace=True)
gsp_group_data = json.load(open("./data/gspgroups.json"))
gsp_group_level_predictions["name"] = gsp_group_level_predictions["GSPGroup"].map(lambda x: gsp_group_data[x])
# Initialize Dash app
app = dash.Dash(__name__)
app.title = "UK EV Map"
GSPgroup_list = gsp_group_level_predictions.to_dict("records")
fig = px.choropleth_mapbox(
    gsp_level_predictions,
    geojson=geojson_data,
    locations="GSPs",  # Column in the DataFrame
    featureidkey="properties.GSPs",  # Key in GeoJSON properties
    color="log_pred_normalized",  # Column to use for coloring
    mapbox_style="carto-positron",
    hover_data={"GSPs": True, "Predicted No Of EVs": True, "log_pred_normalized": False},  # Show additional data on hover
    zoom=4.5,  # Adjust zoom for UK
    center={"lat": 55.0, "lon": -2.4},  # Center for UK
)
fig.update_layout(
    mapbox_style="carto-positron",
    margin={"r": 10, "t": 0, "l": 0, "b": 0},
    coloraxis_colorbar=dict(
        title="",
        tickvals=[gsp_level_predictions["log_pred_normalized"].min(),
                  gsp_level_predictions["log_pred_normalized"].max()],
        ticktext=["Fewer EVs", "More EVs"],  # Custom labels
        tickmode="array",
        len=0.7,  # Adjust length of the colorbar (optional aesthetic)
    )
)

# Layout
app.layout = html.Div(
    [
        # Title at the top
        html.H1(
            "Grid Supply Point Level distribution of EVs",
            style={
                "fontFamily": "Roboto, sans-serif",
                "textAlign": "center",
                "marginBottom": "20px",
                "fontWeight": "bold",
                "color": "#333333",  # Modern dark gray
            },
        ),
        # Main content with slider on the left and map on the right
        html.Div(
            [
                # Slider section on the left
                html.Div(
                    [
                        # Table for GSP predictions
                        html.H3(
                            "GSPGroup level Predictions",
                            style={
                                "fontFamily": "Roboto, sans-serif",
                                "color": "#333333",
                                "marginBottom": "10px",
                                "textAlign": "center",
                            },
                        ),
                        dash.dash_table.DataTable(
                            id="gsp-table",
                            columns=[
                                {"name": "GSP Group id", "id": "GSPGroup"},
                                {"name": "GSP Group name", "id": "name"},
                                {"name": "Predicted No of EVs", "id": "pred_sum"},
                                {"name": "Total Area in km2", "id": "area_km2", "type": "numeric", "format": Format(precision=0, scheme=Scheme.fixed)},
                            ],
                            data=GSPgroup_list,
                            style_table={"height": "calc(100vh - 100px)", "overflowY": "auto"},
                            style_cell={
                                "fontFamily": "Roboto, sans-serif",
                                "padding": "5px",
                            },
                            style_header={
                                "fontWeight": "bold",
                                "backgroundColor": "#f9f9f9",
                                "color": "#333333",
                            },
                            sort_action="native",  # Enables native column sorting
                            filter_action="native",  # Enables filtering by column
                            row_selectable="single",  # Allows selection of a single row
                            selected_rows=[],  # Default selected rows
                        ),
                    ],
                    style={
                        "flex": "2",
                        "padding": "20px",
                        "backgroundColor": "#f9f9f9",
                        "height": "100vh",
                        "overflow": "hidden",
                    },
                ),
                # Map section on the right, vertically aligned
                html.Div(
                    [
                        dcc.Graph(id="map", figure=fig, style={
                        "flex": "3",
                        "backgroundColor": "#ffffff",
                        "height": "calc(100vh - 20px)",  # Adjust for top padding/margin
                        "width": "50vw",    # Narrower width for a vertical look
                        "display": "flex",
                        "flexDirection": "column",  # Ensure proper stacking
                        "boxShadow": "0 0 10px rgba(0, 0, 0, 0.1)",  # Optional aesthetic
                    },),
                    ],
                ),
            ],
            style={
                "display": "flex",
                "flexDirection": "row",
                "flexGrow": "1",  # Ensure main content grows to fill remaining height
                "height": "100%",
            },
        ),
    ],
    style={
        "backgroundColor": "#ffffff",
        "display": "flex",
        "flexDirection": "column",
        "height": "100vh",  # Full viewport height
    },
)

@app.callback(
    Output("map", "figure"),
    Input("gsp-table", "selected_rows")
)
def update_map(selected_rows):
    if selected_rows:
        selected_gsp_groups = [GSPgroup_list[selected_row]["GSPGroup"] for selected_row in selected_rows]  # Get the first selected row's data
        filtered_df = gsp_level_predictions[gsp_level_predictions["GSPGroup"].isin(selected_gsp_groups)]  # Filter data based on selected GSP group
        central_location = central_location_gsp_group[selected_gsp_groups[0]]
        zoom_level = 6

    else:
        filtered_df = gsp_level_predictions  # Show all data if no row is selected
        central_location = {"lat": 55.0, "lon": -2.4}
        zoom_level = 4.5
    
    fig = px.choropleth_mapbox(
        filtered_df,
        geojson=geojson_data,
        locations="GSPs",
        featureidkey="properties.GSPs",
        color="log_pred_normalized",
        mapbox_style="carto-positron",
        hover_data={"GSPs": True, "Predicted No Of EVs": True, "log_pred_normalized": False},  # Show additional data on hover
        zoom=zoom_level,
        center=central_location,
    )
    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r": 10, "t": 0, "l": 0, "b": 0},
        coloraxis_colorbar=dict(
        title="",
        tickvals=[filtered_df["log_pred_normalized"].min(),
                  filtered_df["log_pred_normalized"].max()],
        tickmode="array",
        ticktext=["Fewer EVs", "More EVs"],  # Custom labels
        len=0.7,  # Adjust length of the colorbar (optional aesthetic)
    )
    )
    return fig
# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
