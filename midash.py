import pandas as pd
import numpy as np
import plotly.graph_objs as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Generamos valores aleatorios
valores = np.random.randint(0, 1001, size=1000)

# Creamos una serie de booleanos para indicar los VP y FP
vp = (valores >= 500) & (valores >= 200)
fp = ~vp
 
# Creamos el DataFrame
df = pd.DataFrame({'Valor': valores, 'VP': vp, 'FP': fp})

# Inicializamos la aplicación Dash
app = dash.Dash(__name__)

# Creamos el layout de la aplicación
app.layout = html.Div([
    dcc.Graph(id='grafica'),
    html.Div([
        dcc.Slider(
            id='slider',
            min=0,
            max=1000,
            value=500,
            marks={i: str(i) for i in range(0, 1001, 100)}
        )
    ]),
    html.Div([
        dcc.Dropdown(
            id='tipo-grafico',
            options=[
                {'label': 'Gráfico de Barras', 'value': 'bar'},
                {'label': 'Gráfico de Puntos', 'value': 'scatter'}
            ],
            value='bar'
        )
    ])
])

# Función para calcular la tasa de reducción y la tasa de riesgo
def calcular_tasas(df):
    total = len(df)
    count_vp = df['VP'].sum()
    count_fp = df['FP'].sum()
    reduccion = (count_fp / total) * 100
    riesgo = (count_vp / total) * 100
    return reduccion, riesgo

# Definimos la callback para actualizar la gráfica
@app.callback(
    Output('grafica', 'figure'),
    [Input('slider', 'value'),
     Input('tipo-grafico', 'value')]
)
def update_graph(slider_value, tipo_grafico):
    filtered_df = df[df['Valor'] <= slider_value]
    count_vp = filtered_df['VP'].sum()
    count_fp = filtered_df['FP'].sum()
    
    reduccion, riesgo = calcular_tasas(filtered_df)
    
    if tipo_grafico == 'bar':
        data = [
            go.Bar(
                x=['VP'],
                y=[count_vp],
                name='VP',
                text=str(count_vp),
                textposition='auto',
                marker=dict(color='rgb(26, 118, 255)')
            ),
            go.Bar(
                x=['FP'],
                y=[count_fp],
                name='FP',
                text=str(count_fp),
                textposition='auto',
                marker=dict(color='rgb(255, 65, 54)')
            )
        ]
    else:
        data = [
            go.Scatter(
                x=filtered_df[filtered_df['VP']]['Valor'],
                y=[1] * count_vp,
                mode='markers',
                name='VP',
                text=str(filtered_df[filtered_df['VP']]['Valor']),
                marker=dict(color='rgb(26, 118, 255)')
            ),
            go.Scatter(
                x=filtered_df[filtered_df['FP']]['Valor'],
                y=[1] * count_fp,
                mode='markers',
                name='FP',
                text=str(filtered_df[filtered_df['FP']]['Valor']),
                marker=dict(color='rgb(255, 65, 54)')
            )
        ]

    layout = go.Layout(
        title=f'Cantidad de VP y FP con valor menor o igual a {slider_value}',
        xaxis=dict(title='Tipo'),
        yaxis=dict(title='Cantidad'),
        bargap=0.1,
        bargroupgap=0.1,
        annotations=[
            dict(
                x=0.5,
                y=1.1,
                xref='paper',
                yref='paper',
                text=f'Reducción: {reduccion:.2f}% | Riesgo: {riesgo:.2f}%',
                showarrow=False,
                font=dict(size=12)
            )
        ]
    )

    return {'data': data, 'layout': layout}

# Ejecutamos la aplicación
if __name__ == '__main__':
    app.run_server(debug=False)
