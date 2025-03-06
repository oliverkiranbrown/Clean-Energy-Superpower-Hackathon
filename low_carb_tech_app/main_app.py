import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from load_data import load_data
import json
# Sample data (replace with your actual data)
data = {
    "outcode": ["AB10", "AB11", "AB12", "AB13"],
    "latitude": [57.13514, 57.13811, 57.09801, 57.11579],
    "longitude": [-2.11731, -2.09381, -2.10981, -2.25178],
    "ev_count": [120, 80, 150, 60],
}

# Create DataFrame
df = load_data()

grouped_series = df.groupby("outcode")["pred"].sum()
coordinates_d = json.load(open("./data/outcode_coordinates.json"))
grouped_df = grouped_series.reset_index()
grouped_df["latitude"] = grouped_df["outcode"].map(lambda x: coordinates_d[x][0])
grouped_df["longitude"] = grouped_df["outcode"].map(lambda x: coordinates_d[x][1])
# Initialize Dash app
app = dash.Dash(__name__)
app.title = "UK EV Map"

# Layout
app.layout = html.Div(
    [
        # Title at the top
        html.H1(
            "Electric Vehicles in the UK by Outcode",
            style={
                "font-family": "Roboto, sans-serif",
                "text-align": "center",
                "margin-bottom": "20px",
                "font-weight": "bold",
                "color": "#333333",  # Modern dark gray
            },
        ),
        # Main content with slider on the left and map on the right
        html.Div(
            [
                # Slider section on the left
                html.Div(
                    [
                        html.P(
                            "Filter by minimum EV count:",
                            style={
                                "font-family": "Roboto, sans-serif",
                                "color": "#555555",  # Subtle gray
                                "margin-bottom": "10px",
                            },
                        ),
                        dcc.Slider(
                            id="ev-slider",
                            min=grouped_df["pred"].min(),
                            max=grouped_df["pred"].max(),
                            step=1,
                            value=grouped_df["pred"].min(),
                            marks={
                                int(i): {"label": str(i), "style": {"color": "#777777"}}
                                for i in range(grouped_df["pred"].min(), grouped_df["pred"].max() + 1, 1)
                            },
                        ),
                    ],
                    style={
                        "flex": "3",
                        "padding": "20px",
                        "background-color": "#ffffff",
                        "height": "100vh",  # Full vertical height
                        "width": "33vw",    # Set a narrower width
                        "overflow": "hidden",  # Ensure no overflow
                    },
                ),
                # Map section on the right, vertically aligned
                html.Div(
                    [
                        dcc.Graph(id="map", style={
                        "flex": "3",
                        "background-color": "#ffffff",
                        "height": "calc(100vh - 20px)",  # Adjust for top padding/margin
                        "width": "50vw",    # Narrower width for a vertical look
                        "display": "flex",
                        "flex-direction": "column",  # Ensure proper stacking
                        "box-shadow": "0 0 10px rgba(0, 0, 0, 0.1)",  # Optional aesthetic
                    },),
                    ],
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "row",
                "flex-grow": "1",  # Ensure main content grows to fill remaining height
                "height": "100%",
            },
        ),
    ],
    style={
        "background-color": "#ffffff",
        "display": "flex",
        "flex-direction": "column",
        "height": "100vh",  # Full viewport height
    },
)
# Callback to update the map
@app.callback(
    Output("map", "figure"),
    Input("ev-slider", "value")
)
def update_map(min_ev_count):
    # Filter data based on slider value
    filtered_df = grouped_df[grouped_df["pred"] >= min_ev_count]

    # Create map figure
    fig = px.scatter_mapbox(
        filtered_df,
        lat="latitude",
        lon="longitude",
        size="pred",
        size_max=15,
        hover_name="outcode",
        hover_data={"latitude": False, "longitude": False, "pred": True},
        color_continuous_scale="Cividis",
        zoom=5,  # Adjusted zoom level for the entire UK
        center={"lat": 55.0, "lon": -2.4}
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )

    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
