import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import pickle

# Load the figures
keys_to_exclude = {'fig16', 'fig17', 'fig18', 'fig19'}

with open('figs.pkl', 'rb') as f:
    figs = {k: v for k, v in pickle.load(f).items() if k not in keys_to_exclude}

with open('figs1.pkl', 'rb') as f:
    figs1 = {k: v for k, v in pickle.load(f).items() if k not in keys_to_exclude}

with open('figs2.pkl', 'rb') as f:
    figs2 = {k: v for k, v in pickle.load(f).items() if k not in keys_to_exclude}

with open('figs3.pkl', 'rb') as f:
    figs3 = {k: v for k, v in pickle.load(f).items() if k not in keys_to_exclude}

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ])

# Define the layout of the app
app.layout = html.Div(style={'backgroundColor': '#f2f2f2'}, children=[
    dbc.Container([
        dbc.Row([
            html.Div([
                html.H1(children="Análise de dados Google analytics", style={'fontSize': '20px'}),
                dcc.Dropdown(
                    id='figs-dropdown',
                    options=[
                        {'label': 'figs', 'value': 'figs'},
                        {'label': 'figs1', 'value': 'figs1'},
                        {'label': 'figs2', 'value': 'figs2'},
                        {'label': 'figs3', 'value': 'figs3'}
                    ],
                    value='figs'
                ),
            ]),
        ], style={'margin': '20px 0'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='figs-display-1'), width=6),
            dbc.Col(dcc.Graph(id='figs-display-2'), width=6),   
        ], style={'margin': '20px 0'}),
    ])
])
# Create a list to store the dbc.Col components
cols = []

# Create a list to store the callback functions
callbacks = []

# Loop over the range of figures
for i in range(16):
    # Create the dbc.Col component
    cols.append(dbc.Col(dcc.Graph(id=f'figs-display-{i}'), width=6))

    # Create the callback function
    @app.callback(
        Output(f'figs-display-{i}', 'figure'),
        Input('figs-dropdown', 'value')
    )
    def update_figure(selected_value, i=i):  # Use default argument to capture the current value of i
        print(f"Updating figure {i} with value: {selected_value}")
        if selected_value == 'figs':
            fig = figs[f'fig{i}']
        elif selected_value == 'figs1':
            fig = figs1[f'fig{i}']
        elif selected_value == 'figs2':
            fig = figs2[f'fig{i}']
        elif selected_value == 'figs3':
            fig = figs3[f'fig{i}']

        # Modify the layout of the figure
        fig.update_layout(
            height=450,  # Increase the height of the graph
            xaxis=dict(
                tickangle=45  # Rotate the x-axis labels to 45 degrees
            )
        )

        return fig

    # Add the callback function to the list
    callbacks.append(update_figure)

# Add the dbc.Col components to the layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div([
            html.H1(children="Google analytics data analysis", style={'fontSize': '25px'}),
            html.H2(children="Project phases", style={'fontSize': '18px', 'color': 'white'}),
            html.H3(children="Data capture and cleaning", style={'fontSize': '13px', 'color': 'white'}),
            html.H3(children="Exploratory data analysis", style={'fontSize': '13px', 'color': 'white', }),
            html.H3(children="Data modeling - PCA - Kmeans Clustering", style={'fontSize': '13px', 'color': 'white'}),
            html.H3(children="Dashboard - Insights", style={'fontSize': '13px', 'color': 'white'}),
            dcc.Dropdown(
                id='figs-dropdown',
                options=[
                    {'label': 'cluster_0', 'value': 'figs'},
                    {'label': 'cluster_1', 'value': 'figs1'},
                    {'label': 'cluster_2', 'value': 'figs2'},
                    {'label': 'cluster_3', 'value': 'figs3'}
                ],
                value='figs'
            ),
        ]),
    ], style={'margin': '20px 0'}),
    dbc.Row(cols, style={'margin': '20px 0'}),
])


# Run the server
if __name__ == '__main__':
    app.run_server(debug=False, port=8051)

