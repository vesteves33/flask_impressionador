from comunidadeimpressionadora import database, loginManager
from datetime import datetime
from flask_login import UserMixin

@loginManager.user_loader
def loadUsuario(idUsuario):
    return Usuario.query.get(int(idUsuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    fotoPerfil = database.Column(database.String, default='default.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True)
    cursos = database.Column(database.String, nullable=False, default='Não informado')

    def contarPost(self):
        return len(self.posts)
    
class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    dataCriacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)   
    idUsuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)