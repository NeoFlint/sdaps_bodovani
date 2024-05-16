# SDAPS_bodovani.py
Terminálový program pro spočítání bodové hodnoty dotazníků z datových souborů SDAPS recognice pro VOŠ.


------------
POSTUP:
------------
1. do jednoho adresáře nahrát potřebné vstupní soubory
2. zeditovat tabulku spravne_odpovedi.ods - POZOR! sloupce nepřehazovat ani nemazat, skript s nimi počítá
3. spustit tento python skript
------------



Vstupy:
------------
template_file = 'spravne_odpovedi.ods'	# klic spravnych odpovedi
input_file = 'data_sdaps.csv'				# SDAPS data z recognice - prvni na radce musi byt cislo respondenta!
section_size = 15							# bohuzel pouzivame sekce a ty maji interni cislovani od 1 - pomuze vypocitat globalni cislo otazky


Výstupy:
------------
output_file = 'vysledky.ods'				# zde budou celkove vysledky prijimacich zkousek

Všechny vstupní i výstupní soubory se předpokládají ve stejném adresáři.


Jazyky, běhové prostředí, doinstalované knihovny
------------
Python 3
pyexcel, pyexcel_ods, pandas


Autor, kontakt
------------
2024-05 Jiří Fictum 
