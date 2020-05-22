# Rabbit hunt

Kratak opis igre
-----------------

Lisica juri zeca po terenu koji sadrži žbunje koje može da blokira pogled lisici do zeca i obrnuto. Lisica pokušava da uhvati zeca dok zec pokušava da joj pobegne. Ukoliko lisica uhvati zeca, pobeđuje. Ako zec ne bude uhvaćen u 200 poteza, on pobeđuje. Lisica i zec su na početku postavljeni na unapred zadato rastojanje bilo gde na polju. Na primer: 



<p align="center">
  <img width="498" height="607"  src= images/pocetna.png>
</p>

<p align="center">
 Lisica je narandžasti trouglić dok je zec beli kvadratić
</p>



 Naš zadatak je bio da napravimo što pametnijeg zeca odnosno da smislimo algoritam pomoću kog će zec što češće pobediti u igri. 
   
Klikom na odgovarajuće dugme, moguće je:


* ![](images/run.png)  Pokrenuti animaciju.

* ![](images/stop.png)  Pauzirati animaciju.

* ![](images/step.png)  Pratiti kretanje lisice i zeca korak po korak. Jednim klikom, i zec i lisica prave po jedan korak.

* ![](images/reset.png)  Započeti igricu od početka, odnosno na teren opet postaviti žbunje, lisicu i zeca.

* ![](images/replay.png)  Vratiti se korak u nazad. Vraćanjem u nazad, igra se ne mora nužno odvijati isto.

  Takođe je moguće i podešavati brzinu kojom se lisica i zec kreću.

Kada se igrica završi pritiskom na (r) igrica se ponovo pokreće a na (q) se prekida sa radom.

                                  
Algoritam
-----------------

Za početak, objasnimo kada se lisica i zec vide i na koji način lisica juri zeca. Matematički formalno, lisica i zec se vide ukoliko duž koja spaja središta polja na kojima se oni nalaze ne seče unutrašnjost ni jednog polja na kom se nalazi žbun. Na početku igre, lisica i zec se postavljaju tako da se vide i da su na razdaljini 7. Razlog zbog kog se uvek vide na početku igre je zbog toga što mislimo da je simulacija interesantnija, a razdaljina je izabrana uz jedini neophodan kriterijum da bude neparna.

Ukoliko lisica vidi zeca, lisica traži najkraći put do tog polja na kome nema žbunja, i u većini situacija bira da napravi korak koji odgovara tom putu. Ako ga ipak ne vidi, ona traži put do polja gde je poslednji put videla zeca. Ovaj put je tražen koristeći algoritmom A* pri čemu je korišćena heuristika Euklidsko rastojanje. Primetimo da lisici dajemo prednost, jer joj na neki način dozvoljavamo da zna kako izgleda raspored žbunja. U malom broju situacija, preciznije u 10%, lisica pravi nasumičan korak. Moglo bi se postaviti pitanje zašto ovo lisica neadi u baš svim situacijama. Ispostavlja se da ova nepredvidivost može zbuniti zeca u odredjenim situacijama.

Zec u svakom trenutku bira polje na koje će preći. D


Jezici i tehnologije korišćene u izradi
---------------------------------------
Program je napisan u jeziku Python3, a od okruženja su korišćeni Visual Studio Code i PyCharm.

Za vizelizaciju korišćen je modul pygame, a osim toga korišćeni su i moduli heapq, collections i numpy. 

Pokretanje
----------
Izvršni fajl je napravljen za operativni sistem Windows.

Potrebno je preuzeti RabbitHunt.exe iz sekcije releases. Pokretanjem RabbitHunt.exe fajla u izabranom folderu kreiraće se novi folder pod nazivom RabbiitHunt. Unutar tog foldera dostupna je simulacija. 


Autori
-------

* Katarina Branković
    katarinab70@gmail.com

* Jana Vučković
    jana.vuck@gmail.com

* Marko Popović
    popsgljb@gmail.com
