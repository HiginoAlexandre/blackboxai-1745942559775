import pandas as pd
from models.livro import Livro
from models.venda import Venda
from app import db

def gerar_relatorio_vendas_mensais():
    vendas = Venda.query.all()
    data = [{
        'data_venda': venda.data_venda,
        'quantidade': venda.quantidade,
        'total': venda.quantidade * venda.preco_unitario,
        'categoria': venda.livro.categoria
    } for venda in vendas]

    df = pd.DataFrame(data)
    if df.empty:
        return pd.DataFrame()

    df['mes'] = df['data_venda'].dt.to_period('M')
    relatorio = df.groupby(['mes', 'categoria']).agg({'quantidade': 'sum', 'total': 'sum'}).reset_index()
    return relatorio

def gerar_relatorio_discrepancias():
    livros = Livro.query.all()
    data = []
    for livro in livros:
        vendas = sum(v.quantidade for v in livro.vendas)
        estoque_calculado = livro.quantidade + vendas
        discrepancia = estoque_calculado - livro.quantidade
        data.append({
            'livro': livro.titulo,
            'estoque_calculado': estoque_calculado,
            'estoque_fisico': livro.quantidade,
            'discrepancia': discrepancia
        })
    df = pd.DataFrame(data)
    return df
