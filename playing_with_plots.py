# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

# US States list for random generation
states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

# random product names
product_names = ["Skateboard Max 1", "Skateboard Max 2",
    "Unicycle Pro GX", "Unicycle Beginners", "BMX Top GX"
]


# create DataFrame with random values for cols above -n rows
n_rows = 1000
data = pd.DataFrame(
    data={ # add date ordered
        'product_name':np.random.choice(product_names,size=n_rows),
        'state':np.random.choice(states,size=n_rows),
        'units_sold':np.random.randint(1,5,n_rows),
        'sales_revenue':np.random.uniform(0,1000,n_rows), # this number doesn't make sense, it's just an example. No prices set for each product :)
        'shipping_fees':np.random.uniform(0,30,n_rows) # this number doesn't make sense, it's just an example :)
    }
)

# DataFrame columns shown in barplot
show_cols = ['units_sold','sales_revenue',
    'shipping_fees'] 
    
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1(
            children="Monthly Results per Product",
            style={
                "textAlign": "center",
            }
        ),
        html.Div(
            children="Playing with random data :)",
            style={
                "textAlign": "center",
            }
        ),
        html.Div([
            dcc.Dropdown(
                id="feature",
                options=[
                    {'label': 'State', 'value': 'state'},
                    {'label': 'Product Name', 'value': 'product_name'},
                ],
                value='product_name'
            ),
            dcc.Checklist(
                id="dollar-values",
                options=[
                    {
                        'label': val.replace("_"," ").capitalize(),
                        'value': val
                        } for val in show_cols
                ],
                value=[show_cols[0]],
                labelStyle={'display': 'inline-block'}
            )
        ]),  
        ### Interactive bar plot: sales revenue (or others) per: state or day or parent or child
        dcc.Graph(id="results-barplot")
        ### add dropdowns before graph
    ]
)
@app.callback(
    Output("results-barplot","figure"),
    [Input("feature","value"),
    Input("dollar-values","value")]
)
def update_figure(selected_feature,dollar_values):
    
    summary_month = data.groupby(selected_feature)\
        .sum()\
        .loc[:,dollar_values]\
        .round(2)

    figure={
        "data": [
            {"x":summary_month.index,
            "y":summary_month.iloc[:,i],
            "type":"bar",
            "name":summary_month.iloc[:,i].name
            } for i in range(len(summary_month.columns))
        ],
        'layout': { # experiment with the layout
        'title': 'Monthly Report-Results per {}'.format(selected_feature)
        }
    }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)