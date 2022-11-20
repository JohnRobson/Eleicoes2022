#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r''' ################################################################

AVISO de Licença de Uso e Reserva de Direitos Autorais BSD 3 Clause

Copyright (c) 2022 por John Robson <john.robson@msn.com> (PIX)

Todo o Código fonte e demais arquivos estão sobre a Licença BSD 3 Clause.
Modificações, Redistribuição, uso Comercial são permitidos, sempre informando
esse aviso de direitos autorais.

Repositório oficial: https://github.com/JohnRobson/Eleicoes2022

################################################################ '''

'''
SQLite Database
https://www.sqlite.org/datatype3.html
https://docs.sqlalchemy.org/en/latest/dialects/sqlite.html
'''
from sqlalchemy import create_engine, Column
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from sqlalchemy import String, Integer, SmallInteger, DateTime
from src_config import arquivo_banco_de_dados

engine = create_engine(arquivo_banco_de_dados, echo=False, future=False, convert_unicode=True)
Base = declarative_base()
Base.metadata.bind = engine
Session = scoped_session(sessionmaker(autoflush=True, autocommit=False, bind=engine))



class Urnas(Base):
	r''' Esta tabela é Exclusiva para o 2o Turno,
	com 2 cargos de Presidente e Governador,
	para o 1o Turno é necessário criar uma tabela de candidatos. '''
	__tablename__ = "Urnas"

	id = Column(Integer, primary_key=True)
	turno = Column(SmallInteger, default=2)

	# Dados do Arquivo BU da Urna

	# Localização da Urna
	regiao = Column(String(2), nullable=False)
	estado = Column(String(2), nullable=False)
	municipio = Column(SmallInteger, nullable=False)
	zona = Column(SmallInteger, nullable=False)
	local = Column(SmallInteger, nullable=False)
	secao = Column(SmallInteger, nullable=False)

	# Registro dos Votos na Urna Para Presidente, Governador, Brancos e Nulos
	vPresA22 = Column(SmallInteger, default=0) # Votos Bolsonaro
	vPresB13 = Column(SmallInteger, default=0) # Votos Lula
	vPresNulo = Column(SmallInteger, default=0)
	vPresBranco = Column(SmallInteger, default=0)

	vGovA = Column(SmallInteger) # Mais Alinhado com Bolsonaro
	vGovB = Column(SmallInteger) # Mais Alinhado com Lula
	vGovNulo = Column(SmallInteger)
	vGovBranco = Column(SmallInteger)

	qEleitAptos = Column(SmallInteger, nullable=False)
	qComparecimento = Column(SmallInteger, default=0)
	qEleitLibCodigo = Column(SmallInteger, default=0)
	qEleitBiometrico = Column(SmallInteger, default=0)

	# Dados do Arquivo de LOG da Urna # não usar "nullable=False"
	vPresTotal = Column(SmallInteger) # conta os votos de presidente recebidos no log da urna, tem que bater com o BU
	modelUrna = Column(String(6), default='UE0000') # 'UE0000' sem arquivo de log | 'UE1111' com arquivo de log, mas sem informar o modelo da urna

	# Estudos
	jaVotou = Column(SmallInteger) # quando o mesário tenta habilitar alguém que já tinha vitado (provavelmente o mesário votou no lugar daquela pessoa e mais tarde ela apareceu para votar)
	vPresIntervalo = Column(String) # 100 menores intervalos de tempo em segundos entre 2 votos durante a votação
	vConfPres1min = Column(String) # total votos confirmados para Presidente a cada 1 minuto

	# Mais Dados Gerais da Urna (Arquivo BU)
	arquivoBU = Column(String(23), nullable=False)
	# idEleicao = Column(SmallInteger, nullable=False)
	dataHoraAbertura = Column(DateTime)
	dataHoraEncerramento = Column(DateTime)
	# dataGeracao = Column(DateTime, nullable=False)
	# dataHoraEmissao = Column(DateTime, nullable=False)
	# codigoCarga1 = Column(String(24), nullable=False)
	# dataHoraCarga1 = Column(DateTime, nullable=False)
	numeroInternoUrna1 = Column(Integer, nullable=False)
	numeroSerieFC1 = Column(String(8), nullable=False)
	# codigoCarga2 = Column(String(24), nullable=False)
	# dataHoraCarga2 = Column(DateTime, nullable=False)
	numeroInternoUrna2 = Column(Integer, nullable=False)
	numeroSerieFC2 = Column(String(8), nullable=False)
	numeroSerieFV = Column(String(8), nullable=False)

	numeroInternoUrna2 = Column(Integer, nullable=False)
	numeroSerieFC2 = Column(String(8), nullable=False)
	numeroSerieFV = Column(String(8), nullable=False)

	# tipoUrna = Column(String(12), nullable=False)
	# versaoVotacao = Column(String, nullable=False)

	# Colunas Extras para uso Opcional e Testes
	'''
	int1 = Column(Integer)
	int2 = Column(Integer)
	int3 = Column(Integer)

	flt1 = Column(Float)
	flt2 = Column(Float)
	flt3 = Column(Float)
	flt4 = Column(Float)
	flt5 = Column(Float)

	txt1 = Column(String)
	txt2 = Column(String)
	'''


def add_column(engine, table_name, column):
	column_name = column.compile(dialect=engine.dialect)
	column_type = column.type.compile(engine.dialect)
	engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type))


if __name__ == '__main__':
	print('Banco de Dados')

	# insere coluna no Banco de Dados
	column = Column('fastVotes3', SmallInteger, default=0)
	# column = Column('fastVotes2', SmallInteger, nullable=False)

	add_column(engine, 'Urnas', column)
