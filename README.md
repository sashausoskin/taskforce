# TaskForce

## Tehtävät

### Viikko 1

[gitlog.txt](https://github.com/sonicsasha/taskforce/blob/master/laskarit/viikko1/gitlog.txt)

[komentorivi.txt](https://github.com/sonicsasha/taskforce/blob/master/laskarit/viikko1/komentorivi.txt)

### Viikko 2
[Työaikakirjanpito](https://github.com/sonicsasha/taskforce/blob/master/dokumentaatio/tyoaikakirjanpito.md)

[Vaatimusmäärittely](https://github.com/sonicsasha/taskforce/blob/master/dokumentaatio/vaatimuusmaarittely.md)

## Projektista

Tämä on tietokoneella toimiva ohjelma, jolla tällä hetkellä voi ainoastaan luoda tilin sekä kirjautua kyseiselle tilille.

### Python-versio

Tämä projekti on toteutettu Python-versiolla 3.9.7. Vanhempien Python-versioiden käyttö voi vaiheuttaa ongelmia.

### Tietokannasta

Tämä projekti käyttää netissä olevaa PostgreSQL-tietokantaa, joten turvallisuussyistä linkkiä siihen ei ole sisällytetty repositoriossa. Linkki tietokantaan on sisällytetty .env-tiedostoon parametrilla ```DATABASE_URL```. Tilanteen voi korjata mm. näillä tavoilla:

1. Käytä paikallista tietokantaa.
2. Luo oma netissä oleva tietokanta itse (esim. [Heroku](https://www.heroku.com/postgres) ja [ElephantSQL](https://www.elephantsql.com/))
3. Kysy osoitetta Telegramissa [@sonicsasha](https://t.me/sonicsasha)

Tätä ongelmaa ei pitäisi olla lopullisessa buildissa.

### Asennus

Projektin riippuvuudet saa asennettua komennolla
```bash
poetry install
```

Kun tietokannalle on annettu osoite, niin tietokannan voi alustaa komennolla
```bash
poetry run invoke init-db
```

Ohjelman voi käynnistää komennolla
```bash
poetry run invoke start
```

### Komentorivikomennot
Ohjelma käynnistetään komennolla
```bash
poetry run invoke start
```

Ohjelman testit suoritetaan komennolla
```bash
poetry run invoke test
```

QtDesignerilla tehdyt .ui-tiedostot voi muuttaa Python-koodiksi alla olevalla komennolla. Joka kerta kun käyttöliittymään tehdään muutoksia QtDesignerilla, niin tämä komento täytyy suorittaa.
```bash
poetry run invoke compile-ui
```

Ohjelmasta voi rakentaa itsenäisesti suoritettavan komennon käyttämällä komentoa 
```bash
poetry run invoke build
```
Tämä kompiloi ohjelman dist-kansioon. **Huom! Tämä toiminto ei ole vielä viimeistelty, joten toistaiseksi ohjelma ei välttämättä toimi oikein. Tämä todennäköisesti vaatii myös tietokannan osoitteen kovakoodauksen koodiin.**


