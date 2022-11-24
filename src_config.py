#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r''' ################################################################

AVISO de Licença de Uso e Reserva de Direitos Autorais BSD 3 Clause

Copyright (c) 2022 por John Robson <john.robson@msn.com> (PIX)

Todo o Código fonte e demais arquivos estão sobre a Licença BSD 3 Clause.
Modificações, Redistribuição, uso Comercial são permitidos, sempre informando
esse aviso de direitos autorais e o repositório oficial:

	https://github.com/JohnRobson/Eleicoes2022

################################################################ '''

import datetime as dt
import warnings

pasta_totalizacoes = './tse' # pasta com os Zip das Totalizações do TSE
pasta_totalizacao_tmp = f'{pasta_totalizacoes}/tmp' # DEV: pasta temporária para descompactar o arquivo de cada estado. esta pasta será Criada e Deletada todas as vezes
arquivo_banco_de_dados = 'sqlite:///urnas_2022.sqlite3' # DEV: local do banco de dados SQLite
# SQLite na Memória: "sqlite+pysqlite:///:memory:"
# PostgreSQL: "postgresql://{username}:{password}@localhost:{port}/{database}"
# MariaDB: "mariadb+mariadbconnector://{username}:{password}@localhost:{port}/{database}"
# MySQL: "mysql+pymysql://{username}:{password}@localhost/{database}?charset=utf8"
# MSSQL Server: 'mssql+pyodbc://{user}:{password}@{localhost}/{database}'
# MSSQL Server: mssql+pymssql://{user}:{password}@{localhost}:{port}/{database}

turnos = {1: ('2022-10-01', '2022-10-02'), 2: ('2022-10-28', '2022-10-30')}


# Estado, Região, Nome do Estado, Número do Governador "vGovA", Número do Governador "vGovB"
# vGovA e vGovB são os candidatos a governo mais alinhados com Bolsonaro e Lula respectivamente.
# 0 (zero) significa que não há votação para governador no 2o Turno.
# https://www.tse.jus.br/partidos/partidos-registrados-no-tse/registrados-no-tse


federacao = {'DF': ['CO', 'Distrito Federal', (15, 'Ibaneis Rocha (MDB)'), (43, 'Leandro Grass (PV')],
						'GO': ['CO', 'Goiás', (44, 'Ronaldo Caiado (União Brasil)'), (22, 'Major Vitor Hugo (PL)')],
						'MT': ['CO', 'Mato Grosso', (44, 'Mauro Mendes (União Brasil)'), (43, 'Márcia Pinheiro (PV)')],
						'MS': ['CO', 'Mato Grosso do Sul', (28, 'Capitão Contar (PRTB)'), (45, 'Eduardo Riedel (PSDB)')],
						'AL': ['NE', 'Alagoas', (44, 'Rodrigo Cunha (União Brasil)'), (15, 'Paulo Dantas (MDB)')],
						'BA': ['NE', 'Bahia', (44, 'ACM Neto (União Brasil)'), (13, 'Jerônimo Rodrigues (PT)')],
						'CE': ['NE', 'Ceará', (44, 'Capitão Wagner (União Brasil)'), (13, 'Elmano de Freitas (PT)')],
						'MA': ['NE', 'Maranhão', (20, 'Lahesio Bonfim (PSC)'), (40, 'Carlos Brandão (PSB)')],
						'PB': ['NE', 'Paraíba', (45, 'Pedro Cunha Lima (PSDB)'), (40, 'João Azevêdo (PSB)')],
						'PE': ['NE', 'Pernambuco', (45, 'Raquel Lyra (PSDB)'), (77, 'Marília Arraes (Solidariedade)')],
						'PI': ['NE', 'Piauí', (44, 'Silvio Mendes (União Brasil)'), (13, 'Rafael Fonteles (PT)')],
						'RN': ['NE', 'Rio Grande do Norte', (77, 'Fabio Dantas (Solidariedade)'), (13, 'Fátima Bezerra (PT)')],
						'SE': ['NE', 'Sergipe', (55, 'Fábio Mitidieri (PSD)'), (13, 'Rogério Carvalho (PT)')],
						'AC': ['N', 'Acre', (11, 'Gladson Cameli (PP)'), (13, 'Jorge Viana (PT)')],
						'AP': ['N', 'Amapá', (55, 'Jaime Nunes (PSD)'), (77, 'Clécio (Solidariedade)')],
						'AM': ['N', 'Amazonas', (44, 'Wilson Lima (União Brasil)'), (15, 'Eduardo Braga (MDB)')],
						'PA': ['N', 'Pará', (22, 'Zequina Marinho (PL)'), (15, 'Helder Barbalho (MDB)')],
						'RO': ['N', 'Rondônia', (22, 'Marcos Rogério (PL)'), (44, 'Coronel Marcos Rocha (União Brasil)')],
						'RR': ['N', 'Roraima', (11, 'Antônio Denarium (PP)'), (15, 'Tereza Surita (MDB)')],
						'TO': ['N', 'Tocantins', (10, 'Wanderlei Barbosa (Republicanos)'), (22, 'Ronaldo Dimas (PL)')],
						'ES': ['SE', 'Espírito Santo', (22, 'Carlos Manato (PL)'), (40, 'Renato Casagrande (PSB)')],
						'MG': ['SE', 'Minas Gerais', (30, 'Romeu Zema (Novo)'), (13, 'Kalil (PT)')],
						'RJ': ['SE', 'Rio de Janeiro', (22, 'Cláudio Castro (PL)'), (40, 'Marcelo Freixo (PSB)')],
						'SP': ['SE', 'São Paulo', (10, 'Tarcísio de Freitas (Republicanos)'), (13, 'Fernando Haddad (PT)')],
						'PR': ['S', 'Paraná', (55, 'Ratinho Jr. (PSD)'), (13, 'Requião (PT)')],
						'RS': ['S', 'Rio Grande do Sul', (22, 'Onyx Lorenzoni (PL)'), (45, 'Eduardo Leite (neutro) (PSDB)')],
						'SC': ['S', 'Santa Catarina', (22, 'Jorginho Mello (PL)'), (13, 'Décio Lima (PT)')],
						'ZZ': ['EX', 'Exterior', (0, 'Sem Governador'), (0, 'Sem Governador')]}

estados_federacao = federacao.keys() # lista com os nomes dos estados

# tipoUrna = {'secao': 1, 'contingencia': 2, 'reservaSecao': 3}

urna_log_remove_texto_exato = None # filtrar textos do Log da Urna
with open('urna_log_remove_texto_exato.txt', 'r') as text_remove:
	urna_log_remove_texto_exato = text_remove.read().splitlines() # readlines()

urna_log_remove_texto_contendo = None # filtrar textos do Log da Urna
with open('urna_log_remove_texto_contendo.txt', 'r') as text_remove:
	urna_log_remove_texto_contendo = text_remove.read().splitlines() # readlines()

dtf_bu = '%Y%m%dT%H%M%S' # formato para conversão "ISO 8601 Short" no BU


def dtf_log(s): # formato para conversão das datas no arquivo log
	return dt.datetime.strptime(s, '%d/%m/%Y %H:%M:%S')


warnings.filterwarnings('ignore', category=FutureWarning, message=('.*will attempt to set the values inplace instead of always setting a new array. To retain the old behavior, use either.*'), )



if __name__ == '__main__':
	print('Variáveis Utilizadas')
	print(federacao)
