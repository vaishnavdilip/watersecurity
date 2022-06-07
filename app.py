import dash
#import dash_html_components as html
from dash import html
#import dash_core_components as dcc
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from plotly.subplots import make_subplots

import plotly.graph_objects as go
import numpy as np

from waterUESI import cluster_neighbors, cluster_waterStress, cities_df

app = dash.Dash(__name__,title='Water Security',external_stylesheets=[dbc.themes.BOOTSTRAP],serve_locally = False)

# add this for heroku
server = app.server

#Chart
fig = make_subplots(rows=1, cols=1)
fig.add_trace(
    go.Scatter(x=np.arange(0,10,1),
               y=np.arange(0,10,1)*2 + np.random.randn(),
               name='Example'),
    row=1, col=1)
fig.update_layout(width=1500)

# City Options
dropdown = dcc.Dropdown(
        id='id_cities',
        options=[
            {'label':i, 'value':i} for i in cities_df['c'].unique()
        ],
    value='bogota')

# Start Date,  End Date & Number of Mixtures
input_groups = dbc.Row(dbc.Col(html.Div(dropdown)))

app.layout = dbc.Container(
    [
        html.Div(children=[html.H1(children='Water Security')],
                 style={'textAlign':'center','color':'black'}),
        html.Hr(),
        html.P('The Urban Environment Social Inclusion Index (UESI) Data which is a research effort to provide the data that urban residents, city managers, and policymakers need to understand their cities’ performance on critical urban environmental issues.The UESI data might help us identify how cities are similar to each other in urban terms, including water stress. Therefore, we use unsupervised learning techniques to analyse how cities tend to form groups and how the water stress behaves in those groups. We thus have two visualizations. The first one allows to chose a city and shows the closest cities in the city cluster according tho the principal components. The second shows the distribution of water stress in the city cluster and highlights the city’s water stress as well as some reference points to asses its current situation.'),
        dbc.Row(
            [
                dbc.Col(input_groups, md=2),
                dbc.Col(dcc.Graph(id="id_scatter",figure=fig), md=10),
                dbc.Col(dcc.Graph(id="id_density",figure=fig), md=10),
            ],
            align="center",
        ),
    ],
    fluid=True,
)

@app.callback(
    Output('id_scatter','figure'),
    Output('id_density','figure'),
    [
     Input('id_cities','value')
     ]
)
def update_chart(city):
 
    params = {}
    params['city']=city
    scatter = cluster_neighbors(params)
    density = cluster_waterStress(params)

    return scatter, density


if __name__ == '__main__':
    app.run_server(debug=True)