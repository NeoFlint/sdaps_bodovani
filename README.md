# SDAPS_bodovani.py
Skript pro bodové vyhodnocení formulářů přijímacích zkoušek, založené na CSV datech OMR rekognice programu SDAPS.
Homepage programu SDAPS včetně návodů zde: https://sdaps.org/

POUŽITÍ SKRIPTU
---------------
1. do adresáře SDAPS projektu s CSV daty provedené rekognice formulářů nakopírovat tento skript

	data_sdaps.csv

2. přidat rozšifrovaný soubor s bodovou hodnotou a s klíčem správných odpovědí - POZOR! sloupce nepřehazovat ani nemazat, skript s nimi počítá tak jak jsou (pořadí i jméno)

	spravne_odpovedi.ods

3. zkontrolovat/zeditovat tento skript, hlavně cesty a názvy vstupních souborů
4. otevřít terminál v tomto adresáři a spustit skript --> náhled výsledků a případné chyby budou v terminálu.

	python zpracuj_sdaps.py

4. doupravit výstup, tj. soubor vysledky.ods - vhodná je šířka sloupců 1-60 na 0.7cm + zašifrovat 

	vysledky_sifra.ods

5. na papírové formuláře dopsat bodové hodnocení a vše zkontrolovat + odstranit dočasné soubory


Vlastnosti skriptu, poznámky
----------------------------
- umí zpracovat rozdílnou bodovou hodnotu jednotlivých otázek (viz editace souboru spravne_odpovedi.ods)
- umí pracovat s větším počtem sekcí formuláře skládaného v programu LaTex
- je připraven na použití formulářů s reálnými questionnaire_id

SDAPS questionnaire_id nepoužíváme, zatím je tedy ID uchazeče ve sloupci 0_1_1, kam jej ručně přepsal zpracovatel při kontrole recognice (viz sdaps gui).


Upozornění
----------
Výsledky přijímacích zkoušek podléhají utajení (manipulace, žaloby, vydírání, kompromitace školy apod.) - proto se ujistěte, že výstupem je pouze a jen zašifrovaná tabulka ODS, všechny ostatní dočasné soubory s výsledky je potřeba bezpečně smazat (Shift + Delete).


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
