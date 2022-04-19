import numpy as np
import plotly.express as px, pandas as pd

class noTearsDict(dict):
    def __missing__(self, key):
        return key
lbls = {'TC':'Time of Concentration (Hrs)','R':'Storage Coefficient (Hrs)','A':'Subbasin Area (SqMi)','imp':'Percent Impervious (%)','nm':'Subbasin Name',
    'n':"Manning's N",
'basin_slope': 'Basin Slope (Ft/Mi)',
    '10_85_slope': '10-85 Slope (Ft/Mi)',
    'elongation_ratio': 'Elongation Ratio',
    'longest_length': 'Longest Length (Mi)'}
lbls = noTearsDict(lbls)
def relabelDA(DA):
    return DA.rename(columns=lbls)

    
def scatta(DF,x,y,ctrl=None,h=700,w=700,colorscale='plasma'):
    '''lbls, relabelDA all hardcoded here'''
    plotTitle = f'<b>{lbls[x]} vs<br>{lbls[y]}</b>'
    # print(plotTitle)

    if ctrl:
        fixd = [xi for xi in ctrl.keys() if xi!=x]
        qry = DF.query(' & '.join( [f'`{fx}`=={ctrl[fx]}' for fx in fixd] ))
    else:
        qry = DF

    data = relabelDA(qry.reset_index()[[x,y]])
    data[[lbls[x],lbls[y]]]=data[[lbls[x],lbls[y]]].astype(float)
    data['i']=np.arange(len(data))
    # data[lbls['nm']] = data[lbls['nm']].map(intifyStr)
    # print(data)

    # slp = np.polyfit(data[lbls[x]],data[lbls[y]],1)

    # X,Y = data[lbls[x]],data[lbls[y]]
    # trendy = lambda x: x*slp[0]+slp[1]
    # trendin = [(X.min(),trendy(X.min())),(X.max(),trendy(X.max()))]
    
    fig = px.scatter(relabelDA(qry),x=lbls[x],y=lbls[y],
        color=lbls[y],color_continuous_scale=colorscale,
        width=w,height=h,title=plotTitle,
        trendline='ols',trendline_color_override="black")
    # fig.layout.showlegend = False 
    fig.update_coloraxes(showscale=False)
    fig.update_layout(title_x=0.5)
    if x!='n':
        fig.update_yaxes(
                            scaleanchor = "x",
                            scaleratio = 1,
                        )
    return fig