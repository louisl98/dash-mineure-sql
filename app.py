# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import psycopg2
import plotly.express as px

# database
def getprovinces():
    try:
        connection = psycopg2.connect(host="ec2-46-137-177-160.eu-west-1.compute.amazonaws.com", database="dbntjps2ogiaoe", user="jqwpptjnjyvaqw", password="cb6d58e6c0a9e078767b32777fe990054d317a029116a89fd35a8a29e974dcfc")
        # declare a cursor
        cur = connection.cursor()
        # get cities
        cur.execute("SELECT * FROM corona")
        provinces = cur.fetchall()
        # # get cities ordered by date
        # cur.execute('SELECT * FROM corona ORDER BY "Last Update" DESC')
        # provincesByDate = cur.fetchall()
        # close the communication with the PostgreSQL
        # get cities outside China
        cur.execute("SELECT * FROM corona WHERE \"Country/Region\" != 'Mainland China'")
        cities = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
    return provinces, cities
        

# front-end
provinces = getprovinces()[0]
# provincesByDate = getprovinces()[1]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
data = []
data2 = []
provinces.remove(provinces[0])
for i in range(len(provinces)): 
    data.append({'x': [provinces[i][0]], 'y': [provinces[i][3]], 'type': 'bar', 'width': [0.8], 'name': provinces[i][0]})
cities = getprovinces()[1]
for i in range(len(cities)): 
    data2.append({'x': [cities[i][1]], 'y': [cities[i][3]], 'type': 'bar', 'width': [0.8], 'name': cities[i][1]})
# dates = []
# infected = []
# for i in range(len(provincesByDate)): 
#     dates.append(provinces[i][2])
#     infected.append(provinces[i][3])
app.layout = html.Div(children=[
    html.H1(children='SQL for dataviz'),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': data,
            'layout': {
                'title': 'Nombre d\'infectés hors de la province de Hubei, Chine'
            }
        }
    ),
    dcc.Graph(
        id='examplee-graph',
        figure={
            'data': data2,
            'layout': {
                'title': 'Nombre d\'infectés hors de Chine'
            }
        }
    )
#     dcc.Graph(
#     figure=dict(
#         data=[
#             dict(
#                 x=dates,
#                 y=infected,
#                 name='Rest of world',
#                 marker=dict(
#                     color='rgb(55, 83, 109)'
#                 )
#             )
#         ],
#         layout=dict(
#             title='US Export of Plastic Scrap',
#             showlegend=True,
#             legend=dict(
#                 x=0,
#                 y=1.0
#             ),
#             margin=dict(l=40, r=0, t=40, b=30)
#         )
#     ),
#     style={'height': 300},
#     id='my-graph'
# )  
])
if __name__ == '__main__':
    app.run_server(debug=True)