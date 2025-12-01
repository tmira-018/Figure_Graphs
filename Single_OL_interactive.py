
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import numpy as np



app = Dash(__name__)

# ------------------------------------------------------------------------------------
# Import Data


# Load data, this is the original dataframe with cell age 
cellage_path = ('/Users/miramota/Desktop/Graphs/DataSheets/WIN_single_cell.xlsx')
cellage_df = pd.read_excel(cellage_path)


#--------------------------------------------------------------------------------------

# App Layout
app.layout = html.Div([
    html.H1('Myelin Sheath Analysis', style = {'text-align': 'center'}),
    dcc.Dropdown( id= 'select_cond',
                 options = [
                     {'label': 'DMSO', 'value': 0.0},
                     {'label':'WIN 1.0', 'value': 1.0},
                     {'label': 'BOTH', 'value': 'both'}],
                     multi = False,
                     value = 'both',
                     clearable = False,
                     style = {'width': '40%'}),
                    
    html.Div(id = 'output_container', children = []),
    html.Br(),
    html.Div([
        dcc.Graph(id = 'avg_sheath_graph', figure={},
              style = {'width': '80%', 'display':'inline-block', 'padding': '0 10'}),
        
        dcc.Graph(id = 'no_sheaths_graph', figure={},
                  style = {'width': '80%', 'display': 'inline-block', 'padding': '0 10'}),
        
        dcc.Graph(id = 'total_output_graph', figure={},
                  style = {'width': '80%', 'display':'inline-block', 'padding': '0 10'})
    ])
])

#--------------------------------------------------------------------------------------
# Connect Plotly graphs with Dash Components
@app.callback(
    [Output(component_id = 'output_container', component_property = 'children'),
     Output(component_id = 'avg_sheath_graph', component_property = 'figure'),
     Output(component_id = 'no_sheaths_graph', component_property = 'figure'),
     Output(component_id = 'total_output_graph', component_property = 'figure')],
     [Input(component_id = 'select_cond', component_property = 'value')]
)

def update_graph(option_selected):
    print(option_selected)
    print(type(option_selected))

    container= 'Condition chosen: {}'.format(option_selected)

    df2 = cellage_df.copy()
    df2 = df2[df2.cond != 0.5]

    if option_selected != 'both':
        df2 = df2[df2['cond'] == option_selected]
    df2 = df2.dropna(subset=['avg_sheath_len'])

    color_by = 'cond' if option_selected == 'both' else 'cell_ID'

    #Plotly Express
    avg_sheath = px.line(df2.dropna(subset=['avg_sheath_len']), 
                x = 'cell_age', y = 'avg_sheath_len',
                color = color_by, markers= True,
                hover_data = {'cell_ID': True,
                                'avg_sheath_len': True,
                                'cell_age': False,
                                'cond': False},
                color_discrete_map = {0.0: '#1768AC', 1.0: '#F72585'},
                labels = {'cell_age': 'Cell Age (days)',
                          'avg_sheath_len': 'Average Sheath Length (µm)'}
                )
    avg_sheath.update_layout(title= 'Average Sheath Length',
                             xaxis = dict(showline = True,
                                          showgrid = False,
                                          linecolor = 'black',
                                          linewidth = 2, 
                                          tickvals = np.arange(1,5,1)),
                            yaxis = dict(showline = True,
                                         showgrid = False,
                                         linecolor= 'black',
                                         linewidth = 2),
                            plot_bgcolor = 'white'
                            )

    no_sheaths = px.line(df2.dropna(subset=['no_sheaths']),
                         x = 'cell_age', y = 'no_sheaths',
                         color = color_by, markers = True,
                            hover_data = {'cell_ID': True,
                                        'no_sheaths': True,
                                        'cell_age': False,
                                        'cond': False},
                        color_discrete_map = {0.0: '#1768AC', 1.0: '#F72585'},
                        labels = {'cell_age': 'Cell Age (days)',
                                  'no_sheaths': 'Number of Sheaths per Cell'})
    no_sheaths.update_layout(title = 'Number of Sheaths per Cell',
                             xaxis = dict(showline = True,
                                          showgrid = False,
                                          linecolor = 'black',
                                          linewidth = 2,
                                          tickvals = np.arange(1,5,1)),
                            yaxis = dict(showline = True,
                                         showgrid = False,
                                         linecolor= 'black',
                                         linewidth = 2),
                            plot_bgcolor = 'white')
    
    total_output = px.line(df2.dropna(subset=['total_output']),
                            x = 'cell_age', y = 'total_output',
                            color = color_by, markers = True,
                                hover_data = {'cell_ID': True,
                                            'total_output': True,
                                            'cell_age': False,
                                            'cond': False},
                            color_discrete_map = {0.0: '#1768AC', 1.0: '#F72585'},
                            labels= {'cell_age': 'Cell Age (days)',
                                     'total_output': 'Total Myelin Output (µm)'})
    total_output.update_layout(title= 'Total Myelin Output',
                             xaxis = dict(showline = True,
                                          showgrid = False,
                                          linecolor = 'black',
                                          linewidth = 2,
                                          tickvals = np.arange(1,5,1)),
                            yaxis = dict(showline = True,
                                         showgrid = False,
                                         linecolor= 'black',
                                         linewidth = 2),
                            plot_bgcolor = 'white')
    
    

    return container, avg_sheath, no_sheaths, total_output
    
#--------------------------------------------------------------------------------------
# Run the app
if __name__ == '__main__':
    app.run(debug=True)