# 🚀 Projet de Surveillance Industrielle – Stage à Lafarge Holcim Bouskoura

Ce dépôt présente le projet que j’ai réalisé lors de mon stage d’initiation à l’usine **Lafarge Holcim Bouskoura**, dans le cadre de ma formation en **DUT Génie Informatique à l’EST Meknès**.

---

## 🔍 Contexte et problème détecté

Avant le développement de ce projet, la surveillance des équipements industriels était réalisée **manuellement par les employés** sur un ordinateur central contenant **des millions d’entités** à contrôler.  

Cette méthode présentait plusieurs limites :  
- Il fallait **faire défiler de longues pages** pour vérifier chaque variable, ce qui prenait beaucoup de temps.  
- Les employés pouvaient être **distraient** (appels, pauses, autres tâches), et donc **risquer de manquer des anomalies importantes**.  
- Aucun **système d’alerte automatique** n’était en place pour signaler rapidement un problème.  

---

## 🎯 Objectif du projet

Le projet a été conçu pour :  
- **Automatiser la surveillance en temps réel** des équipements via OPC UA  
- **Détecter immédiatement les anomalies** comparées aux seuils définis dans la base SQLite  
- **Notifier automatiquement** les alertes afin que rien ne passe inaperçu  
- **Faciliter l’analyse et le suivi** des incidents, sans dépendre de l’attention humaine constante  

Cette solution permet un **gain de temps significatif**, une **réduction des erreurs** et une **fiabilité accrue** de la surveillance industrielle.

---

## 🧠 Technologies utilisées

- **Python** (avec les bibliothèques `opcua`, `sqlite3`, `tkinter`, `logging`)  
- **OPC UA** pour la communication avec les automates industriels  
- **SQLite** pour la gestion locale des données et des alertes  
- **Interface Tkinter** pour la visualisation en temps réel  
- **Système de logs** et exportation en PDF  
- **Architecture modulaire** (scripts séparés : connexion, interface, alertes, logs, etc.)

---

## 🎥 Vidéo de démonstration

Cliquez sur l’image ci-dessous pour regarder la vidéo de présentation du projet :  

[![Regarder la vidéo sur YouTube](https://img.youtube.com/vi/dnU4mzOTyX0/0.jpg)](https://youtu.be/dnU4mzOTyX0)

---

## 📂 Structure du projet *(à venir)*

Le dépôt contiendra prochainement :  
- `main.py` → Script principal de surveillance  
- `interface/` → Interface graphique Tkinter  
- `database/` → Fichiers de base SQLite  
- `alerts/` → Gestion et historique des alertes  
- `logs/` → Enregistrements d’événements  
- `export/` → Génération des rapports PDF  

---

## 👩‍💻 Auteur

**Hiba Zitouni**  
Étudiante en **1ère année DUT Génie Informatique** – EST Meknès  
Stage d’initiation à **Lafarge Holcim Bouskoura**  
📅 **Période :** Juin – Juillet 2025  

---

## 🏅 Remerciements

Je tiens à remercier :  
- Mon encadrant professionnel à Lafarge Holcim pour son accompagnement et ses conseils  
- Mon encadrant pédagogique à l’EST Meknès pour son suivi  
- Et toute l’équipe de maintenance pour leur accueil et leur aide durant le stage

---

## 💡 Perspectives d’amélioration

- Ajout d’un **tableau de bord web** (visualisation via navigateur)  
- Intégration d’un **module d’analyse statistique des alertes**  
- Amélioration de l’interface graphique et de l’ergonomie  
- Déploiement sur un serveur local ou un mini-PC industriel (Raspberry Pi)

---
