ELEKTRONICKÉ VYHODNOCENÍ PAPÍROVÝCH FORMULÁŘŮ
=============================================
Virtualizační platforma VirtualBox 7.0.18
připravené virtuální PC "Xubuntu_22-04" (export v souboru .ova - stačí importovat a spustit)
- na ploše je připravený návod a nainstalováno vše potřebné (systémové nástroje, SDAPS rekognice, skript pro spočítání výsledků) 
- test 20.6.2024: OK
Pro přenos souborů do virtuálního PC (dále VM) lze využít Přídavky pro hosta a soubory přetáhnout myší, další možností je sdílená složka a nakonec cloud (googledisk, dropbox apod.) Virtuální PC je zcela oddělené od hostitelského, proto je principálně složité zprovoznit přenášení soubory z flešky přímo do VM. Tento návod je na ploše přímo uvnitř VM, takže pro samotné zpracování je kopírování příkazů dostupné vždy i bez sítě.

!!! Po provední zpracování nezapomeňte po sobě smazat všechny nezašifrované soubory se správnými odpověďmi a s výsledky přijímacího řízení !!!

Homepage systémů, soubory ke stažení
-----------------------------------
Systém SDAPS má velmi pěknou dokumentaci, v podstatě se stačí řídit návodem. Pro vyzkoušení systému existuje vzor formuláře example.tex (viz github), obsahující možné funkcionality a ze kterého lze vyjít při tvorbě vlastního odpovědního formuláře. 

	https://sdaps.org/
	https://github.com/sdaps/sdaps/tree/master/sdaps
	https://ctan.org/pkg/sdaps
	https://github.com/NeoFlint/sdaps_bodovani


Recognice formulářů (OMR)
-------------------------
0. PŘÍPRAVA FORMULÁŘŮ
- existuje vzor SDAPS, ve kterém jsou obsažené všechny použitelné funkcionality - kód formuláře ke stažení zde, z něj je možné vyjít pro případné úpravy našeho formuláře form.tex (jsou potřebné základní znalosti systému LaTex):

	https://raw.githubusercontent.com/sdaps/sdaps/master/examples/example.tex


1. PŘÍPRAVA PROJEKTU 
- adresář TEMP na ploše: zde připravit finální kód formuláře - soubor .tex (pro přípravu/úpravu formuláře lze využít instalované LaTeX Studio)
- nahrát sem potřebné soubory pro SDAPS (pravý klik v adresáři --> otevřít terminál zde):

	cp -R /usr/share/texlive/texmf-dist/tex/latex/sdaps/* .
	
- zkontrolovat obsah adresáře

	ll
	
- vygenerovat PDF náhled form.pdf budoucího formuláře k tisku - zatím netisknutelné s vodoznakem "DRAFT" (pokud jsou chyby, použít variantu se --shell-escape)

	pdflatex form.tex
	pdflatex --shell-escape form.tex
	
- v adresáři SDAPS připravit adresář projektu (název podle roku a kola, jen musí být unikátní) a vygenerovat tisknutelný formulář questionnaire.pdf na základě připraveného form.tex (adresář pro projekt se sám založí a nahraje se do něj automaticky vše potřebné):

	sdaps setup tex ~/Desktop/SDAPS/2024-1 form.tex
	
	...formulář questionnaire.pdf vytisknout pro všechny studenty a vykonat přijímací zkoušky

	
2. SKENOVÁNÍ FORMULÁŘŮ 
- vyplněné formuláře ideálně rozdělit do stosů po 50-100ks, ideálně srovnat vzestupně podle ID
- dále naskenovat formuláře od studentů - celý štúsek lícem nahoru a nejmenším ID nahře založit do horního podavače kopírky, nejlépe skenovat na 300dpi monochrome do vícestránkového souboru TIF (v případě PDF nebo jiných parametrů se musí použít konverze viz dále). Srovnané štosy pomohou s orinetací při dohledávání nesrovnalostí.
- přesun do adresáře projektu

	cd ~/Desktop/SDAPS/2024-1
	
- skeny přidat do projektu (může být na vícekrát, takže to nemusí být nutně jeden soubor), ideálně vytvořit podadresář a pomocí * hromadné přidání do jediného souboru (nejšikovnější způsob)

	sdaps add . --convert ./skeny/skeny1.tif
	sdaps add . --convert ./skeny/skeny1.pdf
	sdaps add . --convert ./skeny/*.tif
	
3. REKOGNICE
- provést to hlavní, tedy recognici zaškrtnutých políček ve formulářích (z adresáře projektu)

	sdaps recognize .


4. KONTROLA A EXPORT DAT
- provést grafickou kontrolu a případnou ruční úpravu rozpoznaných odpovědí (z grafického okna změny nutno uložit), dokud nezprovozníme čárové kódy a formuláře tisknuté na jméno, je také nutné přepisovat v tomto okně ID uchazeče do pole "ID uchazeče" - je to důležité pro rozlišení účastníků do výsledkové tabulky a smozřejmě to zabere určitý čas. Tlusté křížky SDAPS vyhodnocuje jako zrušené a náhodnou čárku může vyhodnotit jako chtěnou odpověď - kliknutím v GUI to lze opravit + ULOŽIT změny

	sdaps gui .

- nakonec vyexportovat textová data 

	sdaps export csv .

- v této fázi by měl jiný člověk udělat vizuální kontrolu všech formulářů ve znovu spuštěném gui - kontroluje u každého účastníka, že ID na skenu (levá polovina obrazovky) sedí s ID v datech (pravá polovina obrazovky) a taktéž zkontroluje zažlucené křížky, které program detekoval
- jakmile máme zkontrolovaná a čistá data v CSV, můžeme přistoupit k bodovému vyhodnocení skriptem


Bodové vyhodnocení formulářů
----------------------------
Připravený python skript pro potřeby vosplzen.cz na ploše a zde:
https://github.com/NeoFlint/sdaps_bodovani

případně kontakt: fictum.jiri@gmail.com


- pro podrobné informace viz README, základní princip je následující:
- připravit vstupní soubory data_sdaps.csv, spravne_odpovedi.ods a samotný skript zpracuj_sdaps.py

	data_sdaps.csv
	spravne_odpovedi.ods
	zpracuj_sdaps.py
	
- po spuštění skript vygeneruje novou excelovou tabulku vysledky.ods  
	
	python zpracuj_sdaps.py
	
- výsledkovou tabulku je nutno otevírat v Calcu a kamkoliv kopírovat nebo posílat v zašifrované podobě!
- na konec je nutná namátková kontrola výsledků - u 2 až 3 účastníků prostě formulář vyhodnotíme ručně a porovnáme s hodnotami v tabulce. 
