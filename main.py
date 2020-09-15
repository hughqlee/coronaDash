import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from data import country_totals, dropdown_options, make_global_df, make_country_df
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
        html.Div(children=[dcc.Graph(figure=world_map)], style={"width": "80%"}),
        html.Div(
            children=[html.Div(children=[make_table(country_totals)])],
            style={"margin": "5% 10%"},
        ),
        html.Div(
            children=[
                dcc.Dropdown(
                    placeholder="Select a country",
                    id="country",
                    options=[
                        {"label": country, "value": country}
                        for country in dropdown_options
                    ],
                    style={"color": "#111111", "margin": "0 auto", "width": 320},
                ),
                dcc.Graph(id="output-graph"),
            ],
            style={"width": "80%"},
        ),
    ],
)


@app.callback(Output("output-graph", "figure"), [Input("country", "value")])
def interactive_graph(value):
    if value:
        df = make_country_df(value)
    else:
        df = make_global_df()
    fig = px.line(
        df,
        x="date",
        y=["confirmed", "deaths", "recovered"],
        template="plotly_dark",
        labels={"value": "Cases", "variable": "Condition", "date": "Date"},
        hover_data={"value": ":,", "variable": False},
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)