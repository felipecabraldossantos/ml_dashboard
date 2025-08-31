from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from paginas import graficos, formulario
from app import app

navegacao = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink('Gráficos', href='/graficos')),
        dbc.NavItem(dbc.NavLink('Formulário', href='/formulario')),
    ],
    brand='Dashboard - Unoesc',
    brand_href='/',
    color='primary',
    dark=True
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navegacao,
    html.Div(id='conteudo')
])

@app.callback(
    Output('conteudo', 'children'),
    [Input('url', 'pathname')]
)
def mostrar_pagina(pathname):
    if pathname == '/formulario':
        return formulario.layout
    elif pathname == '/graficos':
        return graficos.layout
    else:
        return html.H2('Página Inicial - Bem-vindo ao Dashboard!')

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
