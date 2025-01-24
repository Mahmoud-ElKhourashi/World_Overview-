from dash import html, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path="/")

# Home page layout
layout = dbc.Container(
    [
        # Welcome Section
        dbc.Row(
            dbc.Col(
                [
                    html.H1("Welcome to the Dashboard", className="text-center mt-4 mb-4"),
                    html.P("This is the home page.", className="text-center mb-4"),
                ],
                width=12,
            ),
            className="mb-5"
        ),

        # Population Overview Section
        dbc.Row(
            dbc.Col(
                [
                    html.H2("Population Overview"),
                    dbc.Button("Population Chart",href='/population', color="primary", className="me-2"),
                ],
                width=12,
            ),
            className="mb-5"
         ),
        # Economy Overview Section
        dbc.Row(
            dbc.Col(
                [
                    html.H2("Economy Overview", className="mb-3"),
                    dbc.Button("Go to GDP Page", href="/gdp", color="primary", className="me-2"),
                ],
                width=12,
            ),
            className="mb-5"
        ),

        # Trade Overview Section
        dbc.Row(
            dbc.Col(
                [
                    html.H2("Trade Overview", className="mb-3"),
                    dbc.Button("Go to Trade Page", href="/trade", color="primary", className="me-2"),
                ],
                width=12,
            ),
            className="mb-5"
        ),
    ],
    fluid=True,
    className="p-4"
)