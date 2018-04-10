import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime as dt
from heartHandler import *
from sleepHandler import *
from stepHandler import *

def dateAsString(date):
    return date.strftime('%Y-%m-%d')

class dashGraph():
    def __init__(self):
        current_slide = [0,24]
        heartLogs = heartHandler(dateAsString(dt.date.today()))
        stepLogs = stepHandler(dateAsString(dt.date.today()))
        sleepLogs = sleepHandler(dateAsString(dt.date.today()))
        handlers = {'heartLogs': heartLogs, 'stepLogs': stepLogs, 'sleepLogs': sleepLogs }

        self.app = dash.Dash(csrf_protect=False)

        available_indicators = ['heartLogs', 'stepLogs', 'sleepLogs']

#################### ================================================================================= #######################
        self.app.layout = html.Div(children=[
            html.Button(id='refresh_button', n_clicks=0, children='Refresh'),
            dcc.Input(id='startdate-input', type='Date', value=dt.date.today()),
            dcc.RangeSlider(id="Slider",
                min=0, max=24,
                marks={i: str(i) for i in range(0, 24)},
                value=[0,24],
            ),
            html.H1(children='FitBit Monitor'),
            html.Div(dcc.Graph( id='sleep-graphic',
                figure={
                    'title': "Sleep Logs",
                    'data': [{
                        'labels': ['Deep', 'Light', 'REM', 'Awake'],
                        'values': sleepLogs.getSummary(),
                        'type': 'pie','name': 'Sleep',
                        'marker': {'colors': ['rgb(75, 180, 75)', 'rgb(75, 220, 75)','rgb(50, 100, 100)','rgb(180, 75, 75)']},
                        'hoverinfo':'label+percent','textinfo':'none'
                    },]}
            ),style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

            html.Div([
                    dcc.Graph(id='indicator-graphic',
                        figure={
                            'data': [ {'x': heartLogs.plotData[0], 'y': heartLogs.plotData[1], 'type': 'line', 'name': 'SF'} ]
                        } ),
                    dcc.Dropdown( id='yaxis-column', options=[{'label': i, 'value': i} for i in available_indicators], value='heartLogs'),

                    dcc.Graph( id='indicator-graphic2',
                    figure={
                        'data': [ {'x': stepLogs.plotData[0], 'y': stepLogs.plotData[1], 'type': 'line', 'name': 'SF'} ]
                        }),
                    dcc.Dropdown( id='yaxis-column2', options=[{'label': i, 'value': i} for i in available_indicators], value='stepLogs')
            ], style={'width': '48%', 'float': 'left', 'display': 'inline-block'}),

            dcc.Interval(id='interval-component', interval=300*1000)
        ])
#################### ================================================================================= #######################

        @self.app.callback(
            dash.dependencies.Output('indicator-graphic', 'figure'),
            inputs=[dash.dependencies.Input('yaxis-column', 'value'), dash.dependencies.Input('Slider','value'), dash.dependencies.Input('refresh_button','n_clicks')]
            )
        def update_graph(yaxis_column_name, slider_val, button):
            handlers[yaxis_column_name].update()

            handlers[yaxis_column_name].scale(slider_val)
            current_slide = slider_val
            return {
                    'data': [{'x': handlers[yaxis_column_name].plotData[0], 'y': handlers[yaxis_column_name].plotData[1], 'type': 'line', 'name': 'SF'}],
                    'layout': {'title': yaxis_column_name + handlers[yaxis_column_name].getTitle()}
            }

        @self.app.callback(dash.dependencies.Output('refresh_button', 'n_clicks'),
            inputs=[dash.dependencies.Input('startdate-input', 'value')],
            events=[dash.dependencies.Event('interval-component', 'interval')])
        def update_graph(DATE):
            for i in handlers:
                # if handlers[i].date != DATE:
                handlers[i].changeDate(DATE)
                handlers[i].scale(current_slide)
                return {
                    'n_clicks': 1
                }


        @self.app.callback(dash.dependencies.Output('indicator-graphic2', 'figure'),
            inputs=[dash.dependencies.Input('yaxis-column2', 'value'), dash.dependencies.Input('Slider','value'), dash.dependencies.Input('refresh_button','n_clicks')])
        def update_graph(yaxis_column_name, slider_val, button):
            handlers[yaxis_column_name].update()
            handlers[yaxis_column_name].scale(slider_val)
            current_slide = slider_val
            return {
                    'data': [{'x': handlers[yaxis_column_name].plotData[0], 'y': handlers[yaxis_column_name].plotData[1], 'type': 'line', 'name': 'SF'}],
                    'layout': {'title': yaxis_column_name + handlers[yaxis_column_name].getTitle()}
            }
