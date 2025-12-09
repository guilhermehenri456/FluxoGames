from sqlalchemy import create_engine, Column, DateTime, func, ForeignKey, Integer, String, Enum, Text
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('mysql+pymysql://root:senaisp@localhost:3306/jogos')

local_secao = sessionmaker(bind=engine)
Base = declarative_base()


class Empresa(Base):
    __tablename__ = 'empresa'
    id_empresa = Column(Integer, primary_key=True)
    nome_empresa = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    biografia = Column(String(255), nullable=True)
    criado_em = Column(DateTime, nullable=False, server_default=func.now())

    def __repr__(self):
        return f'<Empresa( Nome = {self.nome_empresa}, Email = {self.email} )>'


class Genero(Base):
    __tablename__ = 'genero'
    id_genero = Column(Integer, primary_key=True)
    tipo_genero = Column(Enum('rpg', 'simulacao', 'acao', 'terror', 'esporte', 'aventura'), nullable=False)

    def __repr__(self):
        return f'<Genero( Tipo = {self.tipo_genero} )>'


class Jogador(Base):
    __tablename__ = 'jogador'
    id_jogador = Column(Integer, primary_key=True)
    data_nascimento = Column(DateTime, nullable=False)
    data_registro = Column(DateTime, nullable=False, server_default=func.now())
    cpf = Column(String(15), nullable=False)
    nickname = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    senha = Column(String(50), nullable=False)

    def __repr__(self):
        return f'<Nickname ({self.nickname}), Email: {self.email}>'


class Jogo(Base):
    __tablename__ = 'jogo'
    id_jogo = Column(Integer, primary_key=True)
    nome_jogo = Column(String(150), nullable=False)
    data_lancamento = Column(DateTime, nullable=False)
    preco = Column(Integer, nullable=False)
    descricao = Column(String, nullable=False)
    url_img = Column(String, nullable=False)

    # A coluna 'imagens' foi removida, pois não estava no seu CREATE TABLE SQL

    def __repr__(self):
        return f'<Jogo: {self.nome_jogo}, Preço: {self.preco}>'


class Plataforma(Base):
    __tablename__ = 'plataforma'
    id_plataforma = Column(Integer, primary_key=True)
    tipo_plataforma = Column(String(50), nullable=False)

    def __repr__(self):
        return f'<Plataforma: {self.tipo_plataforma}>'


class Personagem(Base):
    __tablename__ = 'personagem'  # Corrigido para minúsculas
    id_personagem = Column(Integer, primary_key=True)
    historia_personagem = Column(Text, nullable=False)
    habilidades = Column(Text, nullable=False)
    fk_id_jogo = Column(Integer, ForeignKey('jogo.id_jogo'), nullable=True)


class Jogo_Genero(Base):
    __tablename__ = 'jogo_genero'  # Corrigido para minúsculas
    id = Column(Integer, primary_key=True)
    # FKs Corrigidas: tabela.pk_coluna (que é 'jogo.id_jogo' e 'genero.id_genero')
    fk_id_jogo = Column(Integer, ForeignKey('jogo.id_jogo'), nullable=False)
    fk_id_genero = Column(Integer, ForeignKey('genero.id_genero'), nullable=False)

    def __repr__(self):
        # Corrigido o formato do __repr__
        return f'<Jogo_Genero (Jogo ID: {self.fk_id_jogo}, Genero ID: {self.fk_id_genero})>'


class Jogo_Jogador(Base):
    __tablename__ = 'jogo_jogador'  # Corrigido para minúsculas
    id = Column(Integer, primary_key=True)
    fk_id_jogo = Column(Integer, ForeignKey('jogo.id_jogo'), nullable=False)
    fk_id_jogador = Column(Integer, ForeignKey('jogador.id_jogador'), nullable=False)

    def __repr__(self):
        return f'<Jogo_Jogador ID: {self.id}>'


class Personagem_Jogo(Base):
    __tablename__ = 'personagem_jogo'
    id = Column(Integer, primary_key=True)
    fk_id_personagem = Column(Integer, ForeignKey('personagem.id_personagem'), nullable=False)
    fk_id_jogo = Column(Integer, ForeignKey('jogo.id_jogo'), nullable=False)

    def __repr__(self):
        return f'<Personagem_Jogo ID: {self.id}>'

class Categoria(Base):
    __tablename__ = 'cadastro_categorias'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), unique=True, nullable=False)
    descricao = Column(String(255), nullable=False)
    img_url4 = Column(Text, nullable=False)

    def serialize(self):
        categorias = {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "img_url4": self.img_url4,
        }
        return categorias

    def __repr__(self):
        return f"<Categoria ID: {self.id}, Nome: {self.nome}>"

