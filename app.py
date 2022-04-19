import dash
# from dash import Input, Output, State
try:
    import dash_core_components as dcc
    import dash_html_components as html
except:
    from dash import dcc
    from dash import html
try:
    import dash_bootstrap_components as dbc
except:
    from dash import dbc
import numpy as np
import pandas as pd
import matplotlib as mpl
import gunicorn                     #whilst your local machine's webserver doesn't need this, Heroku's linux webserver (i.e. dyno) does. I.e. This is your HTTP server
from whitenoise import WhiteNoise   #for serving static files on Heroku
from itertools import product
import plotly.tools as tls
try:
    from .ftbend import *
    from .plawter import *
except:
    from ftbend import *
    from plawter import *

#construct dataframe-----------

S = np.array([ 2,  8, 12, 16, 47])
S0 = np.array([109, 204, 242, 284, 531])
L = np.array([0.5,1,4,5,15])
N = np.array([0.035, 0.05 , 0.07 , 0.09 , 0.1  , 0.12 , 0.15 , 0.3  , 0.4  ])
I = np.append(np.arange(0,5),[20,40,100])

runz = np.array(np.meshgrid(L,S,N,S0,I)).T.reshape(-1,5)
from functools import reduce
assert len(runz)==reduce(lambda x,y:x*len(y),[len(L),S,N,S0,I])

bend = lambda a:ftbend._TCR(*a)
tcr=np.apply_along_axis(bend,1,runz)
df = pd.DataFrame(np.concatenate([runz,tcr],axis=1),columns=['longest_length','10_85_slope','n','basin_slope','imp','TC','R'])

#create plots
xx=df.columns.to_list()[:-2]
yy = ['TC','R']

# x,y = 'n','TC'

# fig = tls.make_subplots(rows=len(xx)/2, cols=2,
#  shared_xaxes=False,shared_yaxes=False,
#  vertical_spacing=0.009,horizontal_spacing=0.009)



# [
#     html.Div(
#         dcc.Graph(figure=
#             scatta(df,df.iloc[0],xx,x,y)
#         )
#     ,id=f'{x}v{y}'
#     ,style={'display': 'inline-block'} )
#         for x,y in product(xx,yy) 
#         ]


# Instantiate dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG] ) 

# Define the underlying flask app (Used by gunicorn webserver in Heroku production deployment)
server = app.server 

# Enable Whitenoise for serving static files from Heroku (the /static folder is seen as root by Heroku) 
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/') 

# Define Dash layout
def create_dash_layout(app):

    # Set browser tab title
    app.title = "Ft Bend County TC&R Equation Sensitivity Analysis" #browser tab
    
        
    #create dropdowns
    drops = [html.H3('Default fixed parameters'),'Compare the sensitivity of each parameter while the rest remain fixed to the below defaults']+[
        dcc.Dropdown(options=[{'label': f'{lbls[x]}: {v}', 'value': v} for v in df[x].unique()], value=df[x].iloc[0], id=f'drop{x}')
            for x in xx]

    plawts = html.Div(children=[],id='plawts')

    # Header
    header = html.Div([html.Br(), dcc.Markdown(""" # Ft Bend County TC&R Equation Sensitivity Analysis"""), html.Br()])
    
    # Body 
    body = html.Div(drops+[plawts])
    # Footer
    # footer = html.Div([html.Br(), html.Br(), dcc.Markdown(""" ### Built with ![Image](heart.png) in Python using [Dash](https://plotly.com/dash/)""")])
    
    # Assemble dash layout 
    app.layout = html.Div([header, plawts])

    # @app.callback(
    # Output(f'plawts', "children"),
    # [Input(f'drop{x}', f'val{x}') for x in xx]
    # )
    # def refix(*args):
    #     ctrl =  dict(zip(xx,args))
    #     sctrs = [
    #         html.Div(
    #             dcc.Graph(figure=
    #                 scatta(df,ctrl,xx,x,y)
    #             )
    #         ,id=f'{x}v{y}'
    #         ,style={'display': 'inline-block'} )
    #             for x,y in product(xx,yy) ]
    #     return sctrs


    return app

# Construct the dash layout
create_dash_layout(app)

# Run flask app
if __name__ == "__main__": app.run_server(debug=False, host='0.0.0.0', port=8050)
