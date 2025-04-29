from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models.livro import Livro

estoque_bp = Blueprint('estoque', __name__, url_prefix='/estoque')

def admin_required():
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash('Acesso negado.', 'danger')
        return False
    return True

@estoque_bp.route('/')
@login_required
def listar_estoque():
    livros = Livro.query.all()
    return render_template('estoque.html', livros=livros)

@estoque_bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_livro():
    if not admin_required():
        return redirect(url_for('estoque.listar_estoque'))

    if request.method == 'POST':
        titulo = request.form['titulo']
        quantidade = int(request.form['quantidade'])
        preco = float(request.form['preco'])
        categoria = request.form['categoria']
        idioma = request.form['idioma']

        if quantidade < 0 or preco < 0:
            flash('Quantidade e preço não podem ser negativos.', 'danger')
            return redirect(url_for('estoque.adicionar_livro'))

        novo_livro = Livro(titulo=titulo, quantidade=quantidade, preco=preco,
                          categoria=categoria, idioma=idioma)
        db.session.add(novo_livro)
        db.session.commit()
        flash('Livro adicionado com sucesso.', 'success')
        return redirect(url_for('estoque.listar_estoque'))

    return render_template('adicionar_livro.html')

@estoque_bp.route('/editar/<int:livro_id>', methods=['GET', 'POST'])
@login_required
def editar_livro(livro_id):
    if not admin_required():
        return redirect(url_for('estoque.listar_estoque'))

    livro = Livro.query.get_or_404(livro_id)

    if request.method == 'POST':
        livro.titulo = request.form['titulo']
        quantidade = int(request.form['quantidade'])
        preco = float(request.form['preco'])
        if quantidade < 0 or preco < 0:
            flash('Quantidade e preço não podem ser negativos.', 'danger')
            return redirect(url_for('estoque.editar_livro', livro_id=livro_id))
        livro.quantidade = quantidade
        livro.preco = preco
        livro.categoria = request.form['categoria']
        livro.idioma = request.form['idioma']

        db.session.commit()
        flash('Livro atualizado com sucesso.', 'success')
        return redirect(url_for('estoque.listar_estoque'))

    return render_template('editar_livro.html', livro=livro)

@estoque_bp.route('/excluir/<int:livro_id>', methods=['POST'])
@login_required
def excluir_livro(livro_id):
    if not admin_required():
        return redirect(url_for('estoque.listar_estoque'))

    livro = Livro.query.get_or_404(livro_id)
    db.session.delete(livro)
    db.session.commit()
    flash('Livro excluído com sucesso.', 'success')
    return redirect(url_for('estoque.listar_estoque'))
