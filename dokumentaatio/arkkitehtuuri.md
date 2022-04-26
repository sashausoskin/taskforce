# Arkkitehtuurikuvaus

## Käyttöliittymä

Ohjelmassa on kaksi pääikkunaa:
- Kirjautumisikkuna
- Tehtäväikkuna

Näistä näkyy vain yksi kerrallaan. Lisäksi on seuraavia ikkunoita, jotka voivat näkyä pääikkunoiden päällä:

- Tilinluonti
- Organisaation liittyminen
- Uuden organisaation luonti
- Uuden tehtävän luonti

Nämä ikkunat voivat ilmestyä eri vaiheissa käyttöä.

Käyttöjärjestelmän toiminta on pyritty eristämään mahdollisimman hyvin sovelluksen logiikasta vastaavasta koodista. Kaikki sovelluslogiikan toiminnat kutsutaan erilaisilla Serivce-luokkien metodeilla, jotka taas vastaavat sovelluslogiikasta.

Käyttöjärjestelmä muodostetaan pääosin kun käyttäjä kirjautuu sisään, tosin joitakin asioita voidaan päivittää kun Service-luokkien metodeja kutsutaan. Esimerkiksi jos käyttäjä merkitsee tehtävän valmiiksi, niin kutsutaan käyttöliittymän updateTasks(), joka rakentaa uudelleen tehtävälistan kutsumalla TaskService-luokan metodia get_tasks().

Kuvitellaan tilanne, jossa organisaation ylläpitäjä kirjautuu tililleen, jolla hän on jakanut tehtäviä sekä kommentoinut kyseisiä tehtäviä. Tällöin kirjautuessa käyttöliittymä piirtää kaikille annetuille tehtäville napit, piirtää näytölle tiedot sillä hetkellä valitusta tehtävästä, piirtää kommentit senhetkiselle tehtävälle. Lisäksi käyttöliittymä lisää yläpalkin valikkoihin napit organisaation valintaa varten sekä käyttäjien ylentämistä varten.

Ohjelmassa käytetään luokkia ´User´ ja ´Organizations´ kuvaamaan käyttäjiä ja organisaatioita, joihin käyttäjät voivat liittyä. Lisäksi on olemassa luokat Task ja Notification, jotka kuvaavat tehtäviä joita käyttäjät voivat saada sekä ilmoituksia, joita käyttäjälle voi tulla.

```mermaid
 classDiagram
      User "*" --> "*" Organization
      Task "2" --> "*" User
      Task "1" --> "*" Organization
      Notification "1" --> "*" User
      class User{
          id
          name
          username
          password
          organizations
      }
      class Organization{
          id
          name
          code
      }
      class Task{
      	title
      	desc
      	assigned_by
      	assigned_to
      	task_id
      	done
      }
      class Notification{
      	user
      	title
      	message
      	type
      }
```

# Sekvenssikaavio
Alla kuvataan kaksi ohjelman toiminnan kannalta tärkeää prosessia sekvenssikaavioina: sisäänkirjautuminen (olettaen että käyttäjä on olemassa) sekä tehtävän merkiseminen valmiiksi.

## Sisäänkirjautuminen
```mermaid
sequenceDiagram
  actor User
  participant loginWindow
  participant TaskforceService
  participant UserRepository
  participant OrgRepository
  User->>loginWindow: click "Login"
  loginWindow->>TaskforceService: login("user1", "1234")
  TaskforceService->>UserRepository: login("user1", "1234")
  UserRepository-->>TaskforceService: user
  TaskforceService->>OrgRepository: org_member(user.id)
  OrgRepository-->>TaskforceService: [org]
  TaskforceService-->>loginWindow: user
  loginWindow->loginWindow: MainWindow.show()
```

## Tehtävän merkitseminen valmiiksi
```mermaid
sequenceDiagram
  actor Member
  participant mainWindow
  participant TaskforceService
  participant TaskRepository
  Member->>mainWindow: click "Mark as done"
  mainWindow->>TaskforceService: mark_as_done(selected_task)
  TaskforceService->>TaskRepository: mark_as_done(task.task_id)
  mainWindow->>TaskforceService: get_name()
  TaskforceService-->>mainWindow: name
  mainWindow->>TaskforceService: send_notification(selected_task.assigned_to, "User {name} has finished a task", "done") 
  TaskforceService->>TaskRepository: send_notification(assigned_to.id, ""User {name} has finished a task", "done")
  mainWindow->>mainWindow: updateTasks()
  mainWindow-->>Member:sees the task as done
```
