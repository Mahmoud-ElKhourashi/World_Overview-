import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
from dash_extensions.enrich import DashProxy, Output, Input, html, dash, dcc, callback, Dash

dash.register_page(__name__, path='/population', order=1)

# Load data
def get_data():
    return pd.read_excel(r"D:\World_Data_Project\data.xlsx", sheet_name='population')

df = get_data()
total_population = df.groupby('Year')['Population'].sum().reset_index()
fig_population = px.line(total_population, x='Year', y='Population')
fig_population.update_xaxes(
    tickmode='linear',
    dtick=1,
    tickformat='d',
    title='Year'
)

# Layout
layout = html.Div(
    [
        html.H1("Population Chart", className="text-center mt-4"),
        html.P("This is the population page.", className="text-center"),
        html.Hr(),
        dcc.Dropdown(
            id='country-selector',
            value=['Worldwide'],
            options=[{'label': 'Worldwide', 'value': 'Worldwide'}] +
                    [{'label': country, 'value': country} for country in df['Country Name'].unique()],
            multi=True
        ),
        dcc.Graph(id='population-chart', figure=fig_population),
        html.Div(id='population-table'),
        dbc.Button('Go to Home Page', href='/', color="primary", className="mt-3")
    ],
    className="p-4"
)

# Callback
@callback(
    Output('population-chart', 'figure'),
    Input('country-selector', 'value'),
    prevent_initial_call=True
)
def update_population_chart(selected_country):
    if 'Worldwide' in selected_country:
        fig_population = px.line(
            total_population,
            x='Year',
            y='Population',
            title='Population Over Time Worldwide',
        )
    else:
        df_filtered = df[df['Country Name'].isin(selected_country)]
        fig_population = px.line(
            df_filtered,
            x='Year',
            y='Population',
            title=f'Population Over Time by {selected_country}',
            color='Country Name'
        )
        fig_population.update_xaxes(
            tickmode='linear',
            dtick=1,
            tickformat='d',
            title='Year'
        )
    return fig_population