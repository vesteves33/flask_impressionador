from flask import render_template, request, url_for, flash, redirect, abort
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import Login, CriarConta, EditarPerfil, CriarPost
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image

@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    
    
    return render_template('home.html', posts=posts)

@app.route('/contato')
def contato():    
    return render_template('contato.html')

@app.route('/usuarios')
@login_required
def usuarios():
    listaUsuarios = Usuario.query.all()
    return render_template('usuarios.html', listaUsuarios=listaUsuarios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    criarConta = CriarConta()
    login = Login()
    
    if login.validate_on_submit() and 'botaoLogin' in request.form:
        usuario = Usuario.query.filter_by(email=login.email.data).first()
        
        if usuario and bcrypt.check_password_hash(usuario.senha, login.senha.data):
            login_user(usuario, remember=login.lembrarDados.data)
            flash(f'Login feito com sucesso, para o email: {login.email.data}', 'alert-success')
            parametroNext = request.args.get('next')
            
            if parametroNext:
                return redirect(parametroNext)
            else:
                return redirect(url_for('home'))
        else:
            flash('Falha ao tentar realizar login,E-mail ou Senha incorreto tente novamente', 'alert-danger')
        
    if criarConta.validate_on_submit() and 'botaoCriarConta' in request.form:
        senhaHash = bcrypt.generate_password_hash(criarConta.senha.data)
        usuario = Usuario(nome=criarConta.nome.data, email=criarConta.email.data, senha=senhaHash)
        database.session.add(usuario)
        database.session.commit()
        
        flash(f'Conta criada com sucesso, para o email: {criarConta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    
    return render_template('login.html', criarConta=criarConta, login=login)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout feito com sucesso!', 'alert-success')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    fotoPerfil = url_for('static', filename='img/{}'.format(current_user.fotoPerfil))
    
    
    return render_template('perfil.html', fotoPerfil=fotoPerfil)

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criarPost():
    criarPost = CriarPost()
    
    if criarPost.validate_on_submit():
        post = Post(titulo=criarPost.titulo.data, corpo=criarPost.post.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post publicado com sucesso!', 'alert-success')
        return redirect(url_for('home'))
    
    return render_template('criarpost.html', criarPost=criarPost)


def salvarImagem(imagem):
    #renomeando foto evitar duplicidade de arquivo
    hashFoto = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nomeFotoCompleta = nome + hashFoto + extensao
    caminhoDiretorioImg = os.path.join(app.root_path, 'static/img', nomeFotoCompleta)
    
    #compactar a imagem
    tamanho = (200, 200)
    imagemReduzida = Image.open(imagem)
    imagemReduzida.thumbnail(tamanho)

    #salvar nova imagem na aplicação
    imagemReduzida.save(caminhoDiretorioImg)
    return nomeFotoCompleta
    
def atualizarCursos(formulario):
    listaCursos = []
    
    for campo in formulario:
        if 'curso' in campo.name:
            if campo.data:
                listaCursos.append(campo.label.text)
    
    return ';'.join(listaCursos)
    
@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editarPerfil():
    editarPerfil = EditarPerfil()   
    
    if editarPerfil.validate_on_submit():
        current_user.email = editarPerfil.email.data
        current_user.nome = editarPerfil.nome.data
        if editarPerfil.fotoPerfil.data:
            novaFoto = salvarImagem(editarPerfil.fotoPerfil.data)
            current_user.fotoPerfil = novaFoto
            
        current_user.cursos = atualizarCursos(editarPerfil)     
        database.session.commit()
        flash('Perfil atualizado com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        editarPerfil.nome.data = current_user.nome
        editarPerfil.email.data = current_user.email
    
    
    
    fotoPerfil = url_for('static', filename='img/{}'.format(current_user.fotoPerfil))
    return render_template('editarperfil.html', fotoPerfil=fotoPerfil, editarPerfil=editarPerfil)

@app.route('/post/<idPost>', methods=['GET', 'POST'])
@login_required
def exibirPost(idPost):
    post = Post.query.get(idPost)
    if current_user == post.autor:
        editarPost = CriarPost()
        if request.method == 'GET':
            editarPost.titulo.data = post.titulo
            editarPost.post.data = post.corpo
        elif editarPost.validate_on_submit():
            post.titulo = editarPost.titulo.data
            post.corpo = editarPost.post.data
            database.session.commit()
            flash('Post atualizado com sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        editarPost = None
    
    return render_template('post.html', post=post, editarPost=editarPost)


@app.route('/post/<idPost>/excluir', methods=['GET', 'POST'])
@login_required
def excluirPost(idPost):
    post = Post.query.get(idPost)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        
        flash('Post excluido com sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)