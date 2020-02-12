# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import psycopg2

# database
def getprovinces():
    try:
        connection = psycopg2.connect(host="ec2-46-137-177-160.eu-west-1.compute.amazonaws.com", database="dbntjps2ogiaoe", user="jqwpptjnjyvaqw", password="cb6d58e6c0a9e078767b32777fe990054d317a029116a89fd35a8a29e974dcfc")
        # declare a cursor
        cur = connection.cursor()
        # get cities
        cur.execute("SELECT * FROM corona")
        provinces = cur.fetchall()
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
    return provinces
        

# front-end
provinces = getprovinces()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
data = []
for i in range(len(provinces)): 
    data.append({'x': [provinces[i][0]], 'y': [provinces[i][3]], 'type': 'Pie', 'name': provinces[i][0]})
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': data,
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])
if __name__ == '__main__':
    app.run_server(debug=True)