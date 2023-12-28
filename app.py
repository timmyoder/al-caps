from collections import Counter

import pandas as pd

from dash import Dash, dcc, html, Input, Output, callback

import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from dash_holoniq_wordcloud import DashWordcloud

from sensitive_config import MAPBOX_TOKEN

px.set_mapbox_access_token(MAPBOX_TOKEN)

external_stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css']
PNNL_LOGO_PATH = 'assets/PNNL_vertical_logo.png'

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Analytics and Learning Team'
server = app.server

header_font = 'Merriweather, serif'
body_font = 'Montserrat, sans-serif'

survey_file = 'survey.csv'

NOT_ON_KEYWORD = 'No Filter'

survey_data = pd.read_csv(survey_file)


def word_bag(words=survey_data):
    word_list = {}

    for index, row in words.iterrows():
        name = row['Name']
        cap_1 = row['cap_1']
        cap_2 = row['cap_2']
        cap_3 = row['cap_3']
        cap_4 = row['cap_4']
        cap_5 = row['cap_5']
        word_list[name] = [cap_1, cap_2, cap_3]
        if cap_4 != " ":
            word_list[name].append(cap_4)
        if cap_5 != " ":
            word_list[name].append(cap_5)

    big_list = []
    for thing in word_list.keys():
        for item_ in word_list[thing]:
            big_list.append(item_)

    counted_words = Counter(big_list)
    word_cloud_list = []
    for word in counted_words.keys():
        word_cloud_list.append([word, counted_words[word] * 10])
    return word_cloud_list


def create_figure(survey_data):
    map_figure = px.scatter_mapbox(survey_data, lat="lat", lon="long",
                                   zoom=3,
                                   hover_data={
                                       "Name": True,
                                       "cap_1": True,
                                       "cap_2": True,
                                       'cap_3': True,
                                       'cap_4': True,
                                       'cap_5': True,
                                       'lat': False,
                                       'long': False},
                                   # height=600,
                                   # width=1000,
                                   )
    map_figure.update_traces(cluster=dict(enabled=True,
                                          maxzoom=14,
                                          size=25,
                                          ),
                             mode='markers',
                             marker=go.scattermapbox.Marker(size=50),
                             hovertemplate=
                             '<b>%{customdata[0]}</b>' +
                             '<br>%{customdata[1]}' +
                             '<br>%{customdata[2]}' +
                             '<br>%{customdata[3]}' +
                             '<br>%{customdata[4]}' +
                             '<br>%{customdata[5]}'
                             )
    map_figure.update_layout(autosize=True,
                             margin=dict(t=0, b=0, l=0, r=0)
                             )
    map_figure.update_layout(mapbox=dict(
        center=go.layout.mapbox.Center(
            lat=40,
            lon=-95
        ),
        zoom=3
    ))
    return map_figure


survey = pd.read_csv(survey_file)
initial_fig = create_figure(survey_data=survey)

app.layout = html.Div(children=[
    dbc.Row([
        html.H1("Analytics & Learning Team", style={'font-family': header_font}), ]),
    # mapbox
    dbc.Row([
        dbc.Col([
            dbc.Row([html.H3('A&L Capabilities and Home Bases'),
                     dcc.Graph(figure=initial_fig, id='map-figure'), ],
                    ), ],
            style={
                'width': '45vw',
                'height': '30vh',
                'margin-right': '20px',
                # 'padding': 10,
                # 'flex': 1
            }),

        # radio buttons
        dbc.Col([
            html.Br(),
            html.Br(),
            html.Label(html.B('This or That - A&L Team Preferences')),
            dcc.RadioItems(['Extrovert', 'Introvert', NOT_ON_KEYWORD], NOT_ON_KEYWORD,
                           inline=True, id='social'),
            dcc.RadioItems(['Vacation', 'Staycation', NOT_ON_KEYWORD], NOT_ON_KEYWORD,
                           inline=True, id='vaca'),
            dcc.RadioItems(['Morning', 'Night', NOT_ON_KEYWORD], NOT_ON_KEYWORD,
                           inline=True, id='night-owl'),
            dcc.RadioItems(['Driver', 'Passenger', NOT_ON_KEYWORD], NOT_ON_KEYWORD,
                           inline=True, id='car'),
            dcc.RadioItems(['Book', 'Movie', NOT_ON_KEYWORD], NOT_ON_KEYWORD,
                           inline=True, id='pastime'),
            dcc.RadioItems(['Tea', 'Coffee', NOT_ON_KEYWORD], NOT_ON_KEYWORD,
                           inline=True, id='beverage'),
            dcc.RadioItems(['City', 'Countryside', NOT_ON_KEYWORD], NOT_ON_KEYWORD,
                           inline=True, id='location'),
            html.Br(),
            html.H6('Team Members'),
            html.Div(id='my-list')
        ],
            style={
                # 'margin-top': '15px',
                # 'margin-right': '20px',
                'width': '15vw'
            }),
        dbc.Col([
            html.H3('Capabilities'),
            DashWordcloud(
                id='wordcloud',
                list=word_bag(),
                width=600, height=300,
                gridSize=25,
                color='#6371f2',
                backgroundColor='#ffffff',
                shuffle=False,
                rotateRatio=0.3,
                shrinkToFit=True,
                shape='circle',
                hover=True
            )
        ],
            style={
                # 'padding': 10,
                # 'flex': 1,
                'width': '35vw'
            }),
    ],
        style={
            'display': 'flex',
            'flexDirection': 'row'
        }
    ),
    html.Br(),
    html.Br(),
    html.Div(html.A(html.Img(src=PNNL_LOGO_PATH,
                             style={'height': '10%', 'width': '10%',
                                    'display': 'inline-block', 'margin': 'auto'}),
                    href='https://www.pnnl.gov/'),
             style={'textAlign': 'center'})])


@callback(
    Output('map-figure', 'figure'),
    Output('my-list', 'children'),
    Output('wordcloud', 'list'),
    Input('social', 'value'),
    Input('vaca', 'value'),
    Input('night-owl', 'value'),
    Input('car', 'value'),
    Input('pastime', 'value'),
    Input('beverage', 'value'),
    Input('location', 'value'))
def update_map(social, vaca, night_owl, car, pastime, beverage, location):
    survey_update = pd.read_csv(survey_file)

    if social != NOT_ON_KEYWORD:
        survey_update = survey_update[survey_update['social'] == social]
    if vaca != NOT_ON_KEYWORD:
        survey_update = survey_update[survey_update['vaca'] == vaca]
    if night_owl != NOT_ON_KEYWORD:
        survey_update = survey_update[survey_update['night-owl'] == night_owl]
    if car != NOT_ON_KEYWORD:
        survey_update = survey_update[survey_update['car'] == car]
    if pastime != NOT_ON_KEYWORD:
        survey_update = survey_update[survey_update['pastime'] == pastime]
    if beverage != NOT_ON_KEYWORD:
        survey_update = survey_update[survey_update['beverage'] == beverage]
    if location != NOT_ON_KEYWORD:
        survey_update = survey_update[survey_update['location'] == location]

    if not survey_update.empty:
        filtered_staff = survey_update['Name'].to_list()
    else:
        filtered_staff = ['No team members matching that combo...', ]

    word_list = word_bag(survey_update)

    return (create_figure(survey_update),
            [html.P(item) for item in filtered_staff],
            word_list)


if __name__ == '__main__':
    app.run_server(debug=False)
