import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, callback, Input, Output, State
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# import dash_core_components as dcc

dash.register_page(__name__)

df = pd.read_csv('files/symptoms_data.csv')


def input_form():
    row1 = html.Tr([html.Td(dbc.Label("What age group do you belong?"), className='col-4'),
                    html.Td(dbc.RadioItems(
                        options=[
                            {"label": "0 - 21", "value": 0},
                            {"label": "21 - 40", "value": 1},
                            {"label": "41 - 60", "value": 2},
                            {"label": "60+", "value": 3},
                        ],
                        id="age_radioitems",
                        inline=True)
                    )
                    ])

    table_header = [
        html.Thead(html.Tr([html.Th("Symptoms"), html.Th("Degree of Severity")]))
    ]
    row2 = html.Tr([html.Td(dbc.Label("Fever"), className='col-4'),
                    dbc.RadioItems(
                        options=[
                            {"label": "No", "value": 0},
                            {"label": "Mild", "value": 1},
                            {"label": "Moderate", "value": 2},
                            {"label": "High", "value": 3},
                        ],
                        id="fever_radioitems",
                        inline=True,
                    )
                    ])

    row3 = html.Tr([html.Td(dbc.Label("Fatigue")),
                    dbc.RadioItems(
                        options=[
                            {"label": "No", "value": 0},
                            {"label": "Yes", "value": 1},
                        ],
                        id="fatigue_radioitems",
                        inline=True,
                    )
                    ])

    row4 = html.Tr([html.Td(dbc.Label("Cough")),
                    dbc.RadioItems(
                        options=[
                            {"label": "No", "value": 0},
                            {"label": "Yes", "value": 1},
                        ],
                        id="cough_radioitems",
                        inline=True,
                    )
                    ])

    row5 = html.Tr([html.Td(dbc.Label("Body Ache")),
                    dbc.RadioItems(
                        options=[
                            {"label": "No", "value": 0},
                            {"label": "Yes", "value": 1},
                        ],
                        id="body_ache_radioitems",
                        inline=True,
                    )
                    ])

    row6 = html.Tr([html.Td(dbc.Label("Sore Throat"), className='col-4'),
                    dbc.RadioItems(
                        options=[
                            {"label": "No", "value": 0},
                            {"label": "Low", "value": 1},
                            {"label": "High", "value": 2},
                        ],
                        id="sore_throat_radioitems",
                        inline=True,
                    )
                    ])

    row7 = html.Tr([html.Td(dbc.Label("Breathing Difficulties"), className='col-4'),
                    dbc.RadioItems(
                        options=[
                            {"label": "No", "value": 0},
                            {"label": "Low", "value": 1},
                            {"label": "High", "value": 2},
                        ],
                        id="breathing_radioitems",
                        inline=True,
                    )
                    ])

    button_row = dbc.Row(
        [
            dbc.Col(
                dbc.Button(
                    'Submit',
                    id='submit_button',
                    type='submit',
                    color="danger",
                    className='btn rounded-pill mt-2 '
                ), className="me-3 text-end"
            ),
            dbc.Col(
                dbc.Button(
                    'Reset',
                    id = 'reset_button',
                    type='reset',
                    outline=True, color="warning",
                    className='btn rounded-pill mt-2'
                ), className="me-3 text-start"
            )
        ],
        className="mx-auto mb-3")

    table1 = dbc.Table([html.Tbody([row1])], bordered=False, className="table table-borderless")
    table_body = [html.Tbody([row2, row3, row4, row5, row6, row7])]
    table2 = dbc.Table(table_header + table_body, bordered=False, className="table table-borderless")

    form_input = dbc.Form([table1, table2, button_row])

    return form_input


def create_assessment_form():
    assessment_form = html.Div([
        html.H3(
            'Symptoms based assessment for COVID-19',
            className="text-center mt-3"
        ),
        dbc.Container([
            dbc.Row(
                dbc.Col(
                    html.Div(input_form(),
                             style={'border': '1px solid black'}
                             ),
                    width=8,
                ), justify="center", className='mb-5'),

            dbc.Row(
                dbc.Col(
                    html.Div("Output Div",
                             style={'border': '1px solid black'}
                             , id='output_div'),
                    width=8,
                ), justify="center", className='mt-5')
        ],
            fluid=True,
            className="mt-4"),

    ])
    return assessment_form


layout = html.Div(children=[
    create_assessment_form(),
])


def get_model_data(age, fever, fatigue, cough, body_ache, sore_throat, breathing_difficulties):
    X_resampled = df.iloc[:, :7]
    y_resampled = df.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.3, random_state=42)

    # Fitting the logistic regression model
    log_reg = LogisticRegression(max_iter=1000)
    log_reg.fit(X_train, y_train)

    # Creating a Random Forest classifier with 100 trees
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    # Fitting the model on the training data
    rf.fit(X_train, y_train)

    # Creating a Gradient Boosting Classifier
    gb_model = GradientBoostingClassifier()

    # Training the model
    gb_model.fit(X_train, y_train)

    # create a new DataFrame with the input values
    input_data = pd.DataFrame([[age, fever, fatigue, cough, body_ache, sore_throat, breathing_difficulties]],
                              columns=df.columns[:-1])

    # use the trained model to predict the probability of infection
    predicted_probabilities = log_reg.predict_proba(input_data)
    predicted_probabilities = predicted_probabilities[0][1]

    predicted_probabilities_random_forest = rf.predict_proba(input_data)[:, 1]


    predicted_probabilities_gradient_boost = gb_model.predict_proba(input_data)[:, 1]

    print('The predicted probability of being infected is (predicted_probabilities): %.2f%%' % (
            predicted_probabilities * 100))
    print('The predicted probability of being infected is(predicted_probabilities_random_forest): %.2f%%' % (
            predicted_probabilities_random_forest * 100))
    print('The predicted probability of being infected is(predicted_probabilities_gradient_boost): %.2f%%' % (
            predicted_probabilities_gradient_boost * 100))

    p_value = (
                      predicted_probabilities + predicted_probabilities_random_forest + predicted_probabilities_gradient_boost) / 3
    print(p_value)

    return p_value


def get_guidelines(infection_rate):
    if 0 <= infection_rate <= 20:
        return html.Div([
            html.H4("Infection Rate: 0-20% (Low Infection Rate)"),
            html.Ul([
                html.Li("Community transmission is relatively low."),
                html.Li("Maintain basic preventive measures such as:"),
                html.Ul([
                    html.Li("Follow local health guidelines and regulations."),
                    html.Li("Wash hands frequently with soap and water for at least 20 seconds."),
                    html.Li("Maintain physical distance of at least 1 meter (3 feet) from others."),
                    html.Li("Wear a mask in crowded or public settings."),
                    html.Li("Avoid large gatherings and non-essential travel."),
                ]),
                html.Li("Stay informed about the latest updates from reliable sources."),
                html.Li("Encourage vaccination efforts and public health awareness.")
            ])
        ])
    elif 20 < infection_rate <= 40:
        return html.Div([
            html.H4("Infection Rate: 20-40% (Moderate Infection Rate)"),
            html.Ul([
                html.Li(
                    "Limit contact with individuals outside your household, especially those at higher risk, such as the elderly or those with underlying health conditions."),
                html.Li("Avoid non-essential indoor gatherings or crowded places."),
                html.Li("Opt for outdoor activities where it is easier to maintain physical distance."),
            ])
        ])
    elif 40 < infection_rate <= 60:
        return html.Div([
            html.H4("Infection Rate: 40-60% (Substantial Infection Rate)"),
            html.Ul([
                html.Li("Minimize contact with individuals outside your household, especially in enclosed spaces."),
                html.Li("Consider remote work or online learning if feasible."),
                html.Li("Avoid unnecessary travel, especially to high-risk areas."),
                html.Li("Continue practicing good hand hygiene and wearing a mask in public settings.")
            ])
        ])
    elif 60 < infection_rate <= 80:
        return html.Div([
            html.H4("Infection Rate: 60-80% (High Infection Rate)"),
            html.Ul([
                html.Li("Limit social interactions to essential activities only."),
                html.Li("Work from home if possible and follow local guidelines regarding workplace safety."),
                html.Li("Avoid crowded areas and gatherings entirely."),
                html.Li("Consider using delivery services for essential items."),
                html.Li("Stay updated with local health advisories and be prepared for potential lockdown measures.")
            ])
        ])
    elif 80 < infection_rate <= 100:
        return html.Div([
            html.H4("Infection Rate: 80-100% (Critical Infection Rate)"),
            html.Ul([
                html.Li("Strictly adhere to local health guidelines and restrictions."),
                html.Li("Stay home as much as possible and limit contact with individuals outside your household."),
                html.Li("Avoid all non-essential activities and travel."),
                html.Li(
                    "Practice good hygiene, including frequent handwashing and disinfecting commonly touched surfaces."),
                html.Li("Seek medical attention if you develop symptoms or have been exposed to someone with COVID-19.")
            ])
        ])

    else:
        return html.Div("No guidelines available for the given infection rate.")


# @callback(
#     Output("output_div", "children"),
#     [Input("submit_button", "n_clicks")],
#     [State("age_radioitems", "value"),
#      State("fever_radioitems", "value"),
#      State("fatigue_radioitems", "value"),
#      State("cough_radioitems", "value"),
#      State("body_ache_radioitems", "value"),
#      State("sore_throat_radioitems", "value"),
#      State("breathing_radioitems", "value")]
# )
# def get_selected_values(n_clicks, age, fever, fatigue, cough, body_ache, sore_throat, breathing_difficulties):
#     if n_clicks is not None and n_clicks > 0:
#         # Check if all fields are selected
#         if age is not None and fever is not None and fatigue is not None and cough is not None \
#                 and body_ache is not None and sore_throat is not None and breathing_difficulties is not None:
#             percentage = get_model_data(age, fever, fatigue, cough, body_ache, sore_throat, breathing_difficulties)
#             guidelines = get_guidelines(percentage * 100)
#             return html.Div([
#                 html.H4("Result:"),
#                 html.Div(
#                     'The predicted probability of being infected is: %.2f%%' % (percentage * 100),
#                     className="mt-3"
#                 ),
#                 html.H4("COVID-19 Guidelines:"),
#                 html.Div(
#                     guidelines,
#                     className="mt-3"
#                 ),
#                 html.H4("Reference Websites:"),
#                 html.Div([
#                     html.P(
#                         ["COVID-19 Guidelines: ", html.A("WHO COVID-19 Advice for the Public",
#                                                          href="https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public")],
#                         className="mt-3"
#                     ),
#                     html.P(
#                         ["Vaccine Guidelines: ", html.A("WHO COVID-19 Vaccines",
#                                                         href="https://www.who.int/emergencies/diseases/novel-coronavirus-2019/covid-19-vaccines")],
#                         className="mt-3"
#                     )
#                 ])
#             ])
#         else:
#             return html.Div("Please select values for all fields.")
#     else:
#         return None

@callback(
    Output("output_div", "children"),
    [Input("submit_button", "n_clicks"),
     Input("reset_button", "n_clicks")],
    [State("age_radioitems", "value"),
     State("fever_radioitems", "value"),
     State("fatigue_radioitems", "value"),
     State("cough_radioitems", "value"),
     State("body_ache_radioitems", "value"),
     State("sore_throat_radioitems", "value"),
     State("breathing_radioitems", "value")]
)
def handle_button_click(submit_clicks, reset_clicks, age, fever, fatigue, cough, body_ache, sore_throat, breathing_difficulties):
    ctx = dash.callback_context

    if not ctx.triggered:
        # No click event yet
        return None
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "submit_button":
            # Submit button clicked
            if age is not None and fever is not None and fatigue is not None and cough is not None \
                    and body_ache is not None and sore_throat is not None and breathing_difficulties is not None:
                percentage = get_model_data(age, fever, fatigue, cough, body_ache, sore_throat, breathing_difficulties)
                guidelines = get_guidelines(percentage * 100)
                return html.Div([
                    html.H4("Result:"),
                    html.Div(
                        'The predicted probability of being infected is: %.2f%%' % (percentage * 100),
                        className="mt-3"
                    ),
                    html.H4("COVID-19 Guidelines:"),
                    html.Div(
                        guidelines,
                        className="mt-3"
                    ),
                    html.H4("Reference Websites:"),
                    html.Div([
                        html.P(
                            ["COVID-19 Guidelines: ", html.A("WHO COVID-19 Advice for the Public",
                                                             href="https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public")],
                            className="mt-3"
                        ),
                        html.P(
                            ["Vaccine Guidelines: ", html.A("WHO COVID-19 Vaccines",
                                                            href="https://www.who.int/emergencies/diseases/novel-coronavirus-2019/covid-19-vaccines")],
                            className="mt-3"
                        )
                    ])
                ])
            else:
                return html.Div("Please select values for all fields.")

        elif button_id == "reset_button":
            # Reset button clicked
            return None

        else:
            return None


