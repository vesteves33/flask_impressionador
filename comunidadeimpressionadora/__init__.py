from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '927ea2480ff5dc69d53bcde9b80c18d16db4e959c9ab8917259f66c2d9067de3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_projeto'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)
loginManager.login_view = 'login'
loginManager.login_message_category = 'alert-info'

#Não esquecer de importar arquivos que no processo de reorganização deixaram de ser executados
#essa importação precisa ter o 'app' criado, por isso está embaixo
from comunidadeimpressionadora import route
