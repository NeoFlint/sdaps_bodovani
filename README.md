# SDAPS_bodovani.py
Skript pro bodové vyhodnocení formulářů přijímacích zkoušek, založených na CSV datech OMR rekognice programu SDAPS

POUŽITÍ SKRIPTU
---------------
1. do stejného adresáře se skriptem připravit/zeditovat tabulku spravne_odpovedi.ods - POZOR! sloupce nepřehazovat ani nemazat, skript s nimi počítá tak jak jsou (pořadí i jméno)
2. do stejného adresáře se skriptem nahrát soubor data_sdaps.csv obsahující data z recognice programu SDAPS
3. otevřít terminál v tomto adresáři a spustit tento skript --> náhled výsledků a případné chyby budou v terminálu.

	python zpracuj_sdaps.py

4. doupravit vysledky.ods - vhodná je šířka všech sloupců na 0.7cm, ukotvit 1. sloupec a roztáhnout první a poslední sloupec + zašifrovat 
5. na papírové formuláře dopsat bodové hodnocení a vše zkontrolovat


Podrobnosti, vlastnosti skriptu
-------------------------------
- umí zpracovat rozdílnou bodou hodnotu jednotlivých otázek (viz editace souboru spravne_odpovedi.ods)
- umí pracovat s větším počtem sekcí formuláře skládaného v programu LaTex
- je připraven na použití formulářů s reálnými questionnaire_id


Vstupy
------
Vstupní soubory je nutné připravit do stejného adresáře se skriptem a respektovat jejich přesné názvy včetně koncovky souboru.

- spravne_odpovedi.ods => 		...klíč správných odpovědí a bodového hodnocení - musí být připraven jako rozšifrovaný!
- data_sdaps.csv =>  				...SDAPS data z recognice - questionnaire_id nepoužíváme, zatím je tedy ID uchazeče ve sloupci 0_1_1


Výstupy
-------
- => vysledky.ods			...zde budou celkove vysledky prijimacich zkousek 

Všechny vstupní i výstupní soubory se předpokládají ve stejném adresáři spolu se skriptem.


Jazyky, běhové prostředí, závislosti
------------------------------------
Python 3, 
pyexcel, 
pyexcel_ods, 
pandas


Autor, kontakt
--------------
2024-05 Jiří Fictum 
fictum.jiri@gmail.com
