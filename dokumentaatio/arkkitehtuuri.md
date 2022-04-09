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
