# Pont Chaban Delmas pour Home Assistant

[![License](https://img.shields.io/github/license/lightd31/Chaban.svg)](https://github.com/lightd31/Chaban/blob/main/LICENSE)

## Description

Le composant Home Assistant "Chaban Bridge" permet de surveiller les fermetures et réouvertures du pont Chaban-Delmas à Bordeaux. Il utilise les données ouvertes de Bordeaux Métropole pour fournir des informations en temps réel sur les fermetures à venir.

## Installation

### Option 1 : Via HACS (recommandé)

1. Assurez-vous d'avoir [HACS](https://hacs.xyz/) installé
2. Allez dans HACS > Intégrations > Menu (⋮) > Dépôts personnalisés
3. Ajoutez le dépôt :
   - URL : `https://github.com/lightd31/Chaban`
   - Catégorie : Integration
4. Cliquez sur "Ajouter"
5. Recherchez "Chaban Bridge" dans les intégrations HACS
6. Cliquez sur "Télécharger"
7. Redémarrez Home Assistant

### Option 2 : Installation manuelle

1. Clonez ce dépôt dans le répertoire custom_components de votre installation Home Assistant :

    ```sh
    git clone https://github.com/lightd31/Chaban custom_components/chaban_bridge
    ```

2. Redémarrez Home Assistant.

## Configuration

1. Dans l'interface utilisateur de Home Assistant, allez dans `Configuration` > `Intégrations`.
2. Cliquez sur le bouton `+ Ajouter une intégration`.
3. Recherchez "Chaban Bridge" et suivez les instructions à l'écran pour configurer l'intégration.

## Utilisation

Une fois configuré, le composant "Chaban Bridge" ajoutera un capteur qui fournira les informations suivantes :

- **Nom** : Pont Chaban Delmas
- **ID unique** : chaban_bridge
- **État** : État actuel du pont
- **Attributs supplémentaires** :
  - `current_state` : État détaillé actuel du pont
  - `is_closed` : Indique si le pont est fermé
  - `last_update` : Dernière mise à jour des données
  - `closures` : Liste des 5 prochaines fermetures avec :
    - `reason` : Raison de la fermeture
    - `date` : Date de la fermeture
    - `start_date` : Date et heure de début de fermeture
    - `end_date` : Date et heure de fin de fermeture
    - `closure_type` : Type de fermeture

## Carte Lovelace Personnalisée

Une carte Lovelace dédiée a été développée pour afficher les informations de manière plus visuelle. Vous pouvez l'installer depuis :
https://github.com/LightD31/lovelace-chaban-bridge

Cette carte permet d'afficher :
- L'état actuel du pont
- Les prochaines fermetures prévues
- Une visualisation temporelle des fermetures

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](https://github.com/lightd31/Chaban/blob/main/LICENSE) pour plus de détails.