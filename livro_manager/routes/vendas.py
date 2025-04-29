from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models.venda import Venda, Pagamento
from models.livro import Livro
from datetime import datetime

vendas_bp = Blueprint('vendas', __name__, url_prefix='/vendas')

def admin_or_funcionario_required():
    if not current_user.is_authenticated or current_user.role not in ['admin', 'usuario']:
        flash('Acesso negado.', 'danger')
        return False
    return True

@vendas_bp.route('/')
@login_required
def listar_vendas():
    vendas = Venda.query.order_by(Venda.data_venda.desc()).all()
    return render_template('vendas.html', vendas=vendas)

@vendas_bp.route('/registrar', methods=['GET', 'POST'])
@login_required
def registrar_venda():
    if not admin_or_funcionario_required():
        return redirect(url_for('vendas.listar_vendas'))

    livros = Livro.query.all()

    if request.method == 'POST':
        livro_id = int(request.form['livro_id'])
        quantidade = int(request.form['quantidade'])
        preco_unitario = float(request.form['preco_unitario'])
        cliente = request.form['cliente']
        parcelas = int(request.form.get('parcelas', 1))
        valor_pago = float(request.form.get('valor_pago', 0))

        livro = Livro.query.get_or_404(livro_id)

        if quantidade <= 0 or preco_unitario < 0:
            flash('Quantidade deve ser positiva e preço não pode ser negativo.', 'danger')
            return redirect(url_for('vendas.registrar_venda'))

        if livro.quantidade < quantidade:
            flash('Estoque insuficiente para esta venda.', 'danger')
            return redirect(url_for('vendas.registrar_venda'))

        total_venda = quantidade * preco_unitario
        saldo = total_venda - valor_pago

        venda = Venda(
            livro_id=livro_id,
            quantidade=quantidade,
            preco_unitario=preco_unitario,
            total_pago=valor_pago,
            saldo=saldo,
            cliente=cliente,
            parcelas=parcelas,
            data_venda=datetime.utcnow()
        )
        db.session.add(venda)

        # Atualizar estoque
        livro.atualizar_estoque(quantidade)

        # Registrar pagamento inicial se valor_pago > 0
        if valor_pago > 0:
            pagamento = Pagamento(
                venda=venda,
                valor=valor_pago,
                data_pagamento=datetime.utcnow()
            )
            db.session.add(pagamento)

        db.session.commit()
        flash('Venda registrada com sucesso.', 'success')
        return redirect(url_for('vendas.listar_vendas'))

    return render_template('registrar_venda.html', livros=livros)
