# Chaban Bridge

[![GitHub release](https://img.shields.io/github/release/lightd31/Chaban.svg)](https://github.com/lightd31/Chaban/releases)
[![License](https://img.shields.io/github/license/lightd31/Chaban.svg)](https://github.com/lightd31/Chaban/blob/main/LICENSE)

## Description

Le composant Home Assistant "Chaban Bridge" permet de surveiller les fermetures et réouvertures du pont Chaban-Delmas à Bordeaux. Il utilise les données ouvertes de Bordeaux Métropole pour fournir des informations en temps réel sur les fermetures à venir.

## Installation

1. Clonez ce dépôt dans le répertoire `custom_components` de votre installation Home Assistant :

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

- **Nom** : Chaban Bridge Next Closure
- **ID unique** : chaban_bridge_next_closure
- **État** : Date et heure de la prochaine fermeture à la circulation
- **Attributs supplémentaires** :
  - `bateau` : Nom du bateau
  - `date_passage` : Date de passage du bateau
  - `fermeture_a_la_circulation` : Date et heure de fermeture à la circulation
  - `re_ouverture_a_la_circulation` : Date et heure de réouverture à la circulation
  - `type_de_fermeture` : Type de fermeture
  - `fermeture_totale` : Indique si la fermeture est totale

## Licence

Ce projet est sous licence GNU General Public License v3.0. Voir le fichier [LICENSE](https://github.com/lightd31/Chaban/blob/main/LICENSE) pour plus de détails.