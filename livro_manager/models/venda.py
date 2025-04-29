from app import db
from datetime import datetime

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    livro_id = db.Column(db.Integer, db.ForeignKey('livro.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    total_pago = db.Column(db.Float, nullable=False)
    saldo = db.Column(db.Float, nullable=False)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)
    cliente = db.Column(db.String(100))
    parcelas = db.Column(db.Integer, default=1)
    pagamentos = db.relationship('Pagamento', backref='venda', lazy=True)

    def calcular_total(self):
        return self.quantidade * self.preco_unitario

    def atualizar_saldo(self, valor_pago):
        self.total_pago += valor_pago
        self.saldo = self.calcular_total() - self.total_pago
        db.session.commit()

class Pagamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey('venda.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data_pagamento = db.Column(db.DateTime, default=datetime.utcnow)
