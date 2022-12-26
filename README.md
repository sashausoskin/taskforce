# TaskForce

## Dokumentaatio

- [Käyttöohje](/dokumentaatio/kayttoohje.md)
- [Arkkitehtuurikuvaus](https://github.com/sonicsasha/taskforce/blob/master/dokumentaatio/arkkitehtuuri.md)
- [Muutosloki](https://github.com/sonicsasha/taskforce/blob/master/dokumentaatio/changelog.md)
- [Työaikakirjanpito](https://github.com/sonicsasha/taskforce/blob/master/dokumentaatio/tyoaikakirjanpito.md)
- [Vaatimuusmäärittely](https://github.com/sonicsasha/taskforce/blob/master/dokumentaatio/vaatimuusmaarittely.md)

## Julkaisut

- [Versio 0.1.0 (Viikon 5 palautus)](https://github.com/sonicsasha/taskforce/releases/tag/viikko5)

- [Versio 0.2.0 (Voidaan periaatteessa vieläkin laskea viikon 5 palautukseksi)](https://github.com/sonicsasha/taskforce/releases/tag/viikko5-v.0.2.0)

- [Versio 0.3.0 (Viikon 6 palautus)](https://github.com/sonicsasha/taskforce/releases/tag/viikko6)

- [Versio 1.0.0 (Loppupalautus)](https://github.com/sonicsasha/taskforce/releases/tag/viikko7)

## Projektista

Tämä on tietokoneella toimiva ohjelma, jolla voi luoda tilin, kirjautua kyseiselle tilille, luoda organisaatioita sekä liittyä muihin olemassaoleviin organisaatioihin koodilla. Organisaation ylläpitäjät pystyvät jakamaan muille organisaation jäsenille tehtäviä, joita jäsenet voivat sitten merkata valmiiksi. Aina kun käyttäjälle jaetaan tehtävä, niin hänelle annetaan aiheesta työpöytäilmoitus. Samoin tehdään tehtävän antajalle, kun tehtävä merkitään valmiiksi.

### Python-versio

Tämä projekti on toteutettu Python-versiolla 3.9.7. Vanhempien Python-versioiden käyttö voi vaiheuttaa ongelmia.

### Tietokannasta

Tämä projekti käyttää netissä olevaa PostgreSQL-tietokantaa, joten turvallisuussyistä linkkiä siihen ei ole sisällytetty repositoriossa. Linkki tietokantaan merkitään .env-tiedostoon parametrilla `DATABASE_URL`. Tilanteen voi korjata mm. näillä tavoilla:

1. Käytä paikallista tietokantaa. Jos olet esimerkiksi käyttänyt tsohan [asennusskriptiä](https://github.com/hy-tsoha/local-pg), niin voit luoda .env-tiedoston sekä kirjoittaa sinne `DATABASE_URL=postgresql+psycopg2://`
2. Luo itse buildi repositoriossa olevasta versiosta [GitHub Actionissa](https://github.com/sonicsasha/taskforce/actions/workflows/build.yml). Se sisältää viittaukset omaan netissä olevaan tietokantaan.
3. Kysy osoitetta Telegramissa [@sonicsasha](https://t.me/sonicsasha)

### Asennus

Projektin riippuvuudet saa asennettua komennolla
```bash
poetry install
```
**HUOM! Jos ohjelman suorittaa Linux-ympäristössä, niin PyQt5 täytyy asentaa apt:in kautta komennolla `sudo apt install python3-pyqt5`. Cubblissa tämän pitäisi olla jo valmiiksi asennettuna**

**HUOM nro 2! Joissakin tilanteissa paketin dbus-python asentaminen Linuxissa saattaa aiheuttaa virhetilanteen. Tätä pakettia tarvitaan, jotta työpöytäilmoitukset toimisivat Linuxissa. Linuxissa täytyy asentaa paketteja komennolla
`sudo apt install build-essential libpython3-dev libdbus-1-dev`. Näidenkin pakettien pitäisi Cubblissa olla jo asennettuna.**

Kun tietokannalle on annettu osoite, niin tietokannan voi alustaa komennolla
```bash
poetry run invoke init-db
```

**HUOM! Varmista, että olet antanut tietokannan osoitteen .env-tiedostossa ennen kuin suoritat tämän komennon**

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

**HUOM! Nämä testit suoritetaan tietokannassa, joten niiden suorittamisessa voi kestää jonkin aikaa.**

Ohjelman testien kattavuusraportin voi muodostaa komennolla

```bash
poetry run invoke coverage-report
```

QtDesignerilla tehdyt .ui-tiedostot voi muuttaa Python-koodiksi alla olevalla komennolla. Joka kerta kun käyttöliittymään tehdään muutoksia QtDesignerilla, niin tämä komento täytyy suorittaa.
```bash
poetry run invoke compile-ui
```

Pylint-testit pystyy tekemään komennolla
```bash
poetry run invoke lint
```

Ohjelmasta voi rakentaa itsenäisesti suoritettavan version käyttämällä komentoa
```bash
poetry run invoke build
```
Tämä kompiloi ohjelman dist-kansioon.
