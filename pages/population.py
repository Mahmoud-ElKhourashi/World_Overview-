import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
from dash_extensions.enrich import Output, Input, html, dcc, callback, State,dash
import dash_iconify as di


dash.register_page(__name__, path='/population', order=1)

# Load data
def get_data():
    return pd.read_excel(r"D:\World_Data_Project\data.xlsx", sheet_name='population')

df = get_data()
total_population = df.groupby('Year')['Population'].sum().reset_index()
sorted_years = sorted(df['Year'].unique())


# Layout
layout = html.Div(
    style={'height': '100vh', 'display': 'flex', 'flexDirection': 'column'},
    children=[
        html.H1("Population Chart", className="text-center mt-2"),
        html.Hr(),
        html.Img(
            src="/assets/people.png",
            style={
                "height": "150px",
                "width": "150px",
                "position": "absolute",
                "top": "150px",  
                "right": "70px", 
                "zIndex": 1000, 
            }
        ),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='country',
                    value=['Worldwide'],
                    options=[{'label': 'Worldwide', 'value': 'Worldwide'}] +
                    [{'label': country, 'value': country} for country in df['Country Name'].unique()],
                    multi=True),
            ],
                width=6
            ),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label("Chart Type"),
                dbc.RadioItems(
                    options=["Line", "Bar", "Pie"],
                    value='Line',
                    id="chart", inline=True
                ),
                dbc.Button('Go to Home Page', href='/', color="primary", className="mt-3 mb-3"),
            ],
                width=2
            ),
            dbc.Col([
                dbc.Label("Year Filter"),
                dbc.Checklist(id="Year",
                              options=[{"label": x, "value": x} for x in sorted_years],
                              value=sorted_years, inline=True),
            ],
                width=4
            ),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Loading(
                    [dbc.Card(
                        [dcc.Graph(id='population-chart', figure={},
                                   style={'height': '60vh'})
                         ],
                        style={
                            'className': 'mt-3',
                            'borderRadius': '15px',  # Rounded corners
                            'backgroundColor': '#f8f9fa',  # Light gray background
                            'padding': '10px',  # Add padding inside the card
                            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'  # Add a subtle shadow
                        }
                    )
                    ]
                ),
            ],
                width=12
            )
        ])
    ],
    className="p-4")
plot_color_pallete = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

# Callback
@callback(
    Output('population-chart', 'figure'),
    Input('country', 'value'),
    Input('chart', 'value'),
    Input('Year', 'value'),
    prevent_initial_call=False
)
def update_population_chart(selected_country, chart_type, year):
    if 'Worldwide' in selected_country:
        df_filtered = total_population[total_population['Year'].isin(year)]
    else:
        df_filtered = df[df['Country Name'].isin(selected_country) & df['Year'].isin(year)]

    if chart_type == 'Line':
        if 'Worldwide' in selected_country:
            fig = px.line(
                df_filtered,
                x='Year',
                y='Population',
                title='Population Over Time Worldwide',
                markers=True,
                text='Population'
            )
        else:
            fig = px.line(
                df_filtered,
                x='Year',
                y='Population',
                title=f'Population Over Time by {selected_country}',
                color='Country Name',
                markers=True,
                text='Population'
            )
        fig.update_xaxes(
            tickmode='linear',
            dtick=1,
            tickformat='d',
            title='Year'
        ),
        fig.update_traces(
            texttemplate='%{text:.2s}',  # Format numbers in a compact way (e.g., 1.2M, 3.4B)
            textposition="top center",  
            textfont=dict(size=12, color="black") 
        )
    elif chart_type == 'Bar':
        if 'Worldwide' in selected_country:
            fig = px.bar(
                df_filtered,
                x='Year',
                y='Population',
                title='Population Over Time Worldwide',
                text_auto=True,
                template='plotly_white'
            )
        else:
            fig = px.bar(
                df_filtered,
                x='Year',
                y='Population',
                title=f'Population Over Time by {selected_country}',
                color='Country Name',
                text_auto=True,
            )
    elif chart_type == 'Pie':
        if 'Worldwide' in selected_country:
            fig = px.pie(
                df,
                values='Population',
                names='Country Name',
                title='Population Distribution Worldwide',
            )
        else:
            fig = px.pie(
                df_filtered,
                values='Population',
                names='Country Name',
                title=f'Population Distribution by {selected_country}',
            )
    fig.update_layout(
    plot_bgcolor='rgba(240, 240, 240, 1)',  # Light gray background for the plot area
    paper_bgcolor='rgba(255, 255, 255, 1)',  # White background for the entire figure
    margin=dict(l=20, r=20, t=50, b=20),  # Adjust margins
    title={
        'text': f"Population Over Time by {', '.join(selected_country)}",
        'y': 0.97,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 24, 'color': 'black'}
    },
    font=dict(size=14, color="black"),
    xaxis=dict(
        title="Year",
        title_font=dict(size=16, color="black"),
        tickfont=dict(size=14, color="black"),
        gridcolor='rgba(200, 200, 200, 0.5)',  # Light gray grid lines
        linecolor='black',  # Axis line color
        mirror=True  # Show axis lines on all sides
    ),
    yaxis=dict(
        title="Population",
        title_font=dict(size=16, color="black"),
        tickfont=dict(size=14, color="black"),
        gridcolor='rgba(200, 200, 200, 0.5)',  # Light gray grid lines
        linecolor='black',  # Axis line color
        mirror=True  # Show axis lines on all sides
    )
)
    return fig