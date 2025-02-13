"""
    This files contains all the major functions

    We have functions for getting the reports and processing as well as
    generating the actual charts.

    This file is called by both the main app as well as the business logic

"""

import pandas as pd
import plotly.graph_objects as go

import pages.layout_configs as lc

pd.options.mode.chained_assignment = None

def format_number(number):
    if number >= 1000000:
        return "{:.2f}M".format(number/1000000)
    elif number >= 1000:
        return "{:,.0f}".format(number)
    elif number <= 999:
        return number
    else:
        return "{:.2f}K".format(number/1000)




def get_vaccinedata(df_vaccinedata,df_regiondata):
    # df_vaccinedata = df_vaccinedata.rename(columns = { 'Impfdatum': 'date','LandkreisId_Impfort':'region_code', 'Altersgruppe':'age_group','Impfschutz':'vaccination_dose','Anzahl':'total_vaccination'})
    df_regiondata['Regional code'] = df_regiondata['Regional code'].astype(int)
    data_with_regionname = df_vaccinedata.merge(df_regiondata,how='left', left_on='LandkreisId_Impfort',right_on='Regional code')
    data_with_regionname = data_with_regionname.dropna()
    data_with_regionname = data_with_regionname.reset_index()
    data_with_regionname = data_with_regionname.drop(columns=['index','Regional code'])
    data_with_regionname["Impfdatum"] = data_with_regionname["Impfdatum"].astype('datetime64[ns]')
    data_with_regionname = data_with_regionname.rename(columns={'Impfdatum': 'date','LandkreisId_Impfort':'region_code','Altersgruppe':'age_group','Impfschutz':'vaccination_dose','Anzahl':'number_of_vaccinations'})
    dose_map = {1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 6: 4, 11: 4}
    data_with_regionname['dose_group'] = data_with_regionname['vaccination_dose'].replace(dose_map)
    return data_with_regionname
#############################################################################
# Charts
#############################################################################
def make_chart_vaccine(df, district):
    fig = go.Figure(layout=lc.layout_simple)

    if district == 'Rheinland-Pfalz':
        df1 = make_KPI_vaccine(df, district, 1)
        df2 = make_KPI_vaccine(df, district, 2)
        df3 = make_KPI_vaccine(df, district, 3)
        df4 = make_KPI_vaccine(df, district, 4)
        # df = df.groupby(['date'])[['number_of_vaccinations']].sum().reset_index()
        fig.add_traces(
            go.Scatter(
                x=df1.date,
                y=df1.number_of_vaccinations.rolling(7, min_periods=2).mean(),
                name="First Vaccination",
                line_width=2,
                line_color='#64B96A',
                # fill="tonexty",
            )
        )
        fig.add_traces(
            go.Scatter(
                x=df2.date,
                y=df2.number_of_vaccinations.rolling(7, min_periods=2).mean(),
                name="Primary Vaccination",
                line_width=2,
                line_color='#00A1D6',
                # fill="tonexty",
            )
        )
        fig.add_traces(
            go.Scatter(
                x=df3.date,
                y=df3.number_of_vaccinations.rolling(7, min_periods=2).mean(),
                name="First Booster Vaccination",
                line_width=2,
                line_color='#FFA500',
                # fill="tonexty",
            )
        )
        fig.add_traces(
            go.Scatter(
                x=df4.date,
                y=df4.number_of_vaccinations.rolling(7, min_periods=2).mean(),
                name="Second Booster Vaccination",
                line_color='#800080',
                line_width=2,
                # fill="tonexty",
            )
        )
    else:
        df1 = make_KPI_vaccine(df, district, 1)
        df2 = make_KPI_vaccine(df, district, 2)
        df3 = make_KPI_vaccine(df, district, 3)
        df4 = make_KPI_vaccine(df, district, 4)
        # df = df.groupby(['date'])[['number_of_vaccinations']].sum().reset_index()
        fig.add_traces(
            go.Scatter(
                x=df1.date,
                y=df1.number_of_vaccinations.rolling(7, min_periods=2).mean(),
                name="First Vaccination",
                line_color='#64B96A',
                line_width=2,
                # fill="tonexty",
            )
        )
        fig.add_traces(
            go.Scatter(
                x=df2.date,
                y=df2.number_of_vaccinations.rolling(7, min_periods=2).mean(),
                name="Primary Vaccination",
                line_color='#00A1D6',
                line_width=2,
                # fill="tonexty",
            )
        )
        fig.add_traces(
            go.Scatter(
                x=df3.date,
                y=df3.number_of_vaccinations.rolling(7, min_periods=2).mean(),
                name="First Booster Vaccination",
                line_color='#FFA500',
                line_width=2,
                # fill="tonexty",
            )
        )
        fig.add_traces(
            go.Scatter(
                x=df4.date,
                y=df4.number_of_vaccinations.rolling(7, min_periods=2).mean(),
                name="Second Booster Vaccination",
                line_color='#800080',
                line_width=2,
                # fill="tonexty",
            )
        )
    fig.update_layout(
        newshape=dict(line_color="yellow"),
        title="vaccination in " + district,
        xaxis_title="date",
        yaxis_title='Number of Vaccinations',
        # xaxis=dict(showgrid=False),
        # yaxis=dict(showgrid=False)
    )
    # fig.show(config=lc.tool_config)
    return fig


def make_chart_vaccine_comulative(df, district):
    fig = go.Figure(layout=lc.layout_simple)

    if district == 'Rheinland-Pfalz':
        df1 = make_KPI_vaccine(df, district, 1)
        df2 = make_KPI_vaccine(df, district, 2)
        df3 = make_KPI_vaccine(df, district, 3)
        df4 = make_KPI_vaccine(df, district, 4)
        # df = df.groupby(['date'])[['number_of_vaccinations']].sum().reset_index()
        fig.add_traces(
            go.Scatter(
                x=df1.date,
                y=df1.number_of_vaccinations.cumsum().rolling(7, min_periods=2).mean(),
                name="First Vaccination",
                line_width=2,
                line_color='#64B96A',
                # fill="tonexty",
            )
        )
        fig.add_traces(
            go.Scatter(
                x=df2.date,
                y=df2.number_of_vaccinations.cumsum().rolling(7, min_periods=2).mean(),
                name="Primary Vaccination",
                line_width=2,
                line_color='#00A1D6',
                # fill="tonexty",
            )
        )
        fig.add_traces(
            go.Scatter(
                x=df3.date,
                y=df3.number_of_vaccinations.cumsum().rolling(7, min_periods=2).mean(),
                name="First Booster Vaccination",
                line_width=2,
                line_color='#FFA500',
                # fill="tonexty",
            )
        )
        fig.add_traces(
            go.Scatter(
                x=df4.date,
                y=df4.number_of_vaccinations.cumsum().rolling(7, min_periods=2).mean(),
                name="Second Booster Vaccination",
                line_color='#800080',
                line_width=2,
                # fill="tonexty",
            )
        )
    else:
        df1 = make_KPI_vaccine(df, district, 1)
        df2 = make_KPI_vaccine(df, district, 2)
        df3 = make_KPI_vaccine(df, district, 3)
        df4 = make_KPI_vaccine(df, district, 4)
        # df = df.groupby(['date'])[['number_of_vaccinations']].sum().reset_index()
        fig.add_traces(
            go.Scatter(
                x=df1.date,
                y=df1.number_of_vaccinations.cumsum().rolling(7, min_periods=2).mean(),
                name="First Vaccination",
                line_color='#64B96A',
                line_width=2,
                # fill="tonexty",
            )
        )
        fig.add_traces(
            go.Scatter(
                x=df2.date,
                y=df2.number_of_vaccinations.cumsum().rolling(7, min_periods=2).mean(),
                name="Primary Vaccination",
                line_color='#00A1D6',
                line_width=2,
                # fill="tonexty",
            )
        )
        fig.add_traces(
            go.Scatter(
                x=df3.date,
                y=df3.number_of_vaccinations.cumsum().rolling(7, min_periods=2).mean(),
                name="First Booster Vaccination",
                line_color='#FFA500',
                line_width=2,
                # fill="tonexty",
            )
        )
        fig.add_traces(
            go.Scatter(
                x=df4.date,
                y=df4.number_of_vaccinations.cumsum().rolling(7, min_periods=2).mean(),
                name="Second Booster Vaccination",
                line_color='#800080',
                line_width=2,
                # fill="tonexty",
            )
        )
    fig.update_layout(
        newshape=dict(line_color="yellow"),
        title="vaccination in " + district,
        xaxis_title="date",
        yaxis_title='Number of Vaccinations',
        # xaxis=dict(showgrid=False),
        # yaxis=dict(showgrid=False)
    )
    # fig.show(config=lc.tool_config)
    return fig


def make_KPI_vaccine(df, district,dose):
    df = df[df['dose_group'] == dose]
    if district == 'Rheinland-Pfalz':
        df = df.groupby(['date'])[['number_of_vaccinations']].sum().reset_index()
    else:
        df = df.groupby(['date', 'Name'])[['number_of_vaccinations']].sum().reset_index()
        df = df[df['Name'] == district]
    df['number_of_vaccinations'] = df['number_of_vaccinations'].rolling(7, min_periods=2).mean()
    return df



# Create Covid Line chart
def make_chart_DA_comulative(df):
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    fig = go.Figure(layout=lc.layout_simple)
    fig.add_traces(
        go.Scatter(
            x=df.date,
            y=df.current_cases.cumsum().rolling(7, min_periods=2).mean(),
            name="Active Cases",
            line_color='#00004d',
            line_width=2,
        )
    )
    fig.add_traces(
        go.Scatter(
            x=df.date,
            y=df.difference_previous_day.rolling(7, min_periods=2).mean(),
            name="Daily Cases",
            line_width=2,
            line_color = '#4d0013',
            # fill="tonexty",
        )
    )

    fig.add_traces(
        go.Scatter(
            x=df.date,
            y=df.deceased.rolling(7, min_periods=2).mean(),
            name="Deceased",
            line_color = '#990000',
            line_width=2,
        )
    )

    fig.add_traces(
        go.Scatter(
            x=df.date,
            y=df.recovered.rolling(7, min_periods=2).mean(),
            name="Recovered cases",
            line_color='green',
            line_width=2,
        )
    )
    fig.add_traces(
        go.Scatter(
            x=df.date,
            y=df.hospitalized.rolling(7, min_periods=2).mean(),
            name="Hospitalized",
            line_color='yellow',
            line_width=2,
        )
    )
    fig.add_traces(
        go.Scatter(
            x=df.date,
            y=df.total.rolling(7, min_periods=2).mean(),
            name="Total Cases",
            line_color='orange',
            line_width=2,
        )
    )

    fig.update_traces(visible="legendonly", selector=lambda t: not t.name in ["Daily Cases","Deceased",'Active Cases'])

    fig.update_layout(
        newshape=dict(line_color="yellow"),
        title="Daily Positive, Deceased and Active Cases of " + df.district.iloc[-1] + ' from ' +
            str(df.date.iloc[0]) + " to " + str(df.date.iloc[-1]),
        xaxis_title="date",
        yaxis_title='Cases',
    )
    # fig.show(config=lc.tool_config)
    return fig

def make_chart_DA(df):
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    date = str(df['date'].iloc[-1])[:10]




    fig = go.Figure(layout=lc.layout_simple)


    fig.add_traces(
        go.Scatter(
            x=df.date,
            y=df.current_cases.rolling(7, min_periods=2).mean(),
            name="Active Cases",
            line_color='#00004d',
            line_width=2,
        )
    )


    fig.add_traces(
        go.Scatter(
            x=df.date,
            y=df.difference_previous_day.rolling(7, min_periods=2).mean(),
            name="Daily Cases",
            line_width=2,
            line_color = '#4d0013',
            # fill="tonexty",
        )
    )

    fig.add_traces(
        go.Scatter(
            x=df.date,
            y=df.deceased_diff.rolling(7, min_periods=2).mean(),
            name="Deceased",
            line_color = '#990000',
            line_width=2,
        )
    )

    fig.add_traces(
        go.Scatter(
            x=df.date,
            y=df.recovered_diff.rolling(7, min_periods=2).mean(),
            name="Recovered cases",
            line_color='green',
            line_width=2,
        )
    )
    fig.add_traces(
        go.Scatter(
            x=df.date,
            y=df.hospitalized_diff.rolling(7, min_periods=2).mean(),
            name="Hospitalized",
            line_color='yellow',
            line_width=2,
        )
    )
    fig.add_traces(
        go.Scatter(
            x=df.date,
            y=df.total_diff.rolling(7, min_periods=2).mean(),
            name="Total Cases",
            line_color='orange',
            line_width=2,
        )
    )

    fig.update_traces(visible="legendonly", selector=lambda t: not t.name in ["Daily Cases","Deceased",'Active Cases'])

    fig.update_layout(
        newshape=dict(line_color="yellow"),
        title="Daily Positive, Deceased and Active Cases of " + df.district.iloc[-1] + ' from ' +
            str(df.date.iloc[0]) + " to " + str(df.date.iloc[-1]),
        xaxis_title="date",
        yaxis_title='Cases',
    )
    # fig.show(config=lc.tool_config)
    return fig



def get_map_vaccineData(df,rheinland_states,start_date,end_date):
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    # df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    df = df[df.vaccination_dose == 2]
    df = df.groupby(['Name','Population'])[['number_of_vaccinations']].sum().reset_index()
    state_id_map = {}
    for feature in rheinland_states['features']:
        feature['id'] = feature['properties']['nuts']
        state_id_map[feature['properties']['county']] = feature['id']
    df = df.replace({'Name': {'Bitburg-Prüm': 'LK Bitburg-Prüm',
                              'Rhein-Hunsrück': 'LK Rhein-Hunsrück-Kreis',
                              'Südliche Weinstr.': 'LK Südliche Weinstraße',
                              'KS Frankenthal': 'SK Frankenthal',
                              'KS Kaiserslautern': 'SK Kaiserslautern',
                              'KS Koblenz': 'SK Koblenz',
                              'KS Landau i.d.Pf.': 'SK Landau i.d.Pfalz',
                              'KS Ludwigshafen': 'SK Ludwigshafen',
                              'KS Mainz': 'SK Mainz',
                              'KS Neustadt a.d.W.': 'SK Neustadt a.d.Weinstraße',
                              'KS Pirmasens': 'SK Pirmasens',
                              'KS Speyer': 'SK Speyer',
                              'KS Trier': 'SK Trier',
                              'KS Worms': 'SK Worms',
                              'KS Zweibrücken': 'SK Zweibrücken',
                              'Rhein-Pfalz-Kreis': 'LK Rhein-Pfalz-Kreis',
                              'Altenkirchen': 'LK Altenkirchen',
                              'Mayen-Koblenz': 'LK Mayen-Koblenz',
                              'Mainz-Bingen': 'LK Mainz-Bingen',
                              'Kusel': 'LK Kusel',
                              'Kaiserslautern': 'LK Kaiserslautern',
                              'Germersheim': 'LK Germersheim',
                              'Donnersbergkreis': 'LK Donnersbergkreis',
                              'Cochem-Zell': 'LK Cochem-Zell',
                              'Birkenfeld': 'LK Birkenfeld',
                              'Bernkastel-Wittlich': 'LK Bernkastel-Wittlich',
                              'Bad Kreuznach': 'LK Bad Kreuznach',
                              'Bad Dürkheim': 'LK Bad Dürkheim',
                              'Alzey-Worms': 'LK Alzey-Worms',
                              'Neuwied': 'LK Neuwied',
                              'Ahrweiler': 'LK Ahrweiler',
                              'Rhein-Lahn-Kreis': 'LK Rhein-Lahn-Kreis',
                              'Westerwaldkreis': 'LK Westerwaldkreis',
                              'Vulkaneifel': 'LK Vulkaneifel',
                              'Trier-Saarburg': 'LK Trier-Saarburg',
                              'Südwestpfalz': 'LK Südwestpfalz'}})
    df['id'] = df['Name'].apply(lambda x: state_id_map[x])
    df['percentage'] = df['number_of_vaccinations'] / df['Population']
    return df

def get_map_covidData(df,rheinland_states,start_date,end_date):
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    # df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    df = df[df['district']!= 'Rheinland-Pfalz']
    df = df.tail(36)

    state_id_map = {}
    for feature in rheinland_states['features']:
        feature['id'] = feature['properties']['nuts']
        state_id_map[feature['properties']['county']] = feature['id']
    df = df.replace({'district': {'Altenkirchen': 'LK Altenkirchen',
                                  'Ahrweiler': 'LK Ahrweiler',
                                  'Bitburg-Prüm': 'LK Bitburg-Prüm',
                                  'Rhein-Hunsrück': 'LK Rhein-Hunsrück-Kreis',
                                  'Südliche Weinstr.': 'LK Südliche Weinstraße',
                                  'KS Frankenthal': 'SK Frankenthal',
                                  'KS Kaiserslautern': 'SK Kaiserslautern',
                                  'KS Koblenz': 'SK Koblenz',
                                  'KS Landau i.d.Pf.': 'SK Landau i.d.Pfalz',
                                  'KS Ludwigshafen': 'SK Ludwigshafen',
                                  'KS Mainz': 'SK Mainz',
                                  'KS Neustadt a.d.W.': 'SK Neustadt a.d.Weinstraße',
                                  'KS Pirmasens': 'SK Pirmasens',
                                  'KS Speyer': 'SK Speyer',
                                  'KS Trier': 'SK Trier',
                                  'KS Worms': 'SK Worms',
                                  'KS Zweibrücken': 'SK Zweibrücken',
                                  'Rhein-Pfalz-Kreis': 'LK Rhein-Pfalz-Kreis',

                                  'Mayen-Koblenz': 'LK Mayen-Koblenz',
                                  'Mainz-Bingen': 'LK Mainz-Bingen',
                                  'Kusel': 'LK Kusel',
                                  'Kaiserslautern': 'LK Kaiserslautern',
                                  'Germersheim': 'LK Germersheim',
                                  'Donnersbergkreis': 'LK Donnersbergkreis',
                                  'Cochem-Zell': 'LK Cochem-Zell',
                                  'Birkenfeld': 'LK Birkenfeld',
                                  'Bernkastel-Wittlich': 'LK Bernkastel-Wittlich',
                                  'Bad Kreuznach': 'LK Bad Kreuznach',
                                  'Bad Dürkheim': 'LK Bad Dürkheim',
                                  'Alzey-Worms': 'LK Alzey-Worms',
                                  'Neuwied': 'LK Neuwied',
                                  'Rhein-Lahn-Kreis': 'LK Rhein-Lahn-Kreis',
                                  'Westerwaldkreis': 'LK Westerwaldkreis',
                                  'Vulkaneifel': 'LK Vulkaneifel',
                                  'Trier-Saarburg': 'LK Trier-Saarburg',
                                  'Südwestpfalz': 'LK Südwestpfalz'}})

    df['id'] = df['district'].apply(lambda x: state_id_map[x])
    return df



#############################################################################
# Backstop
#############################################################################
if __name__ == "__main__":
    print("Support Functions has nothing to run directly")



