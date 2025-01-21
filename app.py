from dash_extensions.enrich import DashProxy, Output, Input, html,Dash,dcc,callback
from pages.home import layout as home_layout
from pages.population import population_layout,callback_population
from pages.gdp import gdp_layout, callback_GDP
import dash_bootstrap_components as dbc
    

# Initialize the Dash app
app = DashProxy(external_stylesheets=[dbc.themes.CYBORG], suppress_callback_exceptions=True)

# Main app layout with URL routing
app.layout = dbc.Container([
    dcc.Location(id='url', refresh=True),
    dbc.Container(id='page-content')
])

# Callback to switch between pages
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/population':
        return population_layout
    elif pathname == '/gdp':
        return gdp_layout
    else:
        return home_layout

# Register callbacks for the bar chart page
callback_population(app)
callback_GDP(app)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)