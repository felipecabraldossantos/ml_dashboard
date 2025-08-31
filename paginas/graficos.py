from ucimlrepo import fetch_ucirepo
import plotly.express as px
from dash import dcc, html
import dash_bootstrap_components as dbc

heart_disease = fetch_ucirepo(id=45)
dados = heart_disease.data.features

dados['doenca'] = 1 * (heart_disease.data.targets > 0)

fig_hist = px.histogram(
    dados, x='age', nbins=30, 
    title='Distribuição Etária (Plotly)', color='doenca'
)
fig_hist.update_layout(xaxis_title='Idade', yaxis_title='Frequência')

fig_box = px.box(
    dados, x='doenca', y='age', 
    title='Distribuição Etária por Doença', color='doenca'
)
fig_box.update_layout(xaxis_title='Diagnóstico (0 = não | 1 = sim)', yaxis_title='Idade')

layout = html.Div([
    html.H1('Análise de Dados - Doença Cardíaca', 
            className='text-center mb-4 custom-subtitle'),
    
    dbc.Container([
        dbc.Row([
            dbc.Col([dcc.Graph(figure=fig_hist)], md=7),
            dbc.Col([dcc.Graph(figure=fig_box)], md=5)
        ])
    ])
])
