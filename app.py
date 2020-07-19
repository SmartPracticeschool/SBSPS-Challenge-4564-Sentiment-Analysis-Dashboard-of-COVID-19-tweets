import os
import pathlib

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash_daq as daq

from datetime import datetime as dt
import pandas as pd

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = 'COVID Tweets Sentiment Dashboard'
server = app.server
app.config["suppress_callback_exceptions"] = True

APP_PATH = str(pathlib.Path(__file__).parent.resolve())

df_day = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "day_wise.csv")))
df_day['date'] = pd.to_datetime(df_day['date'])
#df_day.set_index('date', inplace=True)
#df_day.index = pd.to_datetime(df_day.index)
df_day= df_day.sort_values(by='date')

df_phase = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "phase_wise.csv")))
#df_phase.set_index('phase', inplace=True)
df_phase['start'] = pd.to_datetime(df_phase['start'])
df_phase['end'] = pd.to_datetime(df_phase['end'])
df_phase['date_mpos'] = pd.to_datetime(df_phase['date_mpos'])
df_phase['date_mneg'] = pd.to_datetime(df_phase['date_mneg'])
df_phase= df_phase.sort_values(by='start')
phases = ['Lockdown 1', 'Lockdown 2', 'Lockdown 3', 'Lockdown 4', 'Unlock 1', 'Unlock 2']
vals = [0,1,2,3,4,5]

def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("SENTIMENT ANALYSIS OF COVID-19 TWEETS"),
                    html.H6("Infering people's daily reactions and with various phases of lockdown"),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.Button(
                        id="learn-more-button", children="KNOW MORE ABOUT THE PROJECT", n_clicks=0
                    ),
                    html.Img(id="logo", src=app.get_asset_url("Logo.png")),
                ],
            ),
        ],
    )


def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab1",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="day-tab",
                        label="day wise statistics dashboard",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="phase-tab",
                        label="phase wise statistics Dashboard",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )


def generate_daywiseplot():
    df = df_day
    fig = make_subplots(rows=3, cols=1,
                shared_xaxes=True)
    fig.add_trace(go.Scatter(x = df['date'], y = df['pos'],
                        mode='lines+markers',
                        name = 'pos',
                        connectgaps=True, marker_color='rgb(35,132,67)'),
                        row=1, col=1)
    fig.add_trace(go.Scatter(x = df['date'], y = df['neg'],
                        mode='lines+markers',
                        name = 'neg',
                        connectgaps=True, marker_color='rgb(244,59,44)'),
                        row=2, col=1)
    fig.add_trace(go.Scatter(x = df['date'], y = df['neut'],
                        mode='lines+markers',
                        name = 'neut',
                        connectgaps=True, marker_color='rgb(62,83,160)'),
                        row=3, col=1)
    fig.update_layout(template='plotly_dark',
                  #paper_bgcolor='rgba(0,0,0,0)',
                  #plot_bgcolor='rgba(0,0,0,0)',
                  xaxis_showgrid=False,
                  yaxis_showgrid=False,
                  height = 500,
                  legend=dict(
                    orientation="h",
                    yanchor="bottom", y=1.02,
                    xanchor="right", x=1),
                  title={
                    'text': "Count of COVID19 Tweets Sentiment Wise per day",
                    'y':0.95, 'x':0.5,
                    'xanchor': 'center', 'yanchor': 'top'},
                  font=dict(
                    family='Raleway, sans-serif',
                    size = 15,
                    color="RebeccaPurple"),
                  )
    fig.update_xaxes(showline=False, linewidth=2,showticklabels=False,
                    #ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=10,
                    showgrid = False, zeroline=False, row=1, col=1)
    fig.update_xaxes(showline=False, linewidth=2,showticklabels=False,
                    #ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=10,
                    showgrid = False, zeroline=False, row=2, col=1)
    fig.update_xaxes(showline=True, linewidth=2,
                    ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=10,
                    title_text='Date', title_standoff=10, matches='x',
                    showgrid = False, zeroline=False, row=3, col=1)
    fig.update_yaxes(showline=True, linewidth=2,
                    ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=20,
                    showgrid=False, zeroline=False, row=1, col=1)
    fig.update_yaxes(showline=True, linewidth=2,
                    ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=20,
                    showgrid=False, zeroline=False, row=2, col=1)
    fig.update_yaxes(showline=True, linewidth=2,
                    ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=20,
                    showgrid=False, zeroline=False, row=3, col=1)
    return dcc.Graph(
        id="daywiseplot", responsive=True,
        figure = fig)

def generate_totplot():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_day['date'], y =df_day['tot'],
                            mode='lines+markers',
                            connectgaps=True, marker_color='rgb(135,44,162)'
                            )
    )

    fig.update_layout(template='plotly_dark',
                  #paper_bgcolor='rgba(0,0,0,0)',
                  #plot_bgcolor='rgba(0,0,0,0)',
                  xaxis_showgrid=False,
                  yaxis_showgrid=False,
                  font=dict(
                    family='Raleway, sans-serif',
                    size = 15,
                    color="RebeccaPurple"),
                  title={
                    'text': "Total Count of COVID19 Tweets per day",
                    'y':0.95, 'x':0.5,
                    'xanchor': 'center', 'yanchor': 'top'}
                  )
    fig.update_xaxes(showline=True, linewidth=2,
                    ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=10,
                    title_text='Date', title_standoff=10,
                    #rangeslider_visible=True
                    )
    fig.update_yaxes(showline=True, linewidth=2,
                    ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=20,
                    title_text='Count of COVID-19 realted tweets', title_standoff=25)
    #fig.update_xaxes(rangeslider_visible=True)

    #fig.update_layout(xaxis_range=['2020-03-21',])
    return dcc.Graph(
        id="totplot", responsive=True,
        figure = fig)

def generate_scoreplot():
    df = df_day
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y = df['avg'],
                            mode='lines+markers',
                            connectgaps=True, marker_color='rgb(135,44,162)'))
    fig.update_layout(template='plotly_dark',
                  #paper_bgcolor='rgba(0,0,0,0)',
                  #plot_bgcolor='rgba(0,0,0,0)',
                  xaxis_showgrid=False,
                  yaxis_showgrid=False,
                  font=dict(
                    family='Raleway, sans-serif',
                    size = 15,
                    color="RebeccaPurple"),
                  title={
                    'text': "Sentiment Score of COVID19 Tweets per day",
                    'y':0.95, 'x':0.5,
                    'xanchor': 'center', 'yanchor': 'top'}
                  )
    fig.update_xaxes(showline=True, linewidth=2,
                    ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=10,
                    title_text='Date', title_standoff=15,
                    rangeslider_visible=True)
    fig.update_yaxes(showline=True, linewidth=2,
                    ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=20,
                    title_text='Sentiment Score', title_standoff=25,
                    zeroline=True, zerolinewidth=2, zerolinecolor='Red')

    return dcc.Graph(
        id="scoreplot", responsive=True,
        figure = fig)

def generate_barplot():
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_phase['phase'], y=df_phase['neg'],
        name='Negative Tweets',
        marker_color='rgb(244,59,44)'
    ))
    fig.add_trace(go.Bar(
        x=df_phase['phase'], y=df_phase['pos'],
        name='Positive Tweets',
        marker_color='rgb(35,132,67)'
    ))
    fig.add_trace(go.Bar(
        x=df_phase['phase'], y=df_phase['neut'],
        name='Neutral Tweets',
        marker_color='rgb(62,83,160)'
    ))

    fig.update_layout(template='plotly_dark',
                  #paper_bgcolor='rgba(0,0,0,0)',
                  #plot_bgcolor='rgba(0,0,0,0)',
                  barmode='group', xaxis_tickangle=-45,
                  xaxis_showgrid=False,
                  yaxis_showgrid=False,
                  height = 800,
                  legend=dict(
                    orientation="h",
                    yanchor="bottom", y=1.02,
                    xanchor="right", x=1),
                  title={
                    'text': "Count of COVID19 Tweets Sentiment Wise per Phase",
                    'y':0.95, 'x':0.5,
                    'xanchor': 'center', 'yanchor': 'top'},
                  font=dict(
                    family='Raleway, sans-serif',
                    size = 15,
                    color="RebeccaPurple"),
                  )
    fig.update_xaxes(showline=True, linewidth=2,
                    title_text='Phase', title_standoff=10,
                    #rangeslider_visible=True
                    )
    fig.update_yaxes(showline=True, linewidth=2,
                    ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=20,
                    title_text='Count of COVID-19 tweets', title_standoff=25)
    #fig.update_xaxes(rangeslider_visible=True)

    #fig.update_layout(xaxis_range=['2020-03-21',])
    return dcc.Graph(
        id="barplot", responsive=True,
        figure = fig)

def generate_c1plot():
    df = df_phase
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['phase'], y = df['avg'],
                            mode='lines+markers',
                            connectgaps=True, marker_color='rgb(135,44,162)'))
    fig.update_layout(template='plotly_dark',
                  #paper_bgcolor='rgba(0,0,0,0)',
                  #plot_bgcolor='rgba(0,0,0,0)',
                  xaxis_showgrid=False,
                  yaxis_showgrid=False,
                  font=dict(
                    family='Raleway, sans-serif',
                    size = 15,
                    color="RebeccaPurple"),
                  title={
                    'text': "Sentiment Score of COVID19 Tweets Phase-wise",
                    'y':0.95, 'x':0.5,
                    'xanchor': 'center', 'yanchor': 'top'}
                  )
    fig.update_xaxes(showline=True, linewidth=2,
                    ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=10, tickangle=-45,
                    title_text='Phase', title_standoff=15,
                    rangeslider_visible=False)
    fig.update_yaxes(showline=True, linewidth=2,
                    ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=20,
                    title_text='Sentiment Score', title_standoff=25,
                    zeroline=True, zerolinewidth=2, zerolinecolor='Red')

    return dcc.Graph(
        id="c1plot", responsive=True,
        figure = fig)

def generate_c2plot():
    df = df_phase
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['phase'], y = df['p/n'],
                            mode='lines+markers',
                            connectgaps=True, marker_color='rgb(135,44,162)'))
    fig.update_layout(template='plotly_dark',
                  #paper_bgcolor='rgba(0,0,0,0)',
                  #plot_bgcolor='rgba(0,0,0,0)',
                  xaxis_showgrid=False,
                  yaxis_showgrid=False,
                  font=dict(
                    family='Raleway, sans-serif',
                    size = 15,
                    color="RebeccaPurple"),
                  title={
                    'text': "P/N Ratio Phase-wise",
                    'y':0.95, 'x':0.5,
                    'xanchor': 'center', 'yanchor': 'top'}
                  )
    fig.update_xaxes(showline=True, linewidth=2,
                    ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=10, tickangle=-45,
                    title_text='Phase', title_standoff=15,
                    rangeslider_visible=False)
    fig.update_yaxes(showline=True, linewidth=2,
                    ticks="outside", tickwidth=2, tickcolor='crimson', ticklen=20,
                    title_text='P/N Ratio', title_standoff=25,
                    zeroline=True, zerolinewidth=2, zerolinecolor='Red')

    return dcc.Graph(
        id="c2plot", responsive=True,
        figure = fig)



def build_tab_1():
    return [
        # day wise statistics
        html.Div(
            id='daywiseplot',
            className='daywiseplot',
            children=[
                html.Div(
                    className="row",
                    children=[
                        # Column for user controls
                        html.Div(
                            className="four columns div-user-controls",
                            children=[
                                html.H2("SINGLE DAY SUMMARY"),
                                html.P(
                                    """Select a particular day using the date picker
                                    for viewing specific summary and statistics."""
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        dcc.DatePickerSingle(
                                            id="date-picker",
                                            min_date_allowed=dt(2020, 3, 21),
                                            max_date_allowed=dt(2020, 7, 12),
                                            initial_visible_month=dt(2020, 3, 21),
                                            date=dt(2020, 3, 21).date(),
                                            display_format="MMMM D, YYYY",
                                            style={"border": "0px solid black"}
                                        )
                                    ]
                                )
                            ]
                        ),
                        # Column for app graphs and plots
                        html.Div(
                            className="eight columns div-for-charts bg-grey",
                            children=[
                                dcc.Graph(id='piechart', responsive=True),
                                html.Div(id='daystats', className='daystats')
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='totplot',
                    children=[generate_totplot()]
                    ),
                html.Div(
                    className='daywiseplot',
                    children=[generate_daywiseplot()]
                    ),
                html.Div(
                    className='scoreplot',
                    children=[generate_scoreplot()]
                    )
            ]
        )
    ]

def build_tab_2():
    return [
        # day wise statistics
        html.Div(
            id='phasewiseplot',
            className='phasewiseplot',
            children=[
                html.Div(
                    className="row",
                    children=[
                        # Column for user controls
                        html.Div(
                            className="four columns div-user-controls",
                            children=[
                                html.H2("SINGLE PHASE SUMMARY"),
                                html.P(
                                    """Select a particular phase using the dropdown
                                    for viewing specific summary and statistics."""
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        dcc.Dropdown(
                                            id="phase-dropdown",
                                            options=[
                                                {"label": i, "value": j}
                                                for (i,j) in zip(phases, vals)
                                            ],
                                            value=0,
                                            placeholder="Select a Phase",
                                            clearable=False
                                        )
                                    ]
                                )
                            ]
                        ),
                        # Column for app graphs and plots
                        html.Div(
                            className="eight columns div-for-charts bg-grey",
                            children=[
                                dcc.Graph(id="pie-graph", className='pie-graph'),
                                html.Div(id='phasestats', className='phasestats')
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='barplot',
                    children=[generate_barplot()]
                    ),
                html.Div(
                    className='row', id='twoplots',
                    children=[
                        html.Div(
                            className='six columns',
                            children=[
                                html.Div(className='c1',
                                    children=[html.H3('Sentiment Score Phase-wise')]),
                                generate_c1plot()
                            ]),
                        html.Div(
                            className='six columns',
                            children=[
                                html.Div(className='c2',
                                    children=[html.H3('P/N Ratio Phase-wise')]),
                                generate_c2plot()
                            ])
                    ])
            ])
    ]

def generate_modal():
    return html.Div(
        id="markdown",
        className="modal",
        children=(
            html.Div(
                id="markdown-container",
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=html.Button(
                            "Close",
                            id="markdown_close",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),
                    html.Div(
                        className="markdown-text",
                        children=dcc.Markdown(
                            children=(
                                """
                        #### **ABOUT PROJECT**

                        This is a dashboard for monitoring sentiment of COVID19 related tweets. It is a webapp built using [dash](https://plotly.com/dash/). This project is hosted [here](https://github.com/SmartPracticeschool/SBSPS-Challenge-4564-Sentiment-Analysis-Dashboard-of-COVID-19-tweets). One can build it locally also by cloning the repository.

                        > ###### This project is part of [**IBM HACK CHALLENGE 2020**](https://smartinternz.com/ibm-hack-challenge-2020).

                        ###### How to Use:
                        * Phases in app means various phases of lockdown exercised as mentioned [here]().
                        * p/n ratio denotes count of positive tweets per negative tweet.
                        * You may encounter following abbreviations:
                            * pos stands for Positive
                            * neg stands for Negative
                            * neut stands for Neutral


                        ###### Following issues still exist with the project (sorry for your inconvenience):
                        * Due to inavailability of twitter API, this does not updates in real time and data is taken from web.
                        * As there is no automated script yet, this app would be updated per week manually.
                        * This app is not fully responsive yet for all the screen sizes.

                        > ###### Data Source: Data used in the app can be found [here](https://ieee-dataport.org/open-access/coronavirus-covid-19-tweets-dataset). It is processed using [these scripts](https://github.com/SmartPracticeschool/SBSPS-Challenge-4564-Sentiment-Analysis-Dashboard-of-COVID-19-tweets/tree/master/data_preprocessing).

                        #### Connect with me:
                        * [**Github**](https://github.com/avats-dev)
                        * [**LinkedIn**](https://www.linkedin.com/in/avats-dev/)
                        * [**Gmail**](mailto:avats.dev@gmail.com)

                        > _**Feel free to drop feedback and suggestions !!**_

                    """
                            )
                        ),
                    ),
                ],
            )
        ),
    )



app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
        #dcc.Store(id="value-setter-store", data=init_value_setter_store()),
        dcc.Store(id="n-interval-stage", data=50),
        generate_modal(),
    ],
)


# ======= Callbacks for modal popup =======
@app.callback(
    Output("markdown", "style"),
    [Input("learn-more-button", "n_clicks"), Input("markdown_close", "n_clicks")],
)
def update_click_output(button_click, close_click):
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "learn-more-button":
            return {"display": "block"}

    return {"display": "none"}


# callback for tab selection
@app.callback(
    [Output("app-content", "children")],
    [Input("app-tabs", "value")]
)
def render_tab_content(tab_switch):
    if tab_switch == "tab1":
        return build_tab_1()
    return build_tab_2()


# Update piechart day
@app.callback(
    output=Output("piechart", "figure"),
    inputs=[Input("date-picker", "date")]
)
def update_piechart_d(sdate):
    df = df_day
    sdate = sdate
    #sdate = dt.strptime(sdate, '%d/%m/%Y').date()
    df = df[(df['date']==str(sdate))]
    p = df.iloc[0].pos
    n = df.iloc[0].neg
    nt = df.iloc[0].neut
    labels = ['Positive Tweets', 'Negative Tweets', 'Neutral Tweets']
    values = [p, n, nt]

    tdate = dt.strptime(sdate, '%Y-%m-%d').date()
    tdate = tdate.strftime("%d-%b-%Y")
    title = 'Statistics of ' + tdate
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                             insidetextorientation='radial',
                             marker_colors=['rgb(35,132,67)', 'rgb(244,59,44)', 'rgb(62,83,160)']
                            )])

    fig.update_traces(textposition='inside')
    fig.update_layout(template='plotly_dark',
                  #paper_bgcolor='rgba(0,0,0,0)',
                  #plot_bgcolor='rgba(0,0,0,0)',
                  #xaxis_showgrid=False,
                  #yaxis_showgrid=False,
                  font=dict(
                    family='Raleway, sans-serif',
                    size = 15,
                    color="RebeccaPurple"),
                  title={
                    'text': title,
                    'y':0.95, 'x':0.5,
                    'xanchor': 'center', 'yanchor': 'top'}
                  )
    fig.update_layout(margin=dict(t=80, b=20, l=0, r=0))

    return fig


# show day stats
@app.callback(
    output=Output("daystats", "children"),
    inputs=[Input("date-picker", "date")]
)
def update_dstats(sdate):
    df = df_day
    sdate = sdate
    #sdate = dt.strptime(sdate, '%d/%m/%Y').date()
    df = df[(df['date']==str(sdate))]
    p = df.iloc[0].pos
    n = df.iloc[0].neg
    nt = df.iloc[0].neut
    av = df.iloc[0].avg
    pn = df.iloc[0]['p/n']*1000

    tdate = dt.strptime(sdate, '%Y-%m-%d').date()
    tdate = tdate.strftime("%d-%b-%Y")
    title = 'Statistics of ' + tdate

    return [
        html.H3(title),
        html.P('Total count of positive tweets on ' + tdate + ' : ' + str(p)),
        html.P('Total count of negative tweets on ' + tdate + ' : ' + str(n)),
        html.P('Total count of neutral tweets on ' + tdate + ' : ' + str(nt)),
        html.P('Average Sentiment Score of tweets on ' + tdate + ' : ' + str(av)),
        html.P('Total positive tweets per 1k negative tweets on ' + tdate + ' : ' + str(round(pn)))
    ]

# update piechart phase
@app.callback(
    output=Output("pie-graph", "figure"),
    inputs=[Input("phase-dropdown", "value")]
)
def update_piechart_p(val):
    df = df_phase
    filter = [False, False, False, False, False, False]
    filter[val]=True
    sphase = phases[val]
    #sdate = dt.strptime(sdate, '%d/%m/%Y').date()
    df = df.loc[filter]
    p = df.iloc[0].pos
    n = df.iloc[0].neg
    nt = df.iloc[0].neut
    labels = ['Positive Tweets', 'Negative Tweets', 'Neutral Tweets']
    values = [p, n, nt]

    title = 'Statistics of ' + sphase
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                             insidetextorientation='radial',
                             marker_colors=['rgb(35,132,67)', 'rgb(244,59,44)', 'rgb(62,83,160)']
                            )])

    fig.update_traces(textposition='inside')
    fig.update_layout(template='plotly_dark',
                  #paper_bgcolor='rgba(0,0,0,0)',
                  #plot_bgcolor='rgba(0,0,0,0)',
                  #xaxis_showgrid=False,
                  #yaxis_showgrid=False,
                  font=dict(
                    family='Raleway, sans-serif',
                    size = 15,
                    color="RebeccaPurple"),
                  title={
                    'text': title,
                    'y':0.95, 'x':0.5,
                    'xanchor': 'center', 'yanchor': 'top'}
                  )
    fig.update_layout(margin=dict(t=80, b=20, l=0, r=0))

    return fig

def date2str(sdate):
    #tdate = dt.strptime(sdate, '%Y-%m-%d').date()
    tdate = sdate.strftime("%d-%b-%Y")
    return tdate

# show phase stats
@app.callback(
    output=Output("phasestats", "children"),
    inputs=[Input("phase-dropdown", "value")]
)
def update_pstats(val):
    df = df_phase
    filter = [False, False, False, False, False, False]
    filter[val]=True
    sphase = phases[val]
    df = df.loc[filter]

    p = df.iloc[0].pos
    n = df.iloc[0].neg
    nt = df.iloc[0].neut
    av = df.iloc[0].avg
    dp = df.iloc[0]['date_mpos']
    dn = df.iloc[0]['date_mneg']
    pn = df.iloc[0]['p/n']*1000
    st = df.iloc[0].start
    ed = df.iloc[0].end
    drn = ed-st
    #dt.strptime(ed, '%Y-%m-%d').date() - dt.strptime(st, '%Y-%m-%d').date()

    dp = date2str(dp)
    dn = date2str(dn)
    st = date2str(st)
    ed = date2str(ed)
    title = 'Statistics of ' + sphase

    return [
        html.H3(title),
        html.P('The ' + sphase + ' started on : ' + st + ' and ended on : ' + ed),
        html.P('Total duration of ' + sphase + ' : ' + str(drn)),
        #html.P('Total count of positive tweets in ' + sphase + ' : ' + str(p)),
        #html.P('Total count of negative tweets in ' + sphase + ' : ' + str(n)),
        #html.P('Total count of neutral tweets in ' + sphase + ' : ' + str(nt)),
        html.P('Average Sentiment Score of tweets in ' + sphase + ' : ' + str(av)),
        html.P('Total positive tweets per 1k negative tweets in ' + sphase + ' : ' + str(round(pn))),
        html.P('Date with highest p/n ratio in ' + sphase + ' : ' + dp),
        html.P('Date with lowest p/n ratio in ' + sphase + ' : ' + dn)
    ]


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
