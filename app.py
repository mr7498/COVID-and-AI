import dash
import dash_bootstrap_components as dbc
from dash import Dash, html




app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.BOOTSTRAP], suppress_callback_exceptions=True)

app.layout = html.Div([
    html.Nav([
        html.H1(
            'COVID-19 AI based Expert System',
            className='navbar-text mx-auto'
        ),
        html.A(
            html.Img(src='assets/logo.png', height='60'),
            className='navbar-brand',
            href='/'
        )
    ],
    className='navbar navbar-expand-lg navbar-light bg-light'),

	 dash.page_container

])

if __name__ == '__main__':
	app.run_server(debug=True)