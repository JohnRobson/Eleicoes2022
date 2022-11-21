## Base de Dados das Eleições 2022

################################################################

AVISO de Licença de Uso e Reserva de Direitos Autorais BSD 3 Clause

Copyright (c) 2022 por John Robson <john.robson@msn.com> (PIX)

Todo o Código fonte e demais arquivos estão sobre a Licença BSD 3 Clause.
Modificações, Redistribuição, uso Comercial são permitidos, sempre informando
esse aviso de direitos autorais e o repositório oficial:

https://github.com/JohnRobson/Eleicoes2022

################################################################

> DOWNLOAD do Banco de Dados:
>
> https://mega.nz/file/AA1xFIba#qtNIePEohlBJW1ymFcoY1M3K1ZQ02z2wVy1s3Qaubo8

> DOWNLOAD dos Arquivos de Log e BU do 1o Turno:
>
> LOG: https://mega.nz/file/UA9FASzJ#SzpsO5pSbR6Wp4tVpB3CqTgO0PAyGtCNxMCaT4L4G2A
>
> BU: https://mega.nz/file/FZMl2KQC#jX6mF7dzLuari_VLNTXXwoRX4ONk6K443yKt2wRWTX4

> DOWNLOAD dos Arquivos de Log e BU do 2o Turno:
>
> LOG: https://mega.nz/file/pVdWwAiD#ABEY6zOvmzUNRkY9ydhscFLo0FLbB35Yf-QyWViPZCY
>
> BU: https://mega.nz/file/RRlgUKCB#nKi9Gk0ci-Qw673p9SwcRMu2bFngsAx2gAUIwE2130Y

Este aquivo tem um banco de dados SQLite com o Registro de Todas as Urnas (944.051) com os Votos para Presidente e Governador no 1 e 2 Turnos nas eleições de 2022.

É uma ótima base de dados para pesquisas facilmente exportável para todos os tipos de softwares de análsies.

Os nomes das Colunas são auto-explicativos, quanto ao Nome das colunas de Votos:

````{verbatim, lang = "markdown"}
vPresA22 = votos para o Presidente Bolsonaro
vPresB13 = votos para o Lula
vPresNulo = votos para presidente nulos
vPresBranco = votos para presidente branco

vGovA = Votos do Governador MAIS Alinhado com Bolsonaro
vGovB =  Votos do Governador MAIS Alinhado Alinhado com Lula
vGovNulo = votos governador nulo
vGovBranco = votos governador branco

vPresTotal = é a conta do total de votos para presidente registrados no Log da urna, tem que bater com o BU

jaVotou = quando o mesário tenta habilitar alguém que já tinha votado
(provavelmente alguém votou no lugar daquela pessoa e mais tarde ela apareceu para votar)
````

Resultado dos 2 Turnos:
````{verbatim, lang = "markdown"}
SELECT turno, SUM(vPresA22) AS "Bolsonaro", SUM(vPresB13) AS "Lula", SUM(vPresNulo) AS "pNulo", SUM(vPresBranco) AS "pBranco" FROM urnas GROUP BY turno ORDER BY turno
````

Resultado dos 2 Turnos para cada estado:
````{verbatim, lang = "markdown"}
SELECT turno, regiao, estado, SUM(vPresA22) AS "Bolsonaro", SUM(vPresB13) AS "Lula", SUM(vPresNulo) AS "pNulo", SUM(vPresBranco) AS "pBranco", SUM(vGovA) AS "GovA", SUM(vGovB) AS "GovB", SUM(vGovNulo) AS "gNulo", SUM(vGovBranco) AS "gBranco" FROM urnas GROUP BY turno, estado ORDER BY turno, regiao, estado
````

Total de votos de urnas e votos das urnas que fecharam 15 minutos após a abertura
````{verbatim, lang = "markdown"}
SELECT turno, count(id), sum(qComparecimento) FROM urnas WHERE datetime(dataHoraEncerramento) > datetime(dataHoraAbertura, '+09:15:00') GROUP BY turno;
````

Fontes usadas para gerar o Banco de Dados, Logs de Urna e Boletina de Urna são todas do próprio site do TSE:
* https://resultados.tse.jus.br/oficial/app/index.html#/eleicao/resultados
* https://dadosabertos.tse.jus.br/dataset/resultados-2022-arquivos-transmitidos-para-totalizacao


Lista dos Estados e a Seleção de 2 (dois) governadores para registro dos dados:

````{verbatim, lang = "markdown"}
{
'DF': ['CO', 'Distrito Federal', 15, 43], # Ibaneis Rocha (15 MDB) X (43 PV) Leandro Grass
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
'ZZ': ['EX', 'Exterior', 0, 0]
}
````

Para Escolher o Governador Mais ALINHADO com cada condidato, eu consultei várias informações públicas
alguns estados, como em SP o alinhamento é bem evidente para ambos os candidatos,
em vários outros estados tb existiam alinhamento para pelo menos 1 canditado
em poucos estados esse alinhamento era neutro.

Mas a Regra é o vGov"A" é mais alinhado com o Bolsonaro e o vGov"B" com o Lula,
o que torna mais fácil as alálises para comparar se o Presidente Bolsonaro teve
pelo menos tantos votos quanto seu candidato a governador mais alinhado vGovA.
