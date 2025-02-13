import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State

dash.register_page(__name__, path='/')

def create_search_bar():
    search_box = dbc.Row(
            [
                dbc.Col(
                    dbc.Input(
                        type="text",
                        className="form-control rounded-pill mx-auto mt-5",
                        placeholder="Search",
                        style={'width': '50%'}
                    ),
                ),
            ],
            className="mx-auto")

    button_row = dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        'Submit',
                        type='submit',
                        color="danger",
                        className='btn rounded-pill mt-3 '
                    ), className="me-3 text-end"
                ),
                dbc.Col(
                    dbc.Button(
                        'Reset',
                        type='reset',
                        outline=True, color="warning",
                        className='btn rounded-pill mt-3'
                    ), className="me-3 text-start"
                )
            ],
        className="mx-auto")

    search_bar = dbc.Form([search_box, button_row])
    return search_bar

first_card = dbc.Card([
    dbc.CardBody(
        [
            html.H5("COVID-19 Dashboard", className="card-title"),
            html.P("Stay Informed and Up-to-Date with Our Comprehensive COVID-19 Dashboard"),

        ], style={'height': '150px'}
    ),
        dbc.CardFooter([
            dcc.Location(id='url', refresh=True),
            dbc.Button("Go", id="button_dashboard", color="danger")
            ]),

])

@callback(
    Output('url', 'pathname'),
    [Input('button_dashboard', 'n_clicks')],
    [State('url', 'pathname')],
)
def navigate_to_app(n_clicks, pathname):
    if n_clicks:
        return '/dashboard'
    return pathname

second_card = dbc.Card([
    dbc.CardBody(
        [
            html.H5("Self-Assessment Test", className="card-title"),
            html.P("Evaluate Your Risk of COVID-19 with Our AI-Powered Self Assessment Test"),

        ],  style={'height': '150px'}
    ), dbc.CardFooter([
                    dcc.Location(id='url', refresh=True),
                    dbc.Button("Go", id='button_assessment', color="danger")
    ])
])

@callback(
    Output('url', 'href'),
    [Input('button_assessment', 'n_clicks')],
    [State('url', 'href')],
)
def navigate_to_app(n_clicks, href):
    if n_clicks:
        return '/assessment'
    return href

cards = dbc.Row(
    [
        dbc.Col(first_card, width=3,style={'margin-left': '1.5rem', 'margin-right': '1.5rem'}),
        dbc.Col(second_card, width=3,style={'margin-left': '1.5rem', 'margin-right': '1.5rem'})
    ], className="mt-5 justify-content-center"
    )



layout = html.Div(children=[
    cards
])

