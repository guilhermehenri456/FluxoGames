[FluxoGames.sql](https://github.com/user-attachments/files/24059162/FluxoGames.sql)
create database Jogos;
use  Jogos;
create table if not exists jogo(
	id_jogo int auto_increment primary key,
	nome_jogo varchar(150) not null unique,
	data_lancamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	preco numeric
    
);

create table if not exists genero(
	id_genero int auto_increment primary key,
	tipo_genero varchar(50)
);

create table if not exists empresa(
	id_empresa int auto_increment primary key,
	nome_empresa varchar(50) not null unique,
	email varchar(50) not null unique,
	biografia text
);

create table if not exists plataforma(
	id_plataforma int auto_increment primary key,
	tipo_plataforma varchar(50)
);


create table if not exists jogador(
	id_jogador int auto_increment primary key,
	data_nascimento date,
	data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	cpf varchar(15) not null
);

create table if not exists personagem(
	id_personagem int auto_increment primary key not null,
	historia_personagem text,
	habilidades text,
	fk_id_jogo int
);

create table if not exists personagem_jogo(
	id int auto_increment primary key,
	fk_id_personagem int,
	constraint fk_personagem_jogo foreign key (fk_id_jogo) references jogo (id_jogo),

	fk_id_jogo int,
	constraint fk_jogo_personagem foreign key (fk_id_personagem) references personagem (id_personagem)

    
);
create table if not exists jogo_jogador(
	id int auto_increment primary key,
	fk_id_jogo int,
	constraint fk_jogo_jogador foreign key (fk_id_jogador) references jogador (id_jogador),

	fk_id_jogador int,
	constraint fk_jogador_jogo foreign key (fk_id_jogo) references jogo (id_jogo)

);

create table if not exists jogo_genero(
	id int auto_increment primary key,
	fk_id_genero int,
	constraint fk_genero_jogo foreign key (fk_id_jogo) references jogo(id_jogo),
	fk_id_jogo int,
	constraint fk_jogo_genero foreign key (fk_id_genero) references genero (id_genero)



);
create table if not exists cadastro_categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL UNIQUE,
    descricao VARCHAR(255)
);








alter table jogador
 ADD nickname varchar(50);
 ALTER TABLE cadastro_categorias ADD COLUMN img_url VARCHAR(255) NOT NULL;
alter table jogador ADD email varchar(50);
alter table jogador ADD senha varchar(50);
alter table cadastro_categorias add img_url4 Text;
 
