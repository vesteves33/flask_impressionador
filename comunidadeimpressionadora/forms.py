from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import PasswordField, StringField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user


class CriarConta(FlaskForm):
    nome = StringField('Nome do usuario', validators=[DataRequired(), Length(3, 20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 12)])
    confirmaSenha = PasswordField('Confirmação de senha', validators=[DataRequired(), EqualTo('senha')])
    botaoCriarConta = SubmitField('Criar conta')
    
    #Lib FlaskForm permite criar validações desde que a função comece com 'validate_'
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()       
        if usuario:
            raise ValidationError('E-mail já existe. Use outro email ou tente fazer login')  
    

class Login(FlaskForm):    
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 12)])
    lembrarDados = BooleanField('Lembrar-me')
    botaoLogin = SubmitField('Login')
    

class EditarPerfil(FlaskForm):
    nome = StringField('Nome do usuario', validators=[DataRequired(), Length(3, 20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    fotoPerfil = FileField('Atualizar', validators=[ FileAllowed(['jpg', 'png'])] )
    cursoExcel = BooleanField('Excel')
    cursoVBA = BooleanField('VBA')
    cursoPython = BooleanField('Python')
    cursoSQL = BooleanField('SQL')
    cursoPowerBI = BooleanField('PowerBI')
    cursoPPT = BooleanField('Apresentações')
    cursoDefault = BooleanField('Não informado')
    botaoEditarPerfil = SubmitField('Salvar mudanças')
    
    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()       
            if usuario:
                raise ValidationError('Já existe um usuário com esse email. Cadastre outro email')
            
            
class CriarPost(FlaskForm):
    titulo = StringField('Título do post', validators=[DataRequired(), Length(5, 50)])
    post = TextAreaField('Descrição do post', validators=[DataRequired()])
    botaoPostar = SubmitField('Publicar')