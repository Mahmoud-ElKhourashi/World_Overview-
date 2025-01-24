from dash_extensions.enrich import DashProxy, html, dash, dcc
import dash_bootstrap_components as dbc
from dash import Input, Output

# Initialize the Dash app
worldapp = DashProxy(__name__, pages_folder='pages', use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Link pages
pages_link = [
    dcc.Link(page['name'], href=page['relative_path'], className='nav-link')
    for page in dash.page_registry.values()
    if page['module'] != 'Error 404'
]

# Main app layout
worldapp.layout = dbc.Container(
    [
        dash.page_container  # Container for rendering the current page
    ],
    fluid=True,  # Full-width container
    className="p-4"  # Add padding
)

# Run the app
if __name__ == '__main__':
    worldapp.run(debug=True)