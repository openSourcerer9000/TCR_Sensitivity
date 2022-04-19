import dash
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
xx = ['longest_length', '10_85_slope', 'n', 'basin_slope', 'imp']
yy = ['TC','R']

x,y = 'n','TC'

fig = scatta(df,df.iloc[0],xx,x,y)

#create dropdowns
drops = [
    dcc.Dropdown(options=[{'label': f'{lbls[x]}: {v}', 'value': v} for v in df[x].unique()], value=df[x].iloc[0], id=f'drop{x}')
        for x in xx]

# Instantiate dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY] ) 

# Define the underlying flask app (Used by gunicorn webserver in Heroku production deployment)
server = app.server 

# Enable Whitenoise for serving static files from Heroku (the /static folder is seen as root by Heroku) 
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/') 

# Define Dash layout
def create_dash_layout(app):

    # Set browser tab title
    app.title = "Your app title" #browser tab
    
    # Header
    header = html.Div([html.Br(), dcc.Markdown(""" # Ft Bend County TC&R Equation Sensitivity Analysis"""), html.Br()])
    
    # Body 
    body = html.Div(
        drops+
        [
        dcc.Graph(figure=fig)])
    # Footer
    # footer = html.Div([html.Br(), html.Br(), dcc.Markdown(""" ### Built with ![Image](heart.png) in Python using [Dash](https://plotly.com/dash/)""")])
    
    # Assemble dash layout 
    app.layout = html.Div([header, body])

    return app

# Construct the dash layout
create_dash_layout(app)

# Run flask app
if __name__ == "__main__": app.run_server(debug=False, host='0.0.0.0', port=8050)
