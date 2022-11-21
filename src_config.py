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


federacao = {'DF': ['CO', 'Distrito Federal', 15, 43], # Ibaneis Rocha (15 MDB) X (43 PV) Leandro Grass
						'GO': ['CO', 'Goiás', 44, 22], # Ronaldo Caiado (União Brasil) X (22 PL) Major Vitor Hugo
						'MT': ['CO', 'Mato Grosso', 44, 43], # Mauro Mendes (44 União Brasil) X (43 PV) Márcia Pinheiro
						'MS': ['CO', 'Mato Grosso do Sul', 28, 45], # Capitão Contar (28 PRTB) X Eduardo Riedel (45 PSDB)
						'AL': ['NE', 'Alagoas', 44, 15], # Rodrigo Cunha (44 União Brasil) X Paulo Dantas (15 MDB)
						'BA': ['NE', 'Bahia', 44, 13], # ACM Neto (neutro) (44 União Brasil) X Jerônimo Rodrigues (13 PT)
						'CE': ['NE', 'Ceará', 44, 13], # Capitão Wagner (44 União Brasil) X Elmano de Freitas (13 PT)
						'MA': ['NE', 'Maranhão', 20, 40], # Lahesio Bonfim (20 PSC)X Carlos Brandão (40 PSB)
						'PB': ['NE', 'Paraíba', 45, 40], # Pedro Cunha Lima (neutro) (45 PSDB) X João Azevêdo (40 PSB)
						'PE': ['NE', 'Pernambuco', 45, 77], # Raquel Lyra (45 PSDB) X Marília Arraes (77 Solidariedade)
						'PI': ['NE', 'Piauí', 44, 13], # Silvio Mendes (44 União Brasil) X Rafael Fonteles (13 PT)
						'RN': ['NE', 'Rio Grande do Norte', 77, 13], # Fabio Dantas (77 Solidariedade) X Fátima Bezerra (13 PT)
						'SE': ['NE', 'Sergipe', 55, 13], # Fábio Mitidieri (55 PSD) X Rogério Carvalho (13 PT)
						'AC': ['N', 'Acre', 11, 13], # Gladson Cameli (11 PP) x Jorge Viana (13 PT)
						'AP': ['N', 'Amapá', 55, 77], # Jaime Nunes (55 PSD) x Clécio (77 SD)
						'AM': ['N', 'Amazonas', 44, 15], # Wilson Lima (44 União Brasil) X Eduardo Braga (15 MDB)
						'PA': ['N', 'Pará', 22, 15], # Zequina Marinho (22 PL) X Helder Barbalho (15 MDB)
						'RO': ['N', 'Rondônia', 22, 44], # Marcos Rogério (22 PL) X Coronel Marcos Rocha (44 União Brasil)
						'RR': ['N', 'Roraima', 11, 15], # Antônio Denarium (11 PP) X Tereza Surita (15 MDB)
						'TO': ['N', 'Tocantins', 10, 22], # Wanderlei Barbosa (10 Republicanos) X Ronaldo Dimas (22 PL)
						'ES': ['SE', 'Espírito Santo', 22, 40], # Carlos Manato (22 PL) X Renato Casagrande (40 PSB)
						'MG': ['SE', 'Minas Gerais', 30, 13], # Romeu Zema (Novo) X Kalil (13 PT)
						'RJ': ['SE', 'Rio de Janeiro', 22, 40], # Cláudio Castro (PL) X Marcelo Freixo (PSB 40)
						'SP': ['SE', 'São Paulo', 10, 13], # Tarcísio de Freitas (10 Republicanos) X Fernando Haddad (13 PT)
						'PR': ['S', 'Paraná', 55, 13], # Ratinho Jr. (55 PSD) X Requião (13 PT)
						'RS': ['S', 'Rio Grande do Sul', 22, 45], # Onyx Lorenzoni (22 PL) X Eduardo Leite (neutro) (45 PSDB)
						'SC': ['S', 'Santa Catarina', 22, 13], # Jorginho Mello (22 PL) X Décio Lima (13 PT)
						'ZZ': ['EX', 'Exterior', 0, 0]}

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
