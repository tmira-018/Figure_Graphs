
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback_context
import numpy as np

##
# Plot function
def myelin_line_plot(df, column):
    single_cell_fig = px.line(df,
                    x = 'cell_age', y = column,
                    markers = True,
                    hover_data = {'cell_ID': False,
                                column: True,
                                'cell_age': True,
                                'cond': False})
    single_cell_fig.update_layout(title = f'{column} across cell age',
                    xaxis = dict(showline = True,
                                 showgrid= False,
                                 linecolor= 'black',
                                 linewidth = 2,
                                 tickvals = np.arange(1,4,1)),
                    yaxis = dict(showline = True,
                                         showgrid = False,
                                         linecolor= 'black',
                                         linewidth = 2),
                    plot_bgcolor = 'white')
    return single_cell_fig

app = Dash(__name__)

# --------------------------------------------------------------------------------------
# Import data


path = ('/Users/miramota/Desktop/Graphs/DataSheets/WIN_single_cell.xlsx')
ol_df = pd.read_excel(path)

ol_analysis= ol_df[ol_df['cell_ID'].map(ol_df['cell_ID'].value_counts()) > 1]

#removes cells that were treated with 0.5 um WIN and cell age 4
ol_analysis2 = ol_df[ol_df.cond != 0.5]
ol_analysis2 = ol_analysis2[ol_analysis2.cell_age != 4]
ol_analysis2 = ol_analysis2.dropna(subset=['aberrant'])


ol_analysis3 = ol_analysis2[ol_analysis2['cell_ID'].map(ol_analysis2['cell_ID'].value_counts()) == 3]   
ol_analysis3['aberrant_bool'] = (ol_analysis3['aberrant']>=1).astype(int)


#pivot table used for heatmap
dmso_ol_analysis = ol_analysis3[ol_analysis3['cond'] == 0.0]
win_ol_analysis = ol_analysis3[ol_analysis3['cond'] == 1.0]
dmso_pivot = dmso_ol_analysis.pivot_table(index='cell_ID', 
                                           columns='cell_age', 
                                           values='aberrant')
win_pivot = win_ol_analysis.pivot_table(index='cell_ID',
                                        columns = 'cell_age',
                                        values = 'aberrant')



dmso_fig = px.imshow(dmso_pivot,
                labels = dict(x = 'Cell Age', y = 'Cell ID', color = 'Non-axonal Ensheathments'),
                x = dmso_pivot.columns,
                y = dmso_pivot.index)

win_fig = px.imshow(win_pivot,
                    labels = dict(x = 'Cell Age', y = 'Cell ID', color = 'Non-axonal Ensheathments'),
                    x = win_pivot.columns,
                    y = win_pivot.index)

#--------------------------------------------------------------------------------------

# App Layout
app.layout = html.Div([
    html.H1('Non-axonal Ensheathments', style = {'text-align': 'center'}),
                    
    html.Div(id = 'output_container', children = []),
    html.Br(),
    html.Div([
        dcc.Graph(id = 'dmso_heatmap_graph', figure = dmso_fig),
        dcc.Graph(id = 'win_heatmap_graph', figure=win_fig)],
        style = {'width':'49%','display': 'flex', 'align-items': 'center'}),
        
    html.Div([
        dcc.Graph(id = 'avg_sheath_graph', figure ={}),
        dcc.Graph(id = 'no_sheaths_graph', figure = {}),
        dcc.Graph(id = 'total_output_graph', figure = {}),], 
        style = {'width': '20%', 'display':'flex', 'align-items': 'center', 'flex-direction': 'row'})
])

#--------------------------------------------------------------------------------------
# Connect Plotly graphs with Dash Components
@app.callback(
    [Output(component_id = 'avg_sheath_graph', component_property = 'figure'),
     Output(component_id = 'no_sheaths_graph', component_property = 'figure'),
     Output(component_id = 'total_output_graph', component_property = 'figure')],
    [Input(component_id = 'dmso_heatmap_graph', component_property = 'clickData'),
     Input('win_heatmap_graph', component_property='clickData')]
)


def update_graph(dmso_click, win_click):
    ctx = callback_context
    if not ctx.triggered:
        # No clicks yet, return empty figures
        return {}, {}, {}

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    print(f"Triggered by: {trigger_id}")
    print(f"DMSO click: {dmso_click}")
    print(f"WIN click: {win_click}")

    if trigger_id == 'dmso_heatmap_graph' and dmso_click:
        cell_id = dmso_click['points'][0]['y']
        condition = 0.0
    elif trigger_id == 'win_heatmap_graph' and win_click:
        cell_id = win_click['points'][0]['y']
        condition = 1.0
    else:
        return {}, {}, {}

    
    single_cell_data = ol_analysis3[ol_analysis3['cell_ID'] == cell_id].dropna(subset = ['avg_sheath_len'])

    no_sheaths_fig = myelin_line_plot(single_cell_data, 'no_sheaths')
    avg_sheath_len_fig = myelin_line_plot(single_cell_data, 'avg_sheath_len')
    total_output_fig = myelin_line_plot(single_cell_data, 'total_output')
    
    return no_sheaths_fig, avg_sheath_len_fig, total_output_fig



#--------------------------------------------------------------------------------------
# Run the app
if __name__ == '__main__':
    app.run(debug=True)