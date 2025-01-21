import pandas as pd 
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px

def get_data():
    df = pd.read_excel(r"D:\World_Data_Project\data.xlsx", sheet_name='population')
    return df
df = get_data() 

total_population = df.groupby('Year')['Population'].sum().reset_index()
fig_population = px.line(total_population, x='Year', y='Population')
fig_population.update_xaxes(
    tickmode='linear',
    dtick=1,
    tickformat='d',  # Display ticks as integers
    title='Year'  # Add a title to the x-axis
)


# layout 
population_layout = html.Div([
    html.H1("Population Chart"),  # Title   
    html.P("This is the population page."), # Description
    html.Hr(),
    dcc.Dropdown(
        id='country-selector',
        value=['Worldwide'],
        options=[{'label': 'Worldwide', 'value': 'Worldwide'}] +
          [{'label': country, 'value': country} for country in df['Country Name'].unique()],
        multi=True
    ),  # Country selector
    dcc.Graph(id='population-chart', figure=fig_population),  # Population chart
    html.Div(id='population-table'), # Population tabl
    dbc.Button('Go to home page', href='/') # Nav to home page
])



def callback_population(app):

    @app.callback(
        Output('population-chart','figure'),
        Input('country-selector','value'),
        prevent_initial_call=True)
    
    def update_population_chart(selected_country):
        if 'Worldwide' in selected_country:
            fig_population = px.line(
                total_population,  # DataFrame
                x='Year',  # X-axis: Year
                y= 'Population'  ,  # Y-axis: Population
                title='Population Over Time Worldwide' ,  # Chart title
            )
        else :     
            df_filterd = df[df['Country Name'].isin(selected_country)]
            fig_population = px.line(
                df_filterd,  # DataFrame
                x='Year',  # X-axis: Year
                y= 'Population'  ,  # Y-axis: Population
                title=f'Population Over Time by {selected_country}' ,  # Chart title
                color='Country Name'
            )
            fig_population.update_xaxes(
                tickmode='linear',
                dtick=1,
                tickformat='d',  # Display ticks as integers
                showgrid=True,  # Show gridlines
                title='Year' # Add a title to the x-axis
                )
        return fig_population
        