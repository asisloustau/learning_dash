import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1(["Factors calculator - Enter a Number"]),
    dcc.Input(id="num", type="number",debounce=True,min=1,step=1),
    html.P(id="error", style={"color":"red"}), # case prime number
    html.P(id="output")
])

@app.callback(
    [Output("output","children"), Output("error","children")],
    [Input("num","value")]
)

def show_result(num):
    if num is None:
        raise dash.exceptions.PreventUpdate # prevent update when input blank
    
    factors = list()
    for val in range(2,num):
        divided = num
        while divided % val == 0: # this will let us show same prime factor several times if applicable
            factors.append(str(val))
            divided = divided / val
    if len(factors) >= 1:
        return "Number {} = {}".format(str(num)," * ".join(factors)), None
    else:
        return None, "Number {} is a prime number".format(str(num))


app.run_server(debug=True)