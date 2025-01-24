import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
from dash_extensions.enrich import DashProxy, Output, Input, html, dash, dcc, callback, Dash

dash.register_page(__name__, path='/gdp', order=2)

# Load data
def get_data():
    return pd.read_excel(r"D:\World_Data_Project\data.xlsx", sheet_name='gdp')

df = get_data()
total_GDP = df.groupby('Year')['GDP'].sum().reset_index()
fig_GDP = px.line(total_GDP, x='Year', y='GDP')
fig_GDP.update_xaxes(
    tickmode='linear',
    dtick=1,
    tickformat='d',
    title='Year'
)

# Layout
layout = html.Div(
    [
        html.H1("GDP Chart", className="text-center mt-4"),
        html.P("This is the GDP page.", className="text-center"),
        html.Hr(),
        dcc.Dropdown(
            id='country-selector',
            value=['Worldwide'],
            options=[{'label': 'Worldwide', 'value': 'Worldwide'}] +
                    [{'label': country, 'value': country} for country in df['Country Name'].unique()],
            multi=True
        ),
        dcc.Graph(id='GDP-chart', figure=fig_GDP),
        html.Div(id='GDP-table'),
        dbc.Button('Go to Home Page', href='/', color="primary", className="mt-3")
    ],
    className="p-4"
)

# Callback
@callback(
    Output('GDP-chart', 'figure'),
    Input('country-selector', 'value'),
    prevent_initial_call=True
)
def update_GDP_chart(selected_country):
    if 'Worldwide' in selected_country:
        fig_GDP = px.line(
            total_GDP,
            x='Year',
            y='GDP',
            title='GDP Over Time Worldwide',
        )
    else:
        df_filtered = df[df['Country Name'].isin(selected_country)]
        fig_GDP = px.line(
            df_filtered,
            x='Year',
            y='GDP',
            title=f'GDP Over Time by {selected_country}',
            color='Country Name'
        )
        fig_GDP.update_xaxes(
            tickmode='linear',
            dtick=1,
            tickformat='d',
            title='Year'
        )
    return fig_GDP