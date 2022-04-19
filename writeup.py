try:
    import dash_core_components as dcc
    import dash_html_components as html
except:
    from dash import dcc
    from dash import html

writeup = html.Div([html.H5('Observations'),
'''
TC values for subbasins with a longest flowpath of 1 Mi or less, and reasonable manning's N of 0.12 or less produce familiar TC values within the realm of a couple of hours. With flowpath lengths of as long as 15 Mi for the Whisky Chitto watershed, more extreme TC and R values may still be realistic. The equation is very sensitive to Manning's N. While Manning's values of 0.12 may produce reasonable results, it could be recommended to refine Manning's N regions within the channel, at a finer resolution than what is provided by National Land Cover Database (NLCD).
''',html.Br(),html.Br(),'''
Example values were chosen to loosely approximate the minimum, maximum, and quartile values found within the Whisky Chitto watershed. Manning's N analyzed were taken from the Dewberry 2019 Amite Study lookup table to NLCD land cover, with extreme values 0.3 and 0.4 added. The TC vs R correlation is only dependent on basin slope, so this is the only fixed parameter in the final, TC vs R plot. All results are derived simply from the above equation, not the results of any HEC-HMS simulations.
'''],style={'padding':f'1.5em 5%'})