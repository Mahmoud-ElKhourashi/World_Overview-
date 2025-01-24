import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
from dash_extensions.enrich import DashProxy, Output, Input, html, dash, dcc, callback, Dash

dash.register_page(__name__, path='/trade', order=2)

# Load data
def get_data():
    return pd.read_excel(r"D:\World_Data_Project\data.xlsx", sheet_name='trade')

df = get_data()
total_Trade = df.groupby('Year')['Trade'].sum().reset_index()
fig_Trade = px.line(total_Trade, x='Year', y='Trade')
fig_Trade.update_xaxes(
    tickmode='linear',
    dtick=1,
    tickformat='d',
    title='Year'
)

# Layout
layout = html.Div(
    [
        html.H1("Trade Chart", className="text-center mt-4"),
        html.P("This is the Trade page.", className="text-center"),
        html.Hr(),
        dcc.Dropdown(
            id='country-selector',
            value=['Worldwide'],
            options=[{'label': 'Worldwide', 'value': 'Worldwide'}] +
                    [{'label': country, 'value': country} for country in df['Country Name'].unique()],
            multi=True
        ),
        dcc.Graph(id='Trade-chart', figure=fig_Trade),
        html.Div(id='Trade-table'),
        dbc.Button('Go to Home Page', href='/', color="primary", className="mt-3")
    ],
    className="p-4"
)

# Callback
@callback(
    Output('Trade-chart', 'figure'),
    Input('country-selector', 'value'),
    prevent_initial_call=True
)
def update_Trade_chart(selected_country):
    if 'Worldwide' in selected_country:
        fig_Trade = px.line(
            total_Trade,
            x='Year',
            y='Trade',
            title='Trade Over Time Worldwide',
        )
    else:
        df_filtered = df[df['Country Name'].isin(selected_country)]
        fig_Trade = px.line(
            df_filtered,
            x='Year',
            y='Trade',
            title=f'Trade Over Time by {selected_country}',
            color='Country Name'
        )
        fig_Trade.update_xaxes(
            tickmode='linear',
            dtick=1,
            tickformat='d',
            title='Year'
        )
    return fig_Trade