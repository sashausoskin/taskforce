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

**Alla olevat videot on kuvattu versiolla 0.3.0, joten tämänhetkinen käyttöliittymä voi erota videoiden käyttöliittymästä.**

Kirjautuminen tapahtuu syöttämällä käyttäjän käyttäjänimi ja salasana kenttiin ja painamalla "login"


https://user-images.githubusercontent.com/9552313/165907412-91abf910-0bd3-4376-917f-d54c93335e06.mp4




## Käyttäjän luominen

Uusi käyttäjä luodaan painamalla "signup" ja täyttämällä näytölle tuleva lomake

https://user-images.githubusercontent.com/9552313/165907488-28e89c1e-3a14-4e21-9756-f26a15a6fc45.mp4



## Uuden organisaation luonti

Jos käyttäjä ei ole liittynyt mihinkään organisaatioon, niin kirjautuessa tulee näkyviin liittymisikkuna. Muissa tapauksissa ikkunan saa näkyville yläpalkista "Organizations" -> "Join an organization or create a new one". Tämän jälkeen organisaation saa luotua klikkaamalla "Create a new organization" ja täyttämällä näkyvillä olevan lomakkeen.

https://user-images.githubusercontent.com/9552313/165907570-36711ac9-aa85-42ac-ac8b-916159022789.mp4

## Organisaatioon liittyminen

Kun käyttäjä pääsee samaan ikkunaan kuin organisaation luonnin vaiheessa, niin organisaatioon liittyminen tapahtuu kirjoittamalla syötteeseen organisaation liittymiskoodi ja klikkaamalla "Join organization".

https://user-images.githubusercontent.com/9552313/165907610-472bb416-6ffd-4316-abc5-76590092053c.mp4

## Organisaation vaihtaminen

Jos käyttäjä on jäsenenä useammassa organisaatiossa, niin aktiivisen organisaation voi vaihtaa yläpalkista "Organizations" -> "Change current organization"

## Tehtävän jakaminen

Organisaation ylläpitäjä voi jakaa tehtävän valitsemalla yläpalkista "Tasks" -> "Assign a new task", ja täyttämällä tehtävän tiedot.

https://user-images.githubusercontent.com/9552313/165907635-04f7ffb8-2974-45fe-aecb-7dba50ed0f4a.mp4


## Kommentointi sekä tehtävän merkitseminen valmiiksi

Kommentin voi jättää kirjoittamalla kommenttikenttään ja klikkaamalla "Post a comment". Tehtävän voi merkitä valmiiksi klikkaamalla "Mark as done".

https://user-images.githubusercontent.com/9552313/165907671-f88f3b82-80c9-47d2-b708-1028aa6ca733.mp4

## Käyttäjän ylentäminen

Ylläpitäjä voi ylentää muun käyttäjän ylläpitäjäksi klikkaamalla "Organizations" -> "Assign a member as admin"

https://user-images.githubusercontent.com/9552313/165907702-a2efe934-e34b-4e00-9388-3c17e21fb2ed.mp4
