# 📊 Besoins Statistiques d'une Écurie de Formule 1

Ce document présente une liste de 15 besoins statistiques qu'une écurie de Formule 1 peut analyser à partir des données disponibles dans la base.

---

## 🏎️ 1. Performance du Véhicule

1. **Temps moyen au tour par pilote et par course**  
   _Source : `LapTime`, `Race`, `Driver`_  
   Permet d’évaluer la régularité des performances sur une course complète.

2. **Évolution du temps au tour (delta)**  
   _Source : `LapTime`_  
   Utile pour détecter l’usure des pneus ou une dégradation des performances.

3. **Analyse des arrêts aux stands**  
   _Source : `PitStop`, `Constructor`_  
   Moyenne et nombre d’arrêts par écurie, durée, et régularité.

4. **Taux d’abandon**  
   _Source : `Result`, `Status`_  
   Nombre de courses non terminées, par pilote ou par écurie.

---

## 👨‍✈️ 2. Pilotage

5. **Écart grille de départ / arrivée**  
   _Source : `Result`_  
   Analyse des positions gagnées ou perdues pendant une course.

6. **Comparaison qualif/course**  
   _Source : `Qualifying`, `Result`_  
   Évalue l'efficacité du pilote à convertir une bonne qualification en résultat.

7. **Meilleur pilote par course (intra-écurie)**  
   _Source : `Result`, `Constructor`_  
   Identifier les leaders au sein de chaque équipe.

---

## 🧠 3. Stratégie de Course

8. **Tours moyens entre deux arrêts aux stands**  
   _Source : `PitStop`_  
   Aide à l’optimisation des stratégies d’arrêt.

9. **Nombre d’arrêts par course et par pilote**  
   _Source : `PitStop`, `Driver`, `Race`_  
   Données utiles pour l’analyse stratégique globale.

10. **Écart d’arrivée entre les deux pilotes d’une écurie**  
    _Source : `Result`, `Constructor`_  
    Permet de mesurer la cohérence des performances au sein de l’équipe.

---

## 📊 4. Performance Globale

11. **Classement constructeur par saison**  
    _Source : `ConstructorStandings`_  
    Classement final, analyse des écarts et des tendances par saison.

12. **Évolution du score pilote au fil de la saison**  
    _Source : `DriverStandings`, `Race`, `Season`_  
    Utile pour évaluer les progressions et baisses de forme.

13. **Nombre de victoires**  
    _Source : `Result`_  
    Par pilote ou par constructeur (`position = 1`).

14. **Analyse des positions de départ**  
    _Source : `Result.grid`_  
    Statistiques sur les grilles de départ pour stratégie qualif.

15. **Circuits favoris par écurie**  
    _Source : `Result`, `Constructor`, `Race`, `Circuit`_  
    Classement des circuits où chaque écurie performe le mieux.

---

## ✅ Remarques

- Toutes les analyses ci-dessus peuvent être effectuées à partir du modèle relationnel actuel.
- L’usage de jointures est indispensable pour relier les entités comme `Race`, `Driver`, `Constructor`, etc.
- Ces indicateurs sont essentiels pour alimenter des tableaux de bord F1, optimiser les stratégies et améliorer la compétitivité.

---

