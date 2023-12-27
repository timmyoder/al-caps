import pandas as pd

from dash import Dash, dcc, html, Input, Output, callback

import plotly.express as px
import plotly.graph_objects as go

from sensitive_config import MAPBOX_TOKEN

px.set_mapbox_access_token(MAPBOX_TOKEN)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
PNNL_LOGO_PATH = 'assets/PNNL_vertical_logo.png'

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Analytics and Learning Team'
server = app.server

header_font = 'Merriweather, serif'
body_font = 'Montserrat, sans-serif'

survey_file = 'survey.csv'


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
                                   height=600,
                                   width=1000
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
    map_figure.update_layout(autosize=True,)
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

app.layout = html.Div([
    html.H1("Analytics & Learning Team", style={'font-family': header_font}),
    html.Div([
        html.Div(children=[
            dcc.RadioItems(['Extrovert', 'Introvert', 'Either'], 'Either',
                           inline=True, id='social'),
            dcc.RadioItems(['Vacation', 'Staycation', 'Either'], 'Either',
                           inline=True, id='vaca'),
            dcc.RadioItems(['Morning', 'Night', 'Either'], 'Either',
                           inline=True, id='night-owl'),
            dcc.RadioItems(['Driver', 'Passenger', 'Either'], 'Either',
                           inline=True, id='car'),
            dcc.RadioItems(['Book', 'Movie', 'Either'], 'Either',
                           inline=True, id='pastime'),
            dcc.RadioItems(['Tea', 'Coffee', 'Either'], 'Either',
                           inline=True, id='beverage'),
            dcc.RadioItems(['City', 'Countryside', 'Either'], 'Either',
                           inline=True, id='location'), ],
            style={'padding': 10, 'flex': 1}),
        html.Div(children=[
            dcc.Graph(figure=initial_fig, id='map-figure'), ],
            style={'padding': 10, 'flex': 1}),

    ], style={'display': 'flex', 'flexDirection': 'row'}
    ),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div(html.A(html.Img(src=PNNL_LOGO_PATH,
                             style={'height': '10%', 'width': '10%',
                                    'display': 'inline-block', 'margin': 'auto'}),
                    href='https://www.pnnl.gov/'),
             style={'textAlign': 'center'})])

@callback(
    Output('map-figure', 'figure'),
    Input('social', 'value'),
    Input('vaca', 'value'),
    Input('night-owl', 'value'),
    Input('car', 'value'),
    Input('pastime', 'value'),
    Input('beverage', 'value'),
    Input('location', 'value'))
def update_map(social, vaca, night_owl, car, pastime, beverage, location):
    survey_update = pd.read_csv(survey_file)

    if social != 'Either':
        survey_update = survey_update[survey_update['social'] == social]
    if vaca != 'Either':
        survey_update = survey_update[survey_update['vaca'] == vaca]
    if night_owl != 'Either':
        survey_update = survey_update[survey_update['night-owl'] == night_owl]
    if car != 'Either':
        survey_update = survey_update[survey_update['car'] == car]
    if pastime != 'Either':
        survey_update = survey_update[survey_update['pastime'] == pastime]
    if beverage != 'Either':
        survey_update = survey_update[survey_update['beverage'] == beverage]
    if location != 'Either':
        survey_update = survey_update[survey_update['location'] == location]

    return create_figure(survey_update)


if __name__ == '__main__':
    app.run_server(debug=True)
