#!/bin/python
# zpracovani prijimacich testu pro DH na zaklade dat z SDAPS recognice

import io, os
from collections import OrderedDict
from csv import reader
import pyexcel as pe 						# pip install pyexcel
from pyexcel_ods import save_data			# pip install pyexcel_ods
import pandas								# pip install pandas

template_file = 'spravne_odpovedi_sifra-test.ods'		# klic spravnych odpovedi
input_file = 'data_sdaps.csv'				# SDAPS data z recognice - prvni na radce musi byt cislo respondenta!
output_file = 'vysledky.ods'				# zde budou celkove vysledky prijimacich zkousek


# TODO: hlasky o prubehu, kontrola stejneho poctu otazek ve vstupnich souborech
# TODO: IDENTIFIKACE UCASTNIKU v CSV !!! 
# TODO: venv
# TODO: ERRORY!

# Overi existenci potrebnych souboru a nacte z nich data.
def load_inputs():
	# testy zda jsou k dispozici potrebne soubory
	if(not os.path.exists(template_file)):
		print(f"Error: Soubor {template_file} nebyl nalezen! Ukoncuji zpracovani...")
		return False

	if(not os.path.exists(input_file)):
		print(f"Error: Soubor {input_file} nebyl nalezen! Ukoncuji zpracovani...")
		return False

	# nacteni spravnych odpovedi
	print("Kontroly vstupnich souboru dokonceny uspesne.")
	sheet = pe.get_sheet(file_name=template_file, name_rows_by_column=0, start_row=1, encoding='UTF-8')
	correct_answers = sheet.to_dict()
	#for key, value in correct_answers.items():
		#print(key, value[0], value[1])						# value[0] = bodova hodnota, value[1] = spravna odpoved(pismeno)
	
	# nacteni odpovedi uchazecu z SDAPS
	csv_data = []
	with open(input_file, 'r') as csv_file:					# as csv_file je dulezite - diky tomu to nacte
		csv_reader = reader(csv_file, delimiter=",")
		for line in csv_reader:							# workarround - jak lepe?
			csv_data.append(line)
	#for row in csv_data:
	#	print(row)

	# dale pristup k datum za predpokladu stejneho indexu - muzeme si to dovolit, protoze CSV ma urcite shodny pocet prvku v radcich
	return csv_data, correct_answers

# ocisti header od zahlavi, ktere nepatri k otazkam
def set_question_header(csv_header):
	question_header = []
	for item in csv_header[7:]:
		if 'rev' in item:
			continue
		else:
			question_header.append(item)
	#print(len(question_header), question_header)
	return question_header

# Nactena data do vysledneho hodnoceni (marks)
def data_processing(csv_data=None, correct_answers=None):
	if csv_data is None or correct_answers is None:
		print("Error: Neplatne vstupy ke zpracovani!")
		return

	marks = OrderedDict()				# zaklad pro budouci vystupy
	csv_header = csv_data[0]			# hlavicka v CSV
	question_header = set_question_header(csv_header)		# pouze zahlavi k otazkam - index bude roven globalnimu cislu otazky
	col_number = len(csv_header)		# kolik je sloupcu v CSV

	for line in csv_data[1:]:			# zahlavi se vynechava, neobsahuje data

		id = line[0]
		empty = line[1]
		valid = line[3]
		recognized = line[4]
		verified = line[6]

		choices = ('invalid',None,'-','a','b','c','d','e','f','g','h','i','j')		# 10 moznosti na otazku, -1= nevyplneno, -2=nevalidni
		values = {}
		sum = 0

		# ted samotne odpovedi (q_num = cislo otazky)
		#for q_num in range(1,len(question_header)):
		for i in range(7,col_number,1): 	# prvni cast jsou identifikacni informace --> preskakujeme
			if 'rev' in csv_header[i]: 		# review sloupce data neobsahuje --> preskakujeme
				continue
			else:
				# zjisteni podrobnosti k otazce rozparsovanim jejiho headeru
				t,s,q = csv_header[i].split('_')	
				test = int(t)
				section = int(s)
				question = int(q)
				question_number = question_header.index(csv_header[i]) + 1			# zjisteni globalniho cisla otazky

				# nacteni spravne odpovedi a zaznam bodu za otazku
				value, correct_choice = correct_answers[str(question_number)]		# klic je ve slovniku bohuzel v podobe stringu
				answer_num = int(line[i]) + 2										# list choices pocita i s nevalidnimi a neodpovezenymi otazkami
				answer = choices[answer_num]
				#print(f"id: {id}, question_number: {question_number}, answer_num: {answer_num}, answer: {answer}, correct_choice: {correct_choice}")
				
				if(correct_choice == answer):
					values[question_number] = value
					sum += value
				else:
					values[question_number] = 0

		values['bodovy_zisk']=sum
		marks[id] = values

	return marks


# Ulozi zpracovane vysledky do tabulkoveho souboru.
def make_output(marks, jmena=None):
	if marks is None:
		print("ERROR: Prazdne hodnoceni, nemam co zapisovat na output!")

	# zapis do ODS souboru pres skvely dataframe :-) ... krasne data naformatuje a vytvori zahlavi tabulky
	df = pandas.DataFrame.from_dict(marks, orient='index')
	print("Nahled vysledku:")
	print(df)

	#with pandas.ExcelWriter("vysledky.xlsx", mode="w", engine="openpyxl") as writer:		# pip install openpyxl --> XLSX
	with pandas.ExcelWriter(output_file, mode="w", engine="odf") as writer:				# --> ODS
		df.to_excel(writer, sheet_name="Sheet1")

	print(f"Hodnoceni ulozeno do souboru {output_file}.")


#-------- MAIN -----------
if __name__ == '__main__':

	csv_data, correct_answers = load_inputs()
	marks = data_processing(csv_data, correct_answers)
	make_output(marks)