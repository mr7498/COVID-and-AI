import json

import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
import numpy as np
import pandas as pd
import plotly.express as px
from dash import html, dcc, callback, Input, Output, State, dash_table

import pages.layout_configs as lc
import pages.support_functions as sf

pd.options.mode.chained_assignment = None


dash.register_page(__name__)

# Use pandas to read the CSV file from the URL
reporting_data = 'files/COVID_case_report_final_V2.csv'

# Covid data Section
report_data = pd.read_csv(reporting_data, encoding='ISO-8859-1')
report_data = pd.read_csv(reporting_data)

# url = "https://raw.githubusercontent.com/robert-koch-institut/COVID-19-Impfungen_in_Deutschland/master/Aktuell_Deutschland_Landkreise_COVID-19-Impfungen.csv"
url = 'files/vaccine_data.csv'

vaccine_data = pd.read_csv(url)
vaccine_data['date'] = pd.to_datetime(vaccine_data['date']).dt.strftime('%d-%m-%Y')

df_region = pd.read_csv('files/covid-19-germany-landkreise.csv')

# use of support functions
# vaccine_data = sf.get_vaccinedata(df_vaccine, df_region)
# vaccine_data.to_csv('files/vaccine_data.csv', index = False)

# GeoJSON file
rheinland_states = json.load(open("files/covid-19-germany-landkreise1.geojson"))

# All filters e.g. Dropdown, Toggle, Date Range

# Create district options
district_options = [{'label': c, 'value': c} for c in report_data['district'].unique()]

# District dropdown
district_dropdown = dbc.Col(
    [
        html.P('Select District:', className='fix_label', style={'color': 'black'}),
        dcc.Dropdown(
            id='w_countries',
            multi=False,
            value=district_options[-1]['value'],
            placeholder='Select District',
            options=district_options
        )
    ],
    md=4,
    sm=12
)

# Toggle Switch for Covid and Vaccine
toggle_switch = dbc.Col(
    [
        html.Div(
            [
                html.Div("Covid", style={"display": "inline-block", "width": "33%"}),
                daq.ToggleSwitch(
                    id='toggle',
                    color='blue',
                    value=False,
                    style={"display": "inline-block", "width": "33%", 'color': 'blue'}
                ),
                html.Div("Vaccine", style={"display": "inline-block", "width": "33%"})
            ],
            style={"text-align": "center", "margin": "30px"}
        )
    ],
    md=2,
    sm=12
)

# Toggle Switch for Actual and Cumulative
toggle_switch_type = dbc.Col(
    [
        html.Div(
            [
                html.Div("Actual", style={"display": "inline-block", "width": "33%"}),
                daq.ToggleSwitch(
                    id='toggle1',
                    color='blue',
                    value=False,
                    style={"display": "inline-block", "width": "33%", 'color': 'blue'}
                ),
                html.Div("Cumulative", style={"display": "inline-block", "width": "33%"})
            ],
            style={"text-align": "center", "margin": "30px"}
        )
    ],
    md=2,
    sm=12
)

# Date Range Selector
date_picker_range = dbc.Col(
    [
        html.Div(
            [
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date='2021-08-01',
                    end_date='2023-02-02',
                    className="dash-bootstrap"
                )
            ],
            style={"margin": "25px"}
        )
    ],
    md=3,
    sm=12
)

# Row to contain the above components
DROPDOWN_MENU = dbc.Row(
    [
        district_dropdown,
        toggle_switch,
        date_picker_range,
        toggle_switch_type
    ],
    className="mt-3"
)


# HTML Section for KPI

info_bar = html.Div(
    id="summary",
)

# Reference Card which contains information about data
deacot_reference_card = (
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.Button("?", id="deacot_card_open"),
                    dbc.Modal(
                        [
                            dbc.ModalHeader("COVID-19 Report/Vaccination References"),
                            dbc.ModalBody(
                                [
                                    html.P(
                                        "Daily cases represents the trend of daily positive cases."
                                    ),
                                    html.P(
                                        "Hospitalized cases represents the growth of cases which hospitalized."
                                    ),
                                    html.P(
                                        "Deceased depicts number of deaths over time"
                                    ),
                                    html.P(
                                        "Current cases illustrates Number of active cases"
                                    ),
                                    html.P("Recovered cases represents number of people recovered"),
                                    html.P("total cases represents total number of positive cases over time"),
                                    html.P("Data retrieved from Rhineland-Palatinate Government Website:"),
                                    html.P("Note: This Chart is visualised based on rolling mean average of daily numbers."),
                                    html.P("Important information: Due to the delay in reporting between new cases becoming known and data transmission, there may sometimes be deviations from the figures currently published by the municipal health authorities, as well as time delays. The number of cases reported may need to be corrected due to incorrect entries and transmission errors in the software. We ask for your understanding."
                                    ),
                                    dbc.CardLink(
                                        "COVID Data (Rhineland-Palatinate)",
                                        href="https://lua.rlp.de/de/unsere-themen/infektionsschutz/meldedaten-coronavirus/",
                                        target='_blank',
                                    ),
                                ]
                            ),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Close",
                                    id="deacot_card_close",
                                    className="ml-auto",
                                )
                            ),
                        ],
                        id="deacot_card_modal",
                    ),
                ]
            ),
        ],
        style={"width": "5rem"},
    ),
)

deacot_reference_card2 = (
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.Button("?", id="deacot_card2_open"),
                    dbc.Modal(
                        [
                            dbc.ModalHeader("COVID-19 Incidences Chart Info"),
                            dbc.ModalBody(
                                [
                                    html.P(
                                        "Indcidence Chart is representation of Number of people reported last 7 days per 100,000 in administrative districts and urban districts (KS) with exact values"
                                    ),
                                    html.P("Green - Mild (Incidence Rate is less then or equal to 50)"),
                                    html.P("Yellow - Moderate (Incidence Rate is greater then 50 and less or equal to 100)"),
                                    html.P("Orange - Severe (Incidence Rate is greater then 100 and less or equal to 200)"),
                                    html.P("Red - Very Severe (Incidence Rate is greater then 200)"),


                                    html.P(
                                        "\n Note: The above figures correspond to the laboratory-confirmed cases of COVID-19 disease with a registration address in Rhineland-Palatinate transmitted in the reporting software of the Robert Koch Institute. These are sent to the Robert Koch Institute by the health authorities via the state registration office at the state examination office. Since the employees of the local health authorities are primarily responsible for identifying contact persons and quarantine measures at the weekend, the reports are sometimes delayed." ),
                                    html.P(
                                        "Important information: Due to the delay in reporting between new cases becoming known and data transmission, there may sometimes be deviations from the figures currently published by the municipal health authorities, as well as time delays. The number of cases reported may need to be corrected due to incorrect entries and transmission errors in the software. We ask for your understanding."
                                    ),


                                    dbc.CardLink(
                                        "COVID Data (Rhineland-Palatinate)",
                                        href="https://lua.rlp.de/de/unsere-themen/infektionsschutz/meldedaten-coronavirus/",
                                        target='_blank',
                                    ),
                                ]
                            ),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Close",
                                    id="deacot_card2_close",
                                    className="ml-auto",
                                )
                            ),
                        ],
                        id="deacot_card2_modal",
                    ),
                ]
            ),
        ],
        style={"width": "5rem"},
    ),
)
# Reference Card which contains information about data
deacot_reference_card_vaccine = (
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.Button("?", id="deacot_card_open"),
                    dbc.Modal(
                        [
                            dbc.ModalHeader("COVID-19 Vaccination References"),
                            dbc.ModalBody(
                                [
                                    html.P(
                                        "First vaccination: The initial dose of a vaccine given to an individual to provide immunity against a specific disease."
                                    ),
                                    html.P(
                                        "Second vaccination: A subsequent dose of a vaccine given to boost the immune response and ensure continued protection against the disease."
                                    ),
                                    html.P(
                                        "First Booster Dose: An additional dose of a vaccine given to provide a boost to the immune system and extend the protection provided by the previous doses."
                                    ),
                                    html.P(
                                        "Second booster vaccination: A subsequent dose of a vaccine given to further extend the protection provided by the previous doses and ensure long-term immunity against the disease."
                                    ),
                                    html.P("Note: This Chart is visualised based on rolling mean average of daily numbers."),

                                    dbc.CardLink(
                                        "Vaccine Data Source RKI",
                                        href="https://github.com/robert-koch-institut/COVID-19-Impfungen_in_Deutschland",
                                        target='_blank',
                                    ),
                                ]
                            ),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Close",
                                    id="deacot_card_close",
                                    className="ml-auto",
                                )
                            ),
                        ],
                        id="deacot_card_modal",
                    ),
                ]
            ),
        ],
        style={"width": "5rem"},
    ),
)


# Container for Line chart
line_graph = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="deacot_sent",
                style={"height": "70vh"},
                config=lc.tool_config,
            ),
            md=11,
        ),
        # Container for information window
        dbc.Col(
            id = 'deacot_reference_card_hover',
            # deacot_reference_card,
            md=1,
        ),
    ]
)

# container for Incidence Chart
incidence_chart = html.Div([
],id = 'incidence-graph')



# Main layout
layout = html.Div([
    DROPDOWN_MENU,
    info_bar,
    # html.Hr(),
    line_graph,
    html.Hr(),
    incidence_chart,
    html.Hr(),
    # map_bar_chart,
], id="mainContainer",
    style={"display": "flex", "flex-direction": "column"})


###################################################
# Callbacks - Summary Block which contain KPI
###################################################
@callback(
    dash.dependencies.Output("summary", "children"),
    [dash.dependencies.Input('toggle', 'value'),
     dash.dependencies.Input("w_countries", "value"),
     dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date'),

     ],
)
def dashboard_summary_numbers(value, w_countries, start_date, end_date):
    if not value:
        report_data['date'] = pd.to_datetime(report_data['date'], format='%d-%m-%Y')
        report_data_summary = report_data[(report_data['date'] >= start_date) & (report_data['date'] <= end_date)]
        # report_data_summary = report_data
        sum_recovered_cases = report_data_summary[report_data_summary['district'] == w_countries].iloc[-1]['recovered']
        # Filtering unwanted values

        return html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Alert(
                            [
                                html.H6("Total Cases: ", style={'color': '#E65100'}),
                                html.H6(sf.format_number(report_data_summary[report_data_summary['district'] == w_countries].iloc[-1]['total']),
                                        style={'color': '#E65100'}),
                                dcc.Graph(figure={}, style={"height": "60px"}, id='KPI_Total_Cases', config={'displayModeBar': False})

                            ],
                            color="light",
                        ),
                        md=3,
                    ),
                    dbc.Col(
                        dbc.Alert(
                            [
                                html.H6("Total Deaths: ", style={'color': '#990000'}),
                                html.H6(sf.format_number(report_data_summary[report_data_summary['district'] == w_countries].iloc[-1]['deceased']),
                                        style={'color': '#990000'}),
                                dcc.Graph(figure={}, style={"height": "60px"}, id='KPI_Total_Deaths',
                                          config={'displayModeBar': False})
                            ],
                            color="light",

                        ),
                        md=3,
                    ),
                    dbc.Col(
                        dbc.Alert(
                            [
                                html.H6("Total Recover: ", style={'color': 'green'}),
                                html.H6(sf.format_number(sum_recovered_cases), style={'color': 'green'}),
                                dcc.Graph(figure={}, style={"height": "60px"}, id='KPI_Total_Recover',
                                          config={'displayModeBar': False})
                            ],
                            color="light",
                        ),
                        md=3,
                    ),
                    dbc.Col(
                        dbc.Alert(
                            [
                                html.H6("Total Active: ", style={'color': '#00004d'}),
                                html.H6(sf.format_number(report_data_summary[report_data_summary['district'] == w_countries].iloc[-1]['current_cases']),
                                        style={'color': '#00004d'}),
                                dcc.Graph(figure={}, style={"height": "60px"}, id='KPI_Total_Active',
                                          config={'displayModeBar': False})
                            ],
                            color="light",
                        ),
                        md=3,
                    ),

                ]
            )
        )
    else:

        if w_countries == 'Rheinland-Pfalz':
            sum_df = vaccine_data.groupby(['dose_group'])['number_of_vaccinations'].sum().reset_index()
            dose_1 = sum_df.loc[sum_df['dose_group'] == 1, 'number_of_vaccinations'].values[0]
            dose_2 = sum_df.loc[sum_df['dose_group'] == 2, 'number_of_vaccinations'].values[0]
            dose_3 = sum_df.loc[sum_df['dose_group'] == 3, 'number_of_vaccinations'].values[0]
            dose_4 = sum_df.loc[sum_df['dose_group'] == 4, 'number_of_vaccinations'].values[0]
        else:
            # vaccine_data1 = vaccine_data[(vaccine_data['date'] >= start_date) & (vaccine_data['date'] <= end_date)]
            dose_1 = vaccine_data[(vaccine_data.Name == w_countries) & (vaccine_data.dose_group == 1)].number_of_vaccinations.sum()
            dose_2 = vaccine_data[
                (vaccine_data.Name == w_countries) & (vaccine_data.dose_group == 2)].number_of_vaccinations.sum()
            dose_3 = vaccine_data[
                (vaccine_data.Name == w_countries) & (vaccine_data.dose_group == 3)].number_of_vaccinations.sum()
            dose_4 = vaccine_data[
                (vaccine_data.Name == w_countries) & (vaccine_data.dose_group == 4)].number_of_vaccinations.sum()

            # vaccine1 = vaccine_data1[vaccine_data1.Name == w_countries].number_of_vaccinations.sum()

        return html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Alert(
                            [
                                html.H6("First Vaccination: "),
                                html.H6(sf.format_number(dose_1)),
                                dcc.Graph(figure={}, style={"height": "60px"}, id='KPI_First_Vaccine',
                                          config={'displayModeBar': False})
                            ],
                            color="light",
                        ),
                        md = 3,
                    ),
                    dbc.Col(
                        dbc.Alert(
                            [
                                html.H6("Primary Vaccination:  "),
                                html.H6(sf.format_number(dose_2)),
                                dcc.Graph(figure={}, style={"height": "60px"}, id='KPI_Second_Vaccine',
                                          config={'displayModeBar': False})
                            ],
                            color="light",
                        ),
                        md=3,
                    ),
                    dbc.Col(
                        dbc.Alert(
                            [
                                html.H6("First Booster Dose: "),
                                html.H6(sf.format_number(dose_3)),
                                dcc.Graph(figure={}, style={"height": "60px"}, id='KPI_First_Booster_Vaccine',
                                          config={'displayModeBar': False})
                            ],
                            color="light",
                        ),
                        md=3,
                    ),
                    dbc.Col(
                        dbc.Alert(
                            [
                                html.H6("Second Booster Dose: "),
                                html.H6(sf.format_number(dose_4)),
                                dcc.Graph(figure={}, style={"height": "60px"}, id='KPI_Second_Booster_Vaccine',
                                          config={'displayModeBar': False})
                            ],
                            color="light",
                        ),
                        md=3,
                    ),

                    ]
            )
        )


###################################################
# Callbacks - KPI Block
###################################################
@callback(
    dash.dependencies.Output('KPI_Total_Cases', 'figure'),
    [dash.dependencies.Input("w_countries", "value"),
     dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date'),
     dash.dependencies.Input('toggle1', 'value')
     ],
)
def get_KPI_chart(w_countries,start_date,end_date,value1):
    # print(value1)
    if not value1:
        report_data['date'] = pd.to_datetime(report_data['date'], format='%d-%m-%Y')
        df = report_data[(report_data['date'] >= start_date) & (report_data['date'] <= end_date) & (report_data['district'] == w_countries)]
        # df.total = df.total - df.total.shift(1)
        df.total_diff = df.total_diff.rolling(7, min_periods=2).mean()
        fig = px.area(df, x='date', y='total_diff', color_discrete_sequence=['#E65100'])

        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0),showlegend=False)
        # Remove x and y axis lines, values, and tick marks
        fig.update_xaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        fig.update_yaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])

        # Set graph background color to whitestick
        fig.update_layout(plot_bgcolor='white',hovermode=False)
        return fig
    else:
        report_data['date'] = pd.to_datetime(report_data['date'], format='%d-%m-%Y')
        df = report_data[(report_data['date'] >= start_date) & (report_data['date'] <= end_date) & (
                    report_data['district'] == w_countries)]
        # df.total = df.total - df.total.shift(1)
        df.total = df.total.rolling(7, min_periods=2).mean()
        fig = px.area(df, x='date', y='total', color_discrete_sequence=['#E65100'])

        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
        # Remove x and y axis lines, values, and tick marks
        fig.update_xaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        fig.update_yaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])

        # Set graph background color to whitestick
        fig.update_layout(plot_bgcolor='white', hovermode=False)
        return fig


@callback(
    dash.dependencies.Output('KPI_Total_Deaths', 'figure'),
    [dash.dependencies.Input("w_countries", "value"),
     dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date'),
    dash.dependencies.Input('toggle1', 'value')
     ],
)
def get_KPI_Deaths_chart(w_countries,start_date,end_date,value1):
    if not value1:
        report_data['date'] = pd.to_datetime(report_data['date'], format='%d-%m-%Y')
        df = report_data[(report_data['date'] >= start_date) & (report_data['date'] <= end_date) & (report_data['district'] == w_countries)]
        # df.deceased = df.deceased - df.deceased.shift(1)
        df.deceased_diff = df.deceased_diff.rolling(7, min_periods=2).mean()
        fig = px.area(df, x='date', y='deceased_diff',color_discrete_sequence=['#990000'])
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0),showlegend=False)
        # fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        # , color_discrete_sequence=['red']
        # Remove x and y axis lines, values, and tick marks
        fig.update_xaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        fig.update_yaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])

        # Set graph background color to white
        fig.update_layout(plot_bgcolor='white',hovermode=False)
        return fig
    else:
        report_data['date'] = pd.to_datetime(report_data['date'], format='%d-%m-%Y')
        df = report_data[(report_data['date'] >= start_date) & (report_data['date'] <= end_date) & (
                    report_data['district'] == w_countries)]
        # df.deceased = df.deceased - df.deceased.shift(1)
        df.deceased = df.deceased.rolling(7, min_periods=2).mean()
        fig = px.area(df, x='date', y='deceased', color_discrete_sequence=['#990000'])
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
        # fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        # , color_discrete_sequence=['red']
        # Remove x and y axis lines, values, and tick marks
        fig.update_xaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        fig.update_yaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])

        # Set graph background color to white
        fig.update_layout(plot_bgcolor='white', hovermode=False)
        return fig


@callback(
    dash.dependencies.Output('KPI_Total_Recover', 'figure'),
    [dash.dependencies.Input("w_countries", "value"),
     dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date'),
     dash.dependencies.Input('toggle1', 'value')
     ],
)
def get_KPI_Recover_chart(w_countries,start_date,end_date,value1):
    if not value1:
        report_data['date'] = pd.to_datetime(report_data['date'], format='%d-%m-%Y')
        df = report_data[(report_data['date'] >= start_date) & (report_data['date'] <= end_date) & (report_data['district'] == w_countries)]
        df.recovered_diff = df.recovered_diff.rolling(7, min_periods=2).mean()
        fig = px.area(df, x='date', y='recovered_diff',color_discrete_sequence=['green'])

        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0),showlegend=False)
        # fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

        # Remove x and y axis lines, values, and tick marks
        fig.update_xaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        fig.update_yaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])

        # Set graph background color to white
        fig.update_layout(plot_bgcolor='white',hovermode=False)
        return fig
    else:
        report_data['date'] = pd.to_datetime(report_data['date'], format='%d-%m-%Y')
        df = report_data[(report_data['date'] >= start_date) & (report_data['date'] <= end_date) & (
                    report_data['district'] == w_countries)]
        df.recovered = df.recovered.rolling(7, min_periods=2).mean()
        fig = px.area(df, x='date', y='recovered', color_discrete_sequence=['green'])

        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
        # fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

        # Remove x and y axis lines, values, and tick marks
        fig.update_xaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        fig.update_yaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])

        # Set graph background color to white
        fig.update_layout(plot_bgcolor='white', hovermode=False)
        return fig


@callback(
    dash.dependencies.Output('KPI_Total_Active', 'figure'),
    [dash.dependencies.Input("w_countries", "value"),
     dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date'),
     dash.dependencies.Input('toggle1', 'value')
     ],
)
def get_KPI_Active_chart(w_countries,start_date,end_date,value1):
    if not value1:
        report_data['date'] = pd.to_datetime(report_data['date'], format='%d-%m-%Y')
        df = report_data[(report_data['date'] >= start_date) & (report_data['date'] <= end_date) & (report_data['district'] == w_countries)]
        fig = px.area(df, x='date', y='current_cases',color_discrete_sequence=['#00004d'])
        # 00004d
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

        # Remove x and y axis lines, values, and tick marks
        fig.update_xaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        fig.update_yaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])

        # Set graph background color to white
        fig.update_layout(plot_bgcolor='white',hovermode=False)
        return fig
    else:
        report_data['date'] = pd.to_datetime(report_data['date'], format='%d-%m-%Y')
        df = report_data[(report_data['date'] >= start_date) & (report_data['date'] <= end_date) & (
                    report_data['district'] == w_countries)]
        df.current_cases = df.current_cases.cumsum().rolling(7, min_periods=2).mean()
        fig = px.area(df, x='date', y='current_cases', color_discrete_sequence=['#00004d'])
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

        # Remove x and y axis lines, values, and tick marks
        fig.update_xaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        fig.update_yaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])

        # Set graph background color to white
        fig.update_layout(plot_bgcolor='white', hovermode=False)
        return fig

# Vaccine Section

@callback(
    dash.dependencies.Output('KPI_First_Vaccine', 'figure'),
    [dash.dependencies.Input("w_countries", "value"),
     dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date'),
     dash.dependencies.Input('toggle1', 'value')
     ],
)
def get_KPI_Vaccine_chart(w_countries,start_date,end_date,value1):
    if not value1:
        df = vaccine_data[(vaccine_data['date'] >= start_date) & (vaccine_data['date'] <= end_date)]
        # use of support functions
        df1 = sf.make_KPI_vaccine(df, w_countries,1)

        fig = px.area(df1, x='date', y='number_of_vaccinations',color_discrete_sequence=['#64B96A'])
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        # Remove x and y axis lines, values, and tick marks
        fig.update_xaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        fig.update_yaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        # Set graph background color to white
        fig.update_layout(plot_bgcolor='white',hovermode=False)
        return fig
    else:
        df = vaccine_data[(vaccine_data['date'] >= start_date) & (vaccine_data['date'] <= end_date)]
        # use of support functions
        df1 = sf.make_KPI_vaccine(df, w_countries,1)
        df1.number_of_vaccinations = df1.number_of_vaccinations.cumsum()
        fig = px.area(df1, x='date', y='number_of_vaccinations',color_discrete_sequence=['#64B96A'])
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        # Remove x and y axis lines, values, and tick marks
        fig.update_xaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        fig.update_yaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        # Set graph background color to white
        fig.update_layout(plot_bgcolor='white',hovermode=False)
        return fig


@callback(
    dash.dependencies.Output('KPI_Second_Vaccine', 'figure'),
    [dash.dependencies.Input("w_countries", "value"),
     dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date'),
     dash.dependencies.Input('toggle1', 'value')
     ],
)
def get_KPI_Vaccine_chart(w_countries,start_date,end_date,value1):
    if not value1:
        df = vaccine_data[(vaccine_data['date'] >= start_date) & (vaccine_data['date'] <= end_date)]
        # use of support functions
        df1 = sf.make_KPI_vaccine(df, w_countries,2)
        fig = px.area(df1, x='date', y='number_of_vaccinations',color_discrete_sequence=['#00A1D6'])
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        # Remove x and y axis lines, values, and tick marks
        fig.update_xaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        fig.update_yaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        # Set graph background color to white
        fig.update_layout(plot_bgcolor='white',hovermode=False)
        return fig
    else:
        df = vaccine_data[(vaccine_data['date'] >= start_date) & (vaccine_data['date'] <= end_date)]
        # use of support functions
        df1 = sf.make_KPI_vaccine(df, w_countries,2)
        df1.number_of_vaccinations = df1.number_of_vaccinations.cumsum()
        fig = px.area(df1, x='date', y='number_of_vaccinations',color_discrete_sequence=['#00A1D6'])
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        # Remove x and y axis lines, values, and tick marks
        fig.update_xaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        fig.update_yaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        # Set graph background color to white
        fig.update_layout(plot_bgcolor='white',hovermode=False)
        return fig

@callback(
    dash.dependencies.Output('KPI_First_Booster_Vaccine', 'figure'),
    [dash.dependencies.Input("w_countries", "value"),
     dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date'),
     dash.dependencies.Input('toggle1', 'value')
     ],
)
def get_KPI_Vaccine_chart(w_countries,start_date,end_date,value1):
    if not value1:
        df = vaccine_data[(vaccine_data['date'] >= start_date) & (vaccine_data['date'] <= end_date)]
        # use of support functions
        df1 = sf.make_KPI_vaccine(df, w_countries,3)
        fig = px.area(df1, x='date', y='number_of_vaccinations',color_discrete_sequence=['#FFA500'])
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        # Remove x and y axis lines, values, and tick marks
        fig.update_xaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        fig.update_yaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        # Set graph background color to white
        fig.update_layout(plot_bgcolor='white',hovermode=False)
        return fig
    else:
        df = vaccine_data[(vaccine_data['date'] >= start_date) & (vaccine_data['date'] <= end_date)]
        # use of support functions
        df1 = sf.make_KPI_vaccine(df, w_countries,3)
        df1.number_of_vaccinations = df1.number_of_vaccinations.cumsum()
        fig = px.area(df1, x='date', y='number_of_vaccinations',color_discrete_sequence=['#FFA500'])
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        # Remove x and y axis lines, values, and tick marks
        fig.update_xaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        fig.update_yaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        # Set graph background color to white
        fig.update_layout(plot_bgcolor='white',hovermode=False)
        return fig
@callback(
    dash.dependencies.Output('KPI_Second_Booster_Vaccine', 'figure'),
    [dash.dependencies.Input("w_countries", "value"),
     dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date'),
     dash.dependencies.Input('toggle1', 'value')
     ],
)
def get_KPI_Vaccine_chart(w_countries,start_date,end_date,value1):
    if not value1:
        df = vaccine_data[(vaccine_data['date'] >= start_date) & (vaccine_data['date'] <= end_date)]
        # use of support functions
        df1 = sf.make_KPI_vaccine(df, w_countries,4)
        fig = px.area(df1, x='date', y='number_of_vaccinations',color_discrete_sequence=['#800080'])
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        # Remove x and y axis lines, values, and tick marks
        fig.update_xaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        fig.update_yaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        # Set graph background color to white
        fig.update_layout(plot_bgcolor='white',hovermode=False)
        return fig
    else:
        df = vaccine_data[(vaccine_data['date'] >= start_date) & (vaccine_data['date'] <= end_date)]
        # use of support functions
        df1 = sf.make_KPI_vaccine(df, w_countries,4)
        df1.number_of_vaccinations = df1.number_of_vaccinations.cumsum()
        fig = px.area(df1, x='date', y='number_of_vaccinations',color_discrete_sequence=['#800080'])
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        # Remove x and y axis lines, values, and tick marks
        fig.update_xaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        fig.update_yaxes(title=None, showline=False, showgrid=False, zeroline=False, tickvals=[])
        # Set graph background color to white
        fig.update_layout(plot_bgcolor='white',hovermode=False)
        return fig


###################################################
# Callbacks - Map Block
###################################################
@callback(
    dash.dependencies.Output('map_chart', 'figure'),
    [
        dash.dependencies.Input('toggle', 'value'),
        dash.dependencies.Input('date-picker-range', 'start_date'),
        dash.dependencies.Input('date-picker-range', 'end_date')
    ],
)
def get_mapchart(value, start_date, end_date):
    if not value:
        # use of support functions

        df = sf.get_map_covidData(report_data, rheinland_states, start_date, end_date)

        edges = pd.cut(df["total"], bins=5, retbins=True)[1]
        edges = edges[:-1] / edges[-1]
        colors = ["#dddeea", "#cccee0", "#bbbed6", "#999dc1", "#777dad", "#555c98"]
        # Adding color scale to bins
        cc_scale = (
                [(0, colors[0])]
                + [(e, colors[(i + 1) // 2]) for i, e in enumerate(np.repeat(edges, 2))]
                + [(1, colors[5])]
        )
        fig = px.choropleth(df, locations="id",
                            color="total",
                            geojson=rheinland_states, hover_name="district",
                            hover_data=['deceased', 'recovered', 'current_cases'],
                            title='Demographic of Covid Cases from ' + start_date + ' to ' + end_date, scope='europe',
                            color_continuous_scale=cc_scale,
                            )
        fig.update_geos(fitbounds='locations', visible=False)
        return fig
    else:
        # use of support functions
        df = sf.get_map_vaccineData(vaccine_data, rheinland_states, start_date, end_date)
        edges = pd.cut(df["number_of_vaccinations"], bins=5, retbins=True)[1]
        edges = edges[:-1] / edges[-1]
        colors = ["#dddeea", "#cccee0", "#bbbed6", "#999dc1", "#777dad", "#555c98"]
        cc_scale = (
                [(0, colors[0])]
                + [(e, colors[(i + 1) // 2]) for i, e in enumerate(np.repeat(edges, 2))]
                + [(1, colors[5])])
        fig = px.choropleth(df, locations="id",
                            color="percentage",
                            geojson=rheinland_states, hover_name="Name", hover_data=['Name', 'number_of_vaccinations','Population','percentage'],
                            title='Demographic of Vaccincations ' + start_date + ' to ' + end_date, scope='europe',
                            color_continuous_scale=cc_scale,
                            # labels={'percentage': 'Vaccinations by population'}
                            )
        fig.update_geos(fitbounds='locations', visible=False)
        return fig

@callback(
    dash.dependencies.Output('deacot_reference_card_hover', 'children'),
    [dash.dependencies.Input('toggle', 'value')]
)
def update_modal(value):
    if not value:
        return deacot_reference_card
    else:
        return deacot_reference_card_vaccine

###################################################
# Callbacks - Incidence Block
###################################################
@callback(
    dash.dependencies.Output('incidence-graph', 'children'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date'),
     dash.dependencies.Input('w_countries', 'value'),
     dash.dependencies.Input('toggle', 'value')]
)

def update_output(start_date, end_date, district,value):
    if not value:
        selected_cols = ['district', 'incidence_7_days_rlp', 'date']
        filtered_df = report_data.query('district == @district and @start_date <= date <= @end_date')[selected_cols]
        conditions = [
            filtered_df['incidence_7_days_rlp'] <= 50,
            (filtered_df['incidence_7_days_rlp'] > 50) & (filtered_df['incidence_7_days_rlp'] <= 100),
            (filtered_df['incidence_7_days_rlp'] > 100) & (filtered_df['incidence_7_days_rlp'] < 200),
            filtered_df['incidence_7_days_rlp'] >= 200
        ]
        values = ['mild', 'moderate', 'severe', 'very severe']
        filtered_df['severity'] = np.select(conditions, values, 'mild')
        filtered_df['date'] = pd.to_datetime(filtered_df['date'], format='%d-%m-%Y')
        fig = px.bar(filtered_df, x='date', y='incidence_7_days_rlp', color='severity',
                     color_discrete_map={'very severe': 'red', 'severe': 'orange', 'moderate': 'yellow', 'mild': 'green'})
        fig.update_layout(legend=dict(title='Severity'),plot_bgcolor='white',
                          title=f'The 7 Days incidences of {district} from {start_date} to {end_date}')
        return (dbc.Row([
                dbc.Col(dcc.Graph(figure=fig), md=11),
            dbc.Col(
        deacot_reference_card2,
        md=1,)]),
                html.Hr(),
            dbc.Row([
            # container for Bar chart
            dbc.Col(
            id='try1'
            # dcc.Graph(figure={}, id='bar-chart-top')
            , md=7
        ),
            # container for Map
        dbc.Col(
            dcc.Graph(figure={}, id='map_chart'), md=5
        ),

        ]))
    else:

        return dbc.Row([
    # container for Bar chart
    dbc.Col(
        id='try1'
        # dcc.Graph(figure={}, id='bar-chart-top')
        , md=7
    ),
    # container for Map
    dbc.Col(
        dcc.Graph(figure={}, id='map_chart'), md=5
    ),

])


###################################################
# Callbacks - Line Chart Block
###################################################
@callback(
    dash.dependencies.Output("deacot_sent", "figure"),
    [dash.dependencies.Input("w_countries", "value"),
     dash.dependencies.Input('toggle', 'value'),
     dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date'),
     dash.dependencies.Input('toggle1', 'value')
     ],
)
def linechart(w_countries, value, start_date, end_date,value1):
    if not value:
        if not value1:
            report_data['date'] = pd.to_datetime(report_data['date'], format='%d-%m-%Y')
            df = report_data[(report_data['date'] >= start_date) & (report_data['date'] <= end_date) & (
                    report_data['district'] == w_countries)]
            # df = report_data[report_data.district == w_countries]
            # use of support functions
            fig = sf.make_chart_DA(df)
            return fig
            # return dcc.Loading(
            #     type="circle",
            #     children=[
            #         dcc.Graph(id="chart", figure=sf.make_chart_DA(df))
            #     ]
            # )
        else:
            report_data['date'] = pd.to_datetime(report_data['date'], format='%d-%m-%Y')
            df = report_data[(report_data['date'] >= start_date) & (report_data['date'] <= end_date) & (
                    report_data['district'] == w_countries)]

            # use of support functions
            fig = sf.make_chart_DA_comulative(df)
            return fig

    else:
        if not value1:

            # df = report_data[report_data.district == w_countries]
            df = vaccine_data[(vaccine_data['date'] >= start_date) & (vaccine_data['date'] <= end_date)]
            # use of support functions
            fig = sf.make_chart_vaccine(df, w_countries)
            return fig
        else:
            df = vaccine_data[(vaccine_data['date'] >= start_date) & (vaccine_data['date'] <= end_date)]
            # use of support functions
            fig = sf.make_chart_vaccine_comulative(df, w_countries)
            return fig


####################################################
#  Callbacks - Table chart
####################################################
@callback(
    dash.dependencies.Output("try1", "children"),
    [dash.dependencies.Input("w_countries", "value"),
        dash.dependencies.Input('toggle', 'value'),
     dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')
     ],
)
def get_barchart(w_countries, value, start_date, end_date):
    if not value:
        df = report_data[(report_data['date'] >= start_date) & (report_data['date'] <= end_date)& (
                report_data['district'] == w_countries)]
        # df = df.sort_values(by = 'date',ascending=False)
        df['date'] = df['date'].dt.date
        selected_columns = ['date', 'district', 'total', 'difference_previous_day',
                            'hospitalized', 'deceased', 'recovered', 'current_cases']
        df = df.loc[:, selected_columns]
        df.deceased = df.deceased - df.deceased.shift(1)
        df.hospitalized = df.hospitalized - df.hospitalized.shift(1)
        df.total = df.total - df.total.shift(1)
        df.recovered = df.recovered.astype(int)
        df.recovered = df.recovered - df.recovered.shift(1)
        df = df.sort_values(by='date', ascending=False)
        df = df.head(20)
        # create the table chart
        return html.Div([ html.H4('Record of Last 10 days of Cases'), dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",         # sort across 'multi' or 'single' columns
        page_action="native",       # all data is passed to the table up-front or not ('none')
        page_current=0,             # page number that user is on
        page_size=11,                # number of rows visible per page
        # style_cell={                # ensure adequate header width when text is shorter than cell's text
        #     'minWidth': 95, 'maxWidth': 95, 'width': 95
        # },
        style_data={                # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto'
        })])
    else:
        if w_countries == 'Rheinland-Pfalz':

            # vaccine_data['date'] = pd.to_datetime(vaccine_data['date'], format='%d-%m-%Y')
            df = vaccine_data[(vaccine_data['date'] >= start_date) & (vaccine_data['date'] <= end_date)]
            df['date'] = df['date'].dt.date
            df = df.sort_values(by='date', ascending=False)
            selected_columns = ['date', 'Name', 'vaccination_dose', 'number_of_vaccinations']
            df = df.loc[:, selected_columns]
        else:
            # vaccine_data['date'] = pd.to_datetime(vaccine_data['date'], format='%d-%m-%Y')
            df = vaccine_data[(vaccine_data['date'] >= start_date) & (vaccine_data['date'] <= end_date) &(
                vaccine_data['Name'] == w_countries)]
            df['date'] = df['date'].dt.date
            df = df.sort_values(by='date', ascending=False)
            selected_columns = ['date', 'Name', 'vaccination_dose', 'number_of_vaccinations']
            df = df.loc[:, selected_columns]
            df = df.head(20)


        return html.Div([html.H4('Record of Last 10 Days of Vaccinations'), dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",         # sort across 'multi' or 'single' columns
        page_action="native",       # all data is passed to the table up-front or not ('none')
        page_current=0,             # page number that user is on
        page_size=11,                # number of rows visible per page
        # style_cell={                # ensure adequate header width when text is shorter than cell's text
        #     'minWidth': 95, 'maxWidth': 95, 'width': 95
        # },
        style_data={                # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto'
        })])



####################################################
#  Callbacks - Modals
####################################################
# Deacot Reference Card
@callback(
    Output("deacot_card_modal", "is_open"),
    [
        Input("deacot_card_open", "n_clicks"),
        Input("deacot_card_close", "n_clicks"),
    ],
    [State("deacot_card_modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
#
# ####################################################
# #  Callbacks - Modals
# ####################################################
# # Deacot Reference Card
@callback(
    Output("deacot_card2_modal", "is_open"),
    [
        Input("deacot_card2_open", "n_clicks"),
        Input("deacot_card2_close", "n_clicks"),
    ],
    [State("deacot_card2_modal", "is_open")],
)
def toggle_modal1(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
# Vaccination Section
