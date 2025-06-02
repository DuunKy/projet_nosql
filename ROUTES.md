# 📊 API F1 – Routes disponibles

## 🧩 Basics API (`/api/v1`)

| #  | Endpoint                 | Method | Query Params              | Description                              |
|----|--------------------------|--------|---------------------------|------------------------------------------|
| 1  | `/seasons`               | GET    | `year`                    | Liste ou détail des saisons              |
| 2  | `/circuits`              | GET    | `id`                      | Liste ou détail des circuits             |
| 3  | `/races`                 | GET    | `id`, `season`            | Courses pour un circuit et/ou une saison |
| 4  | `/drivers`               | GET    | `id`                      | Liste ou détail des pilotes              |
| 5  | `/constructors`          | GET    | `id`                      | Liste ou détail des écuries              |
| 6  | `/results`               | GET    | `id`                      | Résultats de course                      |
| 7  | `/qualifying`            | GET    | `id`                      | Résultats de qualification               |
| 8  | `/pitstops`              | GET    | `raceid`, `stop`          | Détails des arrêts au stand              |
| 9  | `/lap-times`             | GET    | `raceid`, `driver`, `lap` | Temps au tour                            |
| 10 | `/driver-standings`      | GET    | `id`                      | Classement des pilotes                   |
| 11 | `/constructor-standings` | GET    | `id`                      | Classement des écuries                   |
| 12 | `/constructor-results`   | GET    | `id`                      | Résultats constructeur                   |
| 13 | `/sprint-results`        | GET    | `id`                      | Résultats des sprints                    |

---

## 📈 Stats API (`/api/v1`)

| #  | Endpoint                                 | Method | URL/Query Params                                                | Description                        |
|----|------------------------------------------|--------|-----------------------------------------------------------------|------------------------------------|
| 1  | `/teams/<constructorId>/performance`     | GET    | `season`                                                        | Évolution performance d'une écurie |
| 2  | `/seasons/<year>/constructors/standings` | GET    | –                                                               | Classement final des écuries       |
| 3  | `/constructors/<id>/top-drivers`         | GET    | `season`                                                        | Pilotes les plus performants       |
| 4  | `/constructors/<id>/<circuit>/lap-times` | GET    | `circuit`, `season` ***(required)***, `driver` ***(required)*** | Temps au tour sur circuit          |
| 5  | `/constructors/<id>/retirements`         | GET    | `season` ***(required)***                                       | Nombre d’abandons                  |
| 6  | `/constructors/<id>/qualif-vs-race`      | GET    | `season`, `driver`                                              | Comparaison qualifs vs course      |
| 7  | `/constructors/<id>/pitstops`            | GET    | `season`                                                        | Stats arrêts au stand              |
| 8  | `/constructors/compare`                  | GET    | `ids[]`, `season`                                               | Comparaison multi-écuries          |
| 9  | `/constructors/<id>/top-circuits`        | GET    | `season`, `driver`                                              | Circuits favoris                   |
| 10 | `/constructors/<id>/driver-averages`     | GET    | `season`, `circuit`                                             | Moyenne de points pilote/course    |
| 11 | `/constructors/<id>/grid-stats`          | GET    | `season`, `driver`, `circuit`                                   | Moyenne position départ            |
| 12 | `/constructors/<id>/podium-ratio`        | GET    | `season`                                                        | Ratio podiums / courses            |
| 13 | `/constructors/<id>/sprint-laps`         | GET    | `season`, `driver`, `circuit`                                   | Temps moyen en sprint              |
| 14 | `/constructors/<id>/standing-evolution`  | GET    | `season` ***(required)***                                       | Évolution du classement            |
| 15 | `/constructors/<id>/full-comparison`     | GET    | `season`, `driver`                                              | Comparaison qualif/sprint/course   |
