from dash import html, dcc
import dash_bootstrap_components as dbc

# Home page layout
layout = html.Div([
    html.H1("Welcome to the Dashboard"),  # Title
    html.P("This is the home page."), # Description
    dbc.Button('Go to population chart', href='/population'), # Nav to population page
    html.Hr(),
    dbc.Button('Go to gdp Page', href='/gdp')  # Nav to gdp page
])