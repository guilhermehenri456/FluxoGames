from flask import Flask, render_template, request, redirect, url_for, flash, session
from sqlalchemy.exc import SQLAlchemyError
from models import local_secao, Empresa, Genero, Jogador, Jogo, Plataforma, Personagem, Jogo_Genero, Jogo_Jogador, Categoria
from sqlalchemy import select
from datetime import datetime  # Importação essencial para a data de nascimento

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Renderiza a página inicial/login e processa a verificação de credenciais."""

    if request.method == 'POST':
        email = request.form.get('email')
        # Nome do campo conforme seu login.html: name="password"
        senha_digitada = request.form.get('password')

        sessao = local_secao()
        jogador = None

        try:
            # 1. Buscar o Jogador pelo email
            stmt = select(Jogador).where(Jogador.email == email)
            jogador = sessao.execute(stmt).scalar_one_or_none()

            # 2. Verificar o resultado da busca
            if jogador:
                # 3. Verificar a senha (Simples, sem hash)
                if jogador.senha == senha_digitada:
                    # SUCESSO: Iniciar a sessão
                    session['logado'] = True
                    session['jogador_id'] = jogador.id_jogador
                    session['nickname'] = jogador.nickname  # Guarda o nickname para usar na página

                    flash(f'Bem-vindo, {jogador.nickname}!', 'success')
                    return redirect(url_for('jogos'))  # Redireciona para a página principal
                else:
                    # ERRO: Senha incorreta
                    flash('E-mail ou senha incorretos.', 'error')

            else:

                flash('E-mail ou senha incorretos.', 'error')

        except Exception as e:
            flash('Ocorreu um erro inesperado durante o login. Tente novamente.', 'error')
            print(f"Erro no Login: {e}")

        finally:
            sessao.close()

    return render_template('login.html')


@app.route('/cadastro-usuario', methods=['GET', 'POST'])
def cadastro_usuario():
    """Rota para exibir o formulário e processar o cadastro de um novo jogador."""

    if request.method == 'POST':
        # 1. Captura de dados (Lê 'nome' do HTML, armazena em 'nickname')
        nickname = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        cpf = request.form.get('cpf')
        data_nascimento_str = request.form.get('data_nascimento')

        # >>>>>> DEBUG: VERIFICA OS DADOS NO TERMINAL <<<<<<
        print(f"Dados Recebidos: Nickname={nickname}, Email={email}, Data={data_nascimento_str}")

        # 2. Validação e Conversão de Data
        try:
            data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d')
        except (ValueError, TypeError) as e:
            flash('Formato de Data de Nascimento inválido. Tente novamente.', 'error')
            print(f"ERRO DE DATA NA CONVERSÃO: {e}")
            return redirect(url_for('cadastro_usuario'))

        # >>>>>> DEBUG: VERIFICA O OBJETO DATETIME CONVERTIDO <<<<<<
        print(f"Data Convertida: {data_nascimento}")

        sessao = local_secao()
        try:
            # 3. CRIAÇÃO E INSERÇÃO DO JOGADOR (TODOS OS CAMPOS OBRIGATÓRIOS)
            novo_jogador = Jogador(
                nickname=nickname,
                email=email,
                senha=senha,
                cpf=cpf,
                data_nascimento=data_nascimento
            )

            sessao.add(novo_jogador)
            sessao.commit()

            # SUCESSO: Redireciona com a mensagem flash
            flash('Conta criada com sucesso! Você já pode fazer login.', 'success')
            return redirect(url_for('login'))

        except SQLAlchemyError as e:
            sessao.rollback()
            # Tratamento de erro (como duplicidade)
            if "Duplicate entry" in str(e):
                flash('Erro: Este E-mail ou CPF já está cadastrado. Por favor, use dados diferentes.', 'error')
            else:
                flash('Ocorreu um erro inesperado ao registrar. Tente novamente.', 'error')

            # Imprime o erro do banco de dados no terminal
            print(f"ERRO SQLALCHEMY: {e}")
            return redirect(url_for('cadastro_usuario'))

        finally:
            sessao.close()

    return render_template('cadastro_usuario.html')


@app.route('/catalogo')
@app.route('/jogos')
def jogos():
    """Renderiza a página do Catálogo de Jogos (jogos.html)."""
    db_session = local_secao()

    jogos_sql = select(Jogo)
    jogos = db_session.execute(jogos_sql).scalars().all()

    return render_template('jogos.html', jogos=jogos)


@app.route('/sobre')
@app.route('/contato')
def sobre_contato():
    """Renderiza a página combinada de Sobre e Contato."""
    return render_template('sobre_contato.html')


@app.route('/categorias')
def categorias():
    db_session = local_secao()
    categoria_sql = db_session.execute(select(Categoria)).scalars()
    lista = []
    for categoria in categoria_sql:
        lista.append(categoria.serialize())
    db_session.close()
    return render_template('categorias.html', categorias=lista)


# ----------------------------------------------------
# 4. ROTAS DE CATEGORIAS (DETALHE)
# ----------------------------------------------------

@app.route('/categoria/acao')
def categoria_acao():
    return render_template('acao.html')


@app.route('/categoria/aventura')
def categoria_aventura():
    return render_template('aventura.html')


@app.route('/categoria/rpg')
def categoria_rpg():
    return render_template('rpg.html')


@app.route('/categoria/simulacao')
def categoria_simulacao():
    return render_template('simulacao.html')


@app.route('/categoria/esporte')
def categoria_esporte():
    return render_template('esportes.html')


@app.route('/categoria/terror')
def categoria_terror():
    return render_template('terror.html')


# ----------------------------------------------------
# 5. ROTA DE CADASTRO DE JOGOS
# ----------------------------------------------------

@app.route('/cadastro-jogo', methods=['GET', 'POST'])
def cadastro_jogo():
    """Exibe o formulário e processa o cadastro de um novo jogo."""
    db_session = local_secao()
    try:
        if request.method == 'POST':
            # Captura os dados do formulário
            nome = request.form.get('nome')
            url_imagem = request.form.get('url_imagem')
            preco = request.form.get('preco')
            data = request.form.get('data')
            descricao = request.form.get('descricao')
            # Lógica de inserção de Jogo será adicionada aqui futuramente
            jogo = Jogo(
                nome_jogo=nome,
                url_img=url_imagem,
                preco=int(preco),
                data_lancamento=datetime.strptime(data, '%Y-%m-%d'),
                descricao=descricao
            )

            db_session.add(jogo)
            db_session.commit()

            # Redireciona para o catálogo após o cadastro
            flash('Cadastro de jogo temporariamente desativado. Dados recebidos, mas não salvos.', 'info')
            return redirect(url_for('jogos'))
    except SQLAlchemyError as e:
        flash(f"Erro {e}")
    return render_template('cadastro_de_jogos.html')

@app.route('/cadastro-categoria', methods=['GET', 'POST'])
def cadastro_categoria():
    sessao = local_secao()

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        descricao = request.form.get('descricao', '').strip()
        url_imagem = request.form.get('img_url', '').strip()

        if not nome or not descricao or not url_imagem:
            flash('Preencha todos os campos.', 'error')
            return redirect(url_for('cadastro_categoria'))

        nova_categoria = Categoria(
            nome=nome,
            descricao=descricao,
            img_url4=url_imagem
        )

        try:
            sessao.add(nova_categoria)
            sessao.commit()
            flash(f'Categoria "{nome}" cadastrada com sucesso!', 'success')

        except SQLAlchemyError as e:
            sessao.rollback()
            flash('Erro ao cadastrar categoria.', 'error')
            print(e)

        finally:
            sessao.close()

        return redirect(url_for('cadastro_categoria'))

    return render_template('cadastro_de_categoria.html')


if __name__ == '__main__':
    app.run(debug=True)
