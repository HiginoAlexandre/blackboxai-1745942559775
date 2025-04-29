from flask import Blueprint, render_template
from flask_login import login_required
from utils.reports import gerar_relatorio_vendas_mensais, gerar_relatorio_discrepancias
import json

analise_bp = Blueprint('analise', __name__, url_prefix='/analise')

@analise_bp.route('/')
@login_required
def dashboard_analise():
    relatorio_vendas = gerar_relatorio_vendas_mensais()
    relatorio_discrepancias = gerar_relatorio_discrepancias()

    vendas_json = relatorio_vendas.to_json(orient='records')
    discrepancias_json = relatorio_discrepancias.to_json(orient='records')

    return render_template('analise.html', vendas_data=vendas_json, discrepancias_data=discrepancias_json)
