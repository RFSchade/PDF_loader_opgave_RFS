
# Program til at downloade pdf-filer fra links i en excel fil 

Med dette program kan du downloade store mængder af pdf-filer ved at specificere store et id, 
et url og et alternativt url i en excel fil. Programmet producere også en excel fil med en 
oversigt over, hvilke pdf-filer er downloadede, og hvilke ikke er.    

Programmet tager lang tid at køre med meget store datamængder - jeg anbefaler at lade det køre 
hen over natten første gang, og at løbende fjerne/rette rækker med filer der ikke bliver 
downloadet i excel-filen.     

Der er to forskellige versioner af programmet. Generelt anbefaler jeg at anvende 
“download_multithreading.py”, men hvis din computer har 10 eller flere logiske processorer, 
kan det betale sig at bruge “download_multiprocessing.py” i stedet for (se afsnitet 
“logiske processorer” for mere information).     

### Repository struktur
__input:__ Mappe til input data. Her skal Excel filen med listen over PDF’er skal gemmes. 
Når programmet har kørt kommer denne mappe også til at indeholde en CSV version af 
Excel filen (pdf_list.csv).     
 
__output:__ Mappe til output fra python scriptet. Kommer til at indeholde Excel-filen 
”Download_liste.xlsx”, som er en liste over alle filer specificeret i input filen, med en 
kolonne der viser om de er downloadede eller ej.    
- Pdfs: Mappe til downloadede PDF’er.
 
__src:__ Mappe til Python scripts
- \_\_init__.py
- download_multiprocessing.py: Python script der downloader PDF-filer med multiprocessing.
- download_multithreading.py: Python script der downloader PDF-filer med multithreading.

requirements.txt: txt fil med liste over python moduler der er nødvendige at installere for at 
køre scriptet.     

readme.txt: readme i txt format til hvis brugeren ikke kan læse markdowns.    

### Logiske processorer
Programmet “download_multiprocessing.py” downloader PDFer hurtigere ved at fordele arbejdet på flere 
af din computers logiske processorer. Hvis din computer har 10 eller flere, kan det gå hurtigere at 
køre “download_multiprocessing.py” end “download_multithreading.py”.      

Du kan finde ud af, hvor mange logiske processorer en computer med windows 10 har, ved at trykke 
CTRL + Skift + ESC for at åbne joblisten, gå ind under “ydeevne” fanen og  klikke på “CPU”, hvor det 
står under “logiske processorer”.     

### Brug
Koden er skrevet til Python 3.11.1. 
Modulerne anført i requirements.txt skal installeres, før scripts køres. Du kan tjekke om der er nogle 
af modulerne du mangler at installere ved at give følgende command i din shell eller terminal: 
	
	pip freeze -r requirements.txt

Du kan installere alle modulerne på listen ved at skrive: 

	pip install -r requirements.txt

#### download_multiprocessing.py 	
Kør scriptet fra repository-mappen (PDF_loader_opgave_RFS) for at downloade PDF’erne 
med multiprocessing.     

Programmet skal bruge en Excel fil med en ID kolonne, en kolonne med et url der leder hen til PDF-filen, 
og en kolonne med et ‘backup’ URL hvis det første ikke virker. Det er vigtigt at disse kolonner er 
navngivet henholdsvist “BRnum”,  “Pdf_URL” og “Report Html Address”.    

Scriptet har 1 argument: 	
- -f eller --file: Navnet på ‘input’ excel filen - default er “GRI_2017_2020 (1).xlsx”. 
Husk at tilføje ‘.xlsx’ til filnavnet. Jeg anbefaler at scriptet ikke indeholder bindestreger. 

Eksempel på kode, der kører scriptet fra terminalen:	

	python src/download_multiprocessing.py -f GRI_2017_2020 (1).xlsx

Uden argument:

	python src/download_multiprocessing.py

#### download_multithreading.py 	
Kør scriptet fra repository-mappen (PDF_loader_opgave_RFS) for at downloade PDF’erne 
med multithreadng. 

Programmet skal bruge en Excel fil med en ID kolonne, en kolonne med et url der leder hen til PDF-filen, 
og en kolonne med et ‘backup’ URL hvis det første ikke virker. Det er vigtigt at disse kolonner er 
navngivet henholdsvist “BRnum”,  “Pdf_URL” og “Report Html Address”.

Scriptet har 1 argument: 	
- -f eller --file: Navnet på ‘input’ excel filen - default er “GRI_2017_2020 (1).xlsx”. 
Husk at tilføje ‘.xlsx’ til filnavnet. Jeg anbefaler at scriptet ikke indeholder bindestreger. 

Eksempel på kode, der kører scriptet fra terminalen:	

	python src/download_multithreading.py -f GRI_2017_2020 (1).xlsx

Uden argument:

	python src/download_multithreading.py

### Designovervejelser
Som minimum valgte jeg at programmet skulle have følgende features - det skal kunne:  
- Gennemgå en liste af PDF-filer og downloade dem via en URL
- Bruge en backup URL hvis filen ikke kan downloades via den første
- Navngive de gemte filer efter en ID-kolonne (BRnum)
- Lave en liste over hvilke rapporter der er downloadede, og hvilke der ikke er
- Programmet skal kunne køres via command-linjen.

Programmet skulle kunne uden meget teknisk viden eller erfaring. For at imødekomme det har jeg valgt 
at gøre det muligt at køre programmet uden argumenter, og at downloade listen over PDF-filer fra 
en .xlsx fil, i stedet for en CSV eller python pickle fil, som ville have været hurtigere.  
Jeg har også valgt at gøre programmet er ”chatty” – der bliver altså printet beskeder om, hvad der 
foregår i terminalen. ID’et på en PDF vises på terminalen når den behandles af programmet. Dette er også 
et forsøg på at imødekomme kundens ønske om at programmet skulle være mindre “ustabilt”.      
Mens den direkte dokumentation af koden, og programmet i sig selv er på engelsk, har jeg valgt at skrive 
README-filen og listen over downloadede PDF’er på dansk.     

Kunden nævnte også, at det program de tidligere har brugt var langsomt, så jeg har også prioriteret at 
gøre programmet hurtigere.     
Jeg har forsøgt at gøre dette ved at konvertere listen over PDF - filer en CSV-fil før den loades ind til 
programmet, kun loade de tre nødvendige kolonner, og kun importere de nødvendige funktioner i stedet for 
hele moduler.     
Ud over det har jeg også forsøgt at ikke at sende en HTML requests uden et URL, fjerne duplikater (både 
blandt ID’er og de to URL’er), springe filer over der allerede er downloadede, sortere svar på requests 
der ikke er PDF’er fra før de downloades, og undgå globale variabler.     
Jeg har også prøvet at erstatte for-oops med list-comprehensions, og if-statements med dictionaries. 
Når jeg kan her jeg erstattet dem med list-comprehensions.    

Jeg har også haft det i tankerne, at programmet skal kunne bruges igen til andre projekter, af andre folk. 
Derfor har jeg valgt at give det et enkelt argument der gør det muligt at vælge en anden input fil. 
De kolonner der loades ind i programmet vælges med deres navn, og ikke deres position i datasættet.
Der er lavet to scripts for at give mere fleksibilitet, så hastigheden ikke udelukkende er afhængig 
af hvilken computer programmet køres på.     

### Hvad kunne gøres bedre?
1) Selv med multithreading eller multiprocessing er programmet er stadig langsomt. Det tager i hvert fald 2 timer at downloade 
   alle PDF'er i det fulde datasæt.  
   
2) Da jeg skrev programmet Har jeg ikke prioriteret min tid ideelt – mange af de små ændringer jeg 
   har lavet i koden har måske skåret et nogle millisekunder af tiden det tager at køre koden.
   Over mange iterations gør det en lille forskel, men jeg tror jeg ville kunne gøre det endnu hurtigere 
   hvis jeg havde brugt mere tid på multiprocessing.     
   Programmet udsteder flere opgaver på én gang, men jeg kan læse på dokumentation for 
   “multiprocessing”-modulet, at det er muligt at gøre det på flere forskellige måder. Måske kunne jeg 
   have øget hastigheden ved at arbejde med det?  

3) Hvis man kører programmet igen med nogle flere filer i excel arket, vil programmet stadig forsøge at 
   downloade de filer, som den fejlede med at downloade før, og som slap forbi filtrering.

4) Det kunne være rart med en progress - bar.

5) Det virker som om, noget af det der får programmet til at tage lang tid er at gemme PDF’erne på computere. 
   Måske Kunne jeg have fundet en hurtigere måde at gemme dem på.  

6) Jeg kunne have sørget for, at det ville være nok at skrive filnavnet uden .xlsx når man vælger fil.
   Jeg tog mig selv i at glemme det, og det er nok også den slags fejl man kunne have lavet, hvis man var 
   mindre teknisk anlagt.

7) Jeg har forsøgt at gøre noget ved det ved at tilføje til dokumentationen, men Hvis kunden ikke er teknisk 
   kyndig kan det være svært at finde ud af hvor mange cores en computer har (og finde ud af hvilket script 
   der kan betale sig bedst på en bestemt maskine). 
   Nogle af de små ting jeg har gjort for at optimere min koden hastighed (f.eks. at bruge dictionaries i 
   stedet for if-statements) har gjort min kode lidt mindre “pythonic” - altså lidt svær at læse.

8) Det kunne være rart hvis jeg havde haft mulighed for at have lavet en mere præcis test af hastigheden på 
   de to scripts - hvor mange kerner skal en computer helt præcist have, før det bedre kan betale sig at 
   bruge multiprocessing-scriptet? Bliver der sparet mere tid, når datasættet er større? Hvad er den ideelle 
   størrelse? 

9) En del PDF-filer bliver filtreret ud af datasættet før der bliver sendt en HTML request - ville det have 
   været bedre hvis programmet kunne informere brugeren om, hvilke filer blev sorteret fra og for hvilke 
   grunde? 

10) Navne på nogle af de kolonner der bliver brugt fra det input-filen er lidt uhensigtsmæssige (ikke 
   informative, brug af mellemrum ikke konsistent formatering). Da Disse kolonner importeres baseret på 
   deres navn, ville et fremtidigt datasæt også skulle bruge samme navne. Det er dog bedre end at de skulle 
   bruge samme placering, hvilket var det eneste alternativ jeg kunne komme i tanke om.
 
11) Dokumentationen antager at dem der skal bruge programmet bruger Windows 10, og at de kan navigere og 
    kalde programmer via Shellen. 

