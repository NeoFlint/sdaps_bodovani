#!/bin/python
# Bodove vyhodnoceni prijimacich testu na zaklade CSV dat z SDAPS rekognice.
# https://github.com/NeoFlint/sdaps_bodovani
# otestovano 2024-06-20: OK
# -------------------------

import io, os
from collections import OrderedDict
from csv import reader
import pyexcel as pe 					# pip install pyexcel
from pyexcel_ods import save_data			# pip install pyexcel_ods
import pandas						# pip install pandas

template_file = 'spravne_odpovedi.ods'			# klic spravnych odpovedi - pripraven jako rozsifrovany!
input_file = 'data_sdaps.csv'				# SDAPS data z recognice - prejmenovat soubor nebo upravit jeho jmeno zde
output_file = 'vysledky.ods'				# zde budou celkove vysledky prijimacich zkousek - upravit a ZASIFROVAT!

# -------------------------------
# TODO: identifikace ucastniku v CSV - zatim resena rucnim prepisovanim v GUI - ale celkem to jde
# TODO: GUI rozhrani - par tlacitek misto ovladani z terminalu
# -------------------------------

# Overi existenci potrebnych souboru a nacte z nich data.
def load_inputs():
	# testy zda jsou k dispozici potrebne soubory
	if(not os.path.exists(template_file)):
		print(f"ERROR: Soubor {template_file} nebyl nalezen! Ukoncuji zpracovani...")
		return False

	if(not os.path.exists(input_file)):
		print(f"ERROR: Soubor {input_file} nebyl nalezen! Ukoncuji zpracovani...")
		return False

	# nacteni spravnych odpovedi
	print("Kontrola vstupnich souboru: OK")
	sheet = pe.get_sheet(file_name=template_file, name_rows_by_column=0, start_row=1, encoding='UTF-8')
	correct_answers = sheet.to_dict()
	#print("Spravne odpovedi:")
	#for key, value in correct_answers.items():
		#print(key, value[0], value[1])					# value[0] = bodova hodnota, value[1] = spravna odpoved(pismeno)
	
	# nacteni odpovedi uchazecu z SDAPS
	csv_data = []
	with open(input_file, 'r') as csv_file:					# as csv_file je dulezite - diky tomu to nacte
		csv_reader = reader(csv_file, delimiter=",")
		for line in csv_reader:						# workarround - jak lepe?
			csv_data.append(line)
	#for row in csv_data:							# prehled nacteneho obsahu CSV
		#print(row)

	# dale pristup k datum za predpokladu stejneho indexu - muzeme si to dovolit, protoze CSV ma urcite shodny pocet prvku v radcich
	return csv_data, correct_answers

# ocisti header od zahlavi, ktere nepatri k otazkam
def set_question_header(csv_header):
	question_header = []
	for item in csv_header[7:]:
		chunks = item.split('_')
		if 'rev' in item:
			continue
		elif len(chunks) > 3:						# jednickami rozebrane a,b,c,d u odpovedi do headeru nepotrebujeme
			continue	
		else:
			question_header.append(item)
	#print("Delka zahlavi:", len(question_header))
	#print("Zahlavi:", question_header)
	return question_header

# Nactena data do vysledneho hodnoceni (marks)
def data_processing(csv_data=None, correct_answers=None):
	if csv_data is None or correct_answers is None:
		print("ERROR: Neplatne vstupy ke zpracovani!")
		return
		
	marks = OrderedDict()					# zaklad pro budouci vystupy
	csv_header = csv_data[0]				# hlavicka v CSV
	question_header = set_question_header(csv_header)	# pouze zahlavi k otazkam - index bude roven globalnimu cislu otazky
	col_number = len(csv_header)				# kolik je sloupcu v CSV
	
	if len(question_header)-1 == len(correct_answers):
		print("Kontrola poctu spravnych odpovedi a poctu otazek ve vstupnich souborech: OK")
	else:
		print("POZOR!!! Pocet spravnych odpovedi a celkovy pocet otazek ve vstupnich souborech NESOUHLASI!!!")
		return

	for line in csv_data[1:]:				# zahlavi se vynechava, neobsahuje data

		# rozbor metadat odpovedi
		# id = line[0] 					# pokud CSV obsahuje skutecna questionnaire_id
		id = line[9]					# pokud je ID jako 10. hodnota na radce (sloupec 0_1_1) - pripraveno ve formu jako "ID uchazece"
		empty = line[2]
		valid = line[3]
		recognized = line[4]
		verified = line[6]
		
		if id in marks.keys():				# pokud nebylo upraveno ID uchazece, SDAPS generuje do csv hodnotu 1 - nutno resit a v SDAPS GUI doplnit!
			print(f"ID {id} jiz existuje. Preskakuji... Zkontrolujte ID ucastniku ve vstupnich souborech!")
			continue

		choices = ('None','a','b','c','d','e','f','g','h','i','j')		# 10 moznosti na otazku, 
		choices_else = ('invalid','error-multi-select','NA', None)		# -1=NA=nevyplneno, -2=error-multi-select=nevalidni
		values = {}
		sum = 0

		# ted samotne odpovedi (q_num = cislo otazky)
		for i in range(12,col_number,1): 							# prvni cast jsou identifikacni informace --> preskakujeme
			if 'rev' in csv_header[i]: 							# review sloupce data neobsahuje --> preskakujeme
				continue
			else:
				chunks = csv_header[i].split('_')					# zjisteni podrobnosti k otazce rozparsovanim jejiho headeru
				if len(chunks) > 3:							# jednickami rozebrane a,b,c,d u odpovedi preskakujeme - informaci uz vime
					continue	
				test = int(chunks[0])
				section = int(chunks[1])
				question = int(chunks[2])
				question_number = question_header.index(csv_header[i])			# zjisteni globalniho cisla otazky

				# nacteni spravne odpovedi a zaznam bodu za otazku
				value, correct_choice = correct_answers[str(question_number)]		# klic je ve slovniku bohuzel v podobe stringu
				answer_num = int(line[i]) if line[i].isdigit() else 0			# drivejsi SDAPS daval jen ciselnou hodnotu odpovedi, ted uz tu mame i textove vystupy
				answer = choices[answer_num]						
				# print(f"id: {id}, question_number: {question_number}, answer_num: {answer_num}, answer: {answer}, correct_choice: {correct_choice}")
				
				if(correct_choice == answer):
					values[question_number] = value
					sum += value
				else:
					values[question_number] = 0					# neciselna hodnota odpovedi je proste 0b bez dalsiho zkoumani

		values['bodovy_zisk']=sum								# pridani obodovaneho dotazniku do datoveho slovniku
		marks[id] = values

	return marks

# Ulozi zpracovane vysledky do tabulkoveho souboru.
def make_output(marks, jmena=None):
	if marks is None:
		print("ERROR: Prazdne hodnoceni, nemam co zapisovat na output!")
		return

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
