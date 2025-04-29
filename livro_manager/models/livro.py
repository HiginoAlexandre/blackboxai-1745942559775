from app import db

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    quantidade = db.Column(db.Integer, default=0)
    preco = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50))
    idioma = db.Column(db.String(2))  # Ex: 'PT', 'EN'

    vendas = db.relationship('Venda', backref='livro', lazy=True)

    def atualizar_estoque(self, quantidade_vendida):
        if self.quantidade >= quantidade_vendida:
            self.quantidade -= quantidade_vendida
            db.session.commit()
        else:
            raise ValueError("Estoque insuficiente.")
