import pandas as pd 
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px


def get_data():
    df = pd.read_excel(r"D:\World_Data_Project\data.xlsx", sheet_name='gdp')
    return df

df = get_data()

total_GDP = df.groupby('Year')['GDP'].sum().reset_index()
fig_GDP=px.line(total_GDP,x='Year',y='GDP')
fig_GDP.update_xaxes(
    tickmode='linear',
    dtick=1,
    tickformat='d',  # Display ticks as integers
    showgrid=True,  # Show gridlines
    title='Year' # Add a title to the x-axis
    )
 
# layout 
gdp_layout = html.Div([
    html.H1("GDP Chart"),  # Title   
    html.P("This is the GDP page."), # Description
    html.Hr(),
    dcc.Dropdown(id='country-selector',value=['Worldwide'],options=[{'label':'Worldwide','value':'Worldwide'}]+
                 [{'label':country,'value':country} for country in df['Country Name'].unique()],
                 multi=True), # Country selector
    dcc.Graph(id='GDP-chart',figure=fig_GDP), # GDP chart
    html.Div(id='GDP-table'), # GDP tabl
    dbc.Button('Go to home page', href='/') # Nav to home pagex
])



def callback_GDP(app):

    @app.callback(
        Output('GDP-chart','figure'),
        Input('country-selector','value'),
        prevent_initial_call=True)
    
    def update_GDP_chart(selected_country):
        if 'Worldwide' in selected_country:
            fig_GDP = px.line(
                total_GDP,  # DataFrame
                x='Year',  # X-axis: Year
                y= 'GDP'  ,  # Y-axis: GDP
                title='GDP Over Time Worldwide' ,  # Chart title
            )
        else :     
            df_filterd = df[df['Country Name'].isin(selected_country)]
            fig_GDP = px.line(
                df_filterd,  # DataFrame
                x='Year',  # X-axis: Year
                y= 'GDP'  ,  # Y-axis: GDP
                title=f'GDP Over Time by {selected_country}' ,  # Chart title
                color='Country Name'
            )
            fig_GDP.update_xaxes(
                tickmode='linear',
                dtick=1,
                tickformat='d',  # Display ticks as integers
                showgrid=True,  # Show gridlines
                title='Year' # Add a title to the x-axis
                )
        return fig_GDP