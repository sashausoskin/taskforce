# Käyttöohje

## Konfigurointi
Tällä hetkellä ainoa asia, jonka ohjelmassa voi kondiguroida, on PostgreSQL-tietokannan osoite. Tietokannan osoite tallennetaan .env-tiedostoon parametrilla `DATABASE_URL`. Tiedostoa ei ole sisällytetty repositorioon, joten tiedosto täytyy luoda itse. Tiedoston sisältö voisi siis olla esimerkiksi seuraava:
```
DATABASE_URL=postgres://
```

## Ohjelman käynnistäminen lähdekoodista

Ohjelman riippuvuudet saa asennettua komennolla
```bash
poetry install
```
**HUOM! Paketin dbus-python asennus saattaa aiheuttaa virheen. Tämän voi jättää huomiotta. Lisäksi Linuxissa PyQt5 täytyy asentaa erikseen. Lisätietoa löytyy [README](https://github.com/sonicsasha/taskforce#readme):sta**

Kunhan tietokannalle on annettu osoite, niin tietokannan saa alustettua komennolla
```bash
poetry run invoke init-db
```

Tämän jälkeen ohjelman saa käynnistettyä komennolla
```bash
poetry run invoke start
```

## Kirjautuminen

**Alla olevat videot on kuvattu versiolla 0.4.0, joten tämänhetkinen käyttöliittymä voi erota videoiden käyttöliittymästä.**

Kirjautuminen tapahtuu syöttämällä käyttäjän käyttäjänimi ja salasana kenttiin ja painamalla "login"

![](https://github.com/sonicsasha/taskforce/blob/master/dokumentaatio/mov/login.mp4)

## Käyttäjän luominen

Uusi käyttäjä luodaan painamalla "signup" ja täyttämällä näytölle tuleva lomake
![](https://github.com/sonicsasha/taskforce/blob/master/dokumentaatio/mov/signup.mp4)

## Uuden organisaation luonti

Jos käyttäjä ei ole liittynyt mihinkään organisaatioon, niin kirjautuessa tulee näkyviin liittymisikkuna. Muissa tapauksissa ikkunan saa näkyville yläpalkista "Organizations" -> "Join an organization or create a new one". Tämän jälkeen organisaation saa luotua klikkaamalla "Create a new organization" ja täyttämällä näkyvillä olevan lomakkeen.
![](https://github.com/sonicsasha/taskforce/blob/master/dokumentaatio/mov/create_org.mp4)

## Organisaatioon liittyminen

Kun käyttäjä pääsee samaan ikkunaan kuin organisaation luonnin vaiheessa, niin organisaatioon liittyminen tapahtuu kirjoittamalla syötteeseen organisaation liittymiskoodi ja klikkaamalla "Join organization".
![](https://github.com/sonicsasha/taskforce/blob/master/dokumentaatio/mov/join_org.mp4)

## Organisaation vaihtaminen

Jos käyttäjä on jäsenenä useammassa organisaatiossa, niin aktiivisen organisaation voi vaihtaa yläpalkista "Organizations" -> "Change current organization"

## Tehtävän jakaminen

Organisaation ylläpitäjä voi jakaa tehtävän valitsemalla yläpalkista "Tasks" -> "Assign a new task", ja täyttämällä tehtävän tiedot.
![](https://github.com/sonicsasha/taskforce/blob/master/dokumentaatio/mov/assign_task.mp4)

## Kommentointi sekä tehtävän merkitseminen valmiiksi

Kommentin voi jättää kirjoittamalla kommenttikenttään ja klikkaamalla "Post a comment". Tehtävän voi merkitä valmiiksi klikkaamalla "Mark as done".

## Käyttäjän ylentäminen

Ylläpitäjä voi ylentää muun käyttäjän ylläpitäjäksi klikkaamalla "Organizations" -> "Assign a member as admin"

![](https://github.com/sonicsasha/taskforce/blob/master/dokumentaatio/mov/signup.mp4)
