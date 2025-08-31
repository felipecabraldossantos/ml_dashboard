from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import joblib
import pandas as pd
from app import app

modelo = joblib.load('modelo_xgboost.pkl')
medianas = joblib.load('medianas.pkl')

col_esquerda = dbc.Col([
    dbc.Label('Idade'),
    dbc.Input(id='idade', type='number', placeholder='Digite a idade'),

    dbc.Label('Sexo biológico'),
    dbc.Select(id='sexo', options=[
        {'label': 'Masculino', 'value': '1'},
        {'label': 'Feminino', 'value': '0'}
    ]),

    dbc.Label('Tipo de dor no peito'),
    dbc.Select(id='cp', options=[
        {'label': 'Angina típica', 'value': 0},
        {'label': 'Angina atípica', 'value': 1},
        {'label': 'Dor não anginosa', 'value': 2},
        {'label': 'Assintomático', 'value': 3},
    ]),

    dbc.Label('Pressão arterial em repouso'),
    dbc.Input(id='trestbps', type='number', placeholder='Digite a pressão'),

    dbc.Label('Colesterol sérico'),
    dbc.Input(id='chol', type='number', placeholder='Digite o colesterol'),

    dbc.Label('Glicemia em jejum'),
    dbc.Select(id='fbs', options=[
        {'label': '≤ 120 mg/dl', 'value': 0},
        {'label': '> 120 mg/dl', 'value': 1}
    ]),

    dbc.Label('Eletrocardiografia em repouso'),
    dbc.Select(id='restecg', options=[
        {'label': 'Normal', 'value': 0},
        {'label': 'Anormalidade ST-T', 'value': 1},
        {'label': 'Hipertrofia ventricular', 'value': 2}
    ]),
], md=6)

col_direita = dbc.Col([
    dbc.Label('Frequência cardíaca máxima atingida'),
    dbc.Input(id='thalach', type='number', placeholder='Digite a frequência'),

    dbc.Label('Angina induzida por exercício'),
    dbc.Select(id='exang', options=[
        {'label': 'Não', 'value': 0},
        {'label': 'Sim', 'value': 1}
    ]),

    dbc.Label('Depressão do segmento ST induzida por exercício'),
    dbc.Input(id='oldpeak', type='number', placeholder='Digite o valor'),

    dbc.Label('Inclinação do segmento ST'),
    dbc.Select(id='slope', options=[
        {'label': 'Ascendente', 'value': 0},
        {'label': 'Plano', 'value': 1},
        {'label': 'Descendente', 'value': 2}
    ]),

    dbc.Label('Nº de vasos principais coloridos por fluoroscopia'),
    dbc.Select(id='ca', options=[
        {'label': '0', 'value': 0},
        {'label': '1', 'value': 1},
        {'label': '2', 'value': 2},
        {'label': '3', 'value': 3}
    ]),

    dbc.Label('Cintilografia do miocárdio'),
    dbc.Select(id='thal', options=[
        {'label': 'Normal', 'value': 1},
        {'label': 'Defeito fixo', 'value': 2},
        {'label': 'Defeito reversível', 'value': 3}
    ]),

    dbc.Button('Prever', id='botao-prever', color='success', className='mt-3')
], md=6)

layout = html.Div([
    html.H3('Preencha as informações abaixo e clique no botão "Prever" para executar o modelo',
            className='text-center mb-4 custom-subtitle'),
    
    dbc.Row([col_esquerda, col_direita], className='g-3'),
    html.Div(id='previsao')
])

@app.callback(
    Output('previsao', 'children'),
    [Input('botao-prever', 'n_clicks')],
    [
        State('idade', 'value'),
        State('sexo', 'value'),
        State('cp', 'value'),
        State('trestbps', 'value'),
        State('chol', 'value'),
        State('fbs', 'value'),
        State('restecg', 'value'),
        State('thalach', 'value'),
        State('exang', 'value'),
        State('oldpeak', 'value'),
        State('slope', 'value'),
        State('ca', 'value'),
        State('thal', 'value')
    ]
)
def prever_doenca(n_clicks, idade, sexo, cp, trestbps, chol, fbs, restecg,
                  thalach, exang, oldpeak, slope, ca, thal):
    if not n_clicks:
        return ''

    entradas_usuario = pd.DataFrame([[idade, sexo, cp, trestbps, chol, fbs, restecg,
                                      thalach, exang, oldpeak, slope, ca, thal]],
                                    columns=['age','sex','cp','trestbps','chol','fbs','restecg',
                                             'thalach','exang','oldpeak','slope','ca','thal'])

    #rever essa parte
    entradas_usuario = entradas_usuario.fillna(medianas).infer_objects(copy=False)
    entradas_usuario = entradas_usuario.apply(pd.to_numeric, errors='coerce')

    entradas_usuario = entradas_usuario.infer_objects(copy=False)

    entradas_usuario = entradas_usuario.apply(pd.to_numeric, errors='coerce')

    previsao = modelo.predict(entradas_usuario)[0]
    if previsao == 1:
        return dbc.Alert("Você tem risco de doença cardíaca!", color="danger", className="mt-3")
    else:
        return dbc.Alert("Você não tem risco de doença cardíaca!", color="success", className="mt-3")
