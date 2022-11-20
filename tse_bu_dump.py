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

import argparse
import logging
import os
import sys

import asn1tools

exibir = False


class BUDump(object):
	def __init__(self, asn1_paths: list):
		print('Carrega Programa do TSE para Decodificar BUs', flush=True)
		self.conv = asn1tools.compile_files(asn1_paths, codec="ber")


	def espacos(self, profundidade: int):
		return ".	 " * profundidade


	def valor_membro(self, membro):
		if isinstance(membro, (bytes, bytearray)):
			return bytes(membro).hex()
		return membro


	def print_list(self, lista: list, profundidade: int):
		indent = self.espacos(profundidade)
		for membro in lista:
			if type(membro) is dict:
				self.print_dict(membro, profundidade + 1)
			else:
				self.print(f"{indent}valor_membro(membro)")


	def print_dict(self, entidade: dict, profundidade: int):
		indent = self.espacos(profundidade)
		for key in sorted(entidade):
			membro = entidade[key]
			if type(membro) is dict:
				print(f"{indent}{key}:")
				self.print_dict(membro, profundidade + 1)
			elif type(membro) is list:
				print(f"{indent}{key}: [")
				self.print_list(membro, profundidade + 1)
				print(f"{indent}] <== {key}")
			else:
				print(f"{indent}{key} = {self.valor_membro(membro)}")


	def processa_bu(self, bu_path: str):
		envelope_decoded = None
		bu_decoded = None

		try:
			with open(bu_path, "rb") as file:
				envelope_encoded = bytearray(file.read())

			envelope_decoded = self.conv.decode("EntidadeEnvelopeGenerico", envelope_encoded)
			bu_decoded = self.conv.decode("EntidadeBoletimUrna", envelope_decoded["conteudo"])

			if exibir:
				del envelope_decoded["conteudo"]	# remove o conteúdo para não imprimir como array de bytes
				print("EntidadeEnvelopeGenerico:")
				self.print_dict(envelope_decoded, 1)

				print("EntidadeBoletimUrna:")
				self.print_dict(bu_decoded, 1)
			else:
				return bu_decoded
		except Exception as e:
			if exibir: print(e)
			return None


def main():
	parser = argparse.ArgumentParser(
		description="Converte um Boletim de Urna (BU) da Urna Eletrônica (UE) e imprime um extrato",
		formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-a", "--asn1", nargs="+", required=True,
						help="Caminho para o arquivo de especificação asn1 do BU")
	parser.add_argument("-b", "--bu", type=str, required=True,
						help="Caminho para o arquivo de BU originado na UE")
	parser.add_argument("--debug", action="store_true", help="ativa o modo DEBUG do log")

	args = parser.parse_args()

	bu_path = args.bu
	asn1_paths = args.asn1
	level = logging.DEBUG if args.debug else logging.INFO
	logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")

	logging.info("Converte %s com as especificações %s", bu_path, asn1_paths)
	if not os.path.exists(bu_path):
		logging.error("Arquivo do BU (%s) não encontrado", bu_path)
		sys.exit(-1)
	for asn1_path in asn1_paths:
		if not os.path.exists(asn1_path):
			logging.error("Arquivo de especificação do BU (%s) não encontrado", asn1_path)
			sys.exit(-1)

	bud = BUDump(asn1_paths)
	bud.processa_bu(bu_path)


# Test: $ python tse_bu_dump.py -a tse_bu.asn1 -b test/o00407-1310200990074.bu

if __name__ == '__main__':
	exibir = True
	main()
