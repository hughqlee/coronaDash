import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from data import country_totals
from builders import make_table

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap",
]

app = dash.Dash(__name__, external_stylesheets=stylesheets)

world_map = px.scatter_geo(
    country_totals,
    locations="Country_Region",
    locationmode="country names",
    color="Confirmed",
    hover_name="Country_Region",
    hover_data={
        "Confirmed": ":,2f",
        "Deaths": ":,2f",
        "Recovered": ":,2f",
        "Country_Region": False,
    },
    size="Confirmed",
    color_continuous_scale=px.colors.sequential.Blues,
    size_max=40,
    template="plotly_dark",
)

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "backgroundColor": "#111111",
        "color": "white",
        "fontFamily": "Open Sans, sans-serif",
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
    },
    children=[
        html.Header(
            style={"textAlign": "center", "paddingTop": "50px"},
            children=[html.H1("Corona Dashboard", style={"fontSize": 40})],
        ),
        html.Div(
            children=[dcc.Graph(figure=world_map)],
        ),
        html.Div(
            children=[html.Div(children=[make_table(country_totals)])],
        ),
    ],
)


if __name__ == "__main__":
    app.run_server(debug=True)