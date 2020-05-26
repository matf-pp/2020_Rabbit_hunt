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

  Takođe je moguće i podešavati brzinu kojom se lisica i zec kreću. Brzina simulacije naravno ne utiče na sam ishod.

Kada se igrica završi pritiskom na (r) igrica se ponovo pokreće a na (q) se prekida sa radom.

                                  
Duži opis igre
-----------------

Za početak, objasnimo preciznije kako igra funkcioniše. Lisica i zec se kreću po tabeli dimenzija 25x25. Na toj tabeli se nalazi 60 žbunova, koje predstavlja prepreke. Lisica i zec naizmenično prave korake, pri čemu lisica pravi prvi korak. Korak znači pomeraj za jedno polje gore, dole, levo ili desno. Dakle, nema dijagonalnih koraka. Na početku igre, pozicije lisice i zeca se biraju nasumično, ali tako da su uvek na razdaljini 7 i tako da se vide. Definišimo sada šta znači to da se lisica i zec vide. Matematički formalno, lisica i zec se vide ukoliko duž koja spaja središta polja na kojima se oni nalaze ne seče unutrašnjost ni jednog polja na kom se nalazi žbun. Razlog zbog kog se uvek vide na početku igre je zbog toga što mislimo da je simulacija interesantnija, a razdaljina je izabrana uz jedini neophodan kriterijum da bude neparna, uzimajući u obzir da lisica igra prva.

Prilikom testiranja primetili smo zanimljivu stvar. Za relativno male promene gustine žbunova, verovatnoća sa kojom zec pobeđuje se neznatno menja ali u ekstremnim slučajevima dolazi do velikih promena nepovoljnih po zeca. To je i prikazano na sledećem histogramu:
<p align="center">
  <img width="261" height="253"  src= images/br_zbunova3D.png>
</p>

<p align="center">
 x osa predstavlja broj žbunova  
</p>



U zavisnosti od početne razdaljine lisice i zeca verovatnoća sa kojom zec pobeđuje se takođe neznatno menja. No, ono što se menja je broj partija u kojima zec pogine na samom početku. Pri maloj udaljenosti lisice i zeca dešava se da, ma koliko naš zec pametan bio prosto dolazi do neminovnog kraja. Sledeći dijagram upravo to i demonstrira :

<p align="center">
  <img width="261" height="253"  src= images/statistika2.png>
</p>

<p align="center">
 x osa predstavlja početnu udaljenost lisice i zeca
</p>




Predstavimo sada kako se kreće lisica. Ukoliko lisica vidi zeca, lisica traži najkraći put do tog polja na kome nema žbunja, i u većini situacija bira da napravi korak koji odgovara tom putu. Ako ga ipak ne vidi, ona traži put do polja gde je poslednji put videla zeca. Ovaj put je tražen koristeći algoritmom A* pri čemu je korišćena heuristika Euklidsko rastojanje. Primetimo da lisici dajemo prednost, jer joj na neki način dozvoljavamo da zna kako izgleda raspored žbunja. U malom broju situacija, preciznije u 1%, lisica pravi nasumičan korak. Moglo bi se postaviti pitanje zašto ovo lisica ne radi u baš svim situacijama. Ispostavlja se da ova nepredvidivost može zbuniti zeca u odredjenim situacijama.

Pre opisa algoritma po kojem se zec kreće, napomenimo da mu ovaj algoritam značajno povećava šanse za pobedu. Naime, prilikom pokretanja programa 10 000 puta pri nasumičnom kretanju zec nijednom nije uspeo da pobedi, a medijana broja koraka sa kojim se igra završava je 8. 

Primenom algoritma koji sledi šanse zeca da dođe do pobede su oko 42% dok je medijana broja koraka sa kojim se igra završava 154. 


Zec u svakom trenutku bira polje na koje će preći. Postoje polja koja ne dolaze u obzir - polja na kojima je žbunje, polja koja su na udaljenosti 1 od lisice ili koja su ćorsokak. Od preostalih polja, zec bira jedno, nazovimo ga potencijalno polje, na osnovu sledećih faktora:
1) udaljenost potencijalnog polja od lisice
2) udaljenost potencijalnog polja od centra tabele
3) broj "dobrog" žbunja koje je bliže potencijalnom polju, nego lisici
4) broj žbunja s kojim se graniči potencijalno polje
5) da li je potencijalno polje vidljivo sa polja gde je lisica trenutno

Ostali smo još dužni da objasnimo šta je dobro žbunje. Žbunje je dobro ukoliko se može zaobići, odnosno ukoliko postoji putanja oko tog žbunja. Formalno matematički, žbun nije dobar ako se graniči sa ivicom tabele, ili ako ima zajedničku tačku sa nekim drugim žbunom koji nije dobar. Dakle, na osnovu prethodno navedenih faktora, računa se cena polja, i bira se polje sa najmanjom cenom.

Pitanje je: koliko je svaki od ovih faktora bitan u proceni kretanja zeca?

Nakon brojnih testiranja zaključak je sledeći: zec postiže najbolje rezultate kada pri donošenju odluke o sledećoj poziciji favorizuje izbegavanje kretanje po samim obodima table u odnosu na ostale faktore.


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
