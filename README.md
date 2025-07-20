# Pont Chaban Delmas pour Home Assistant

[![License](https://img.shields.io/github/license/lightd31/Chaban.svg)](https://github.com/lightd31/Chaban/blob/main/LICENSE)
[![Test](https://github.com/lightd31/Chaban/workflows/Test/badge.svg)](https://github.com/lightd31/Chaban/actions)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![Version](https://img.shields.io/github/v/release/lightd31/Chaban.svg)](https://github.com/lightd31/Chaban/releases)

## Description

Le composant Home Assistant "Chaban Bridge" permet de surveiller les fermetures et réouvertures du pont Chaban-Delmas à Bordeaux. Il utilise les données ouvertes de Bordeaux Métropole pour fournir des informations en temps réel sur les fermetures à venir.

### Fonctionnalités

- ✅ État en temps réel du pont (ouvert/fermé/maintenance)
- ✅ Prochaines fermetures programmées (jusqu'à 5)
- ✅ Informations détaillées sur chaque fermeture (raison, dates, type)
- ✅ Icônes dynamiques selon l'état du pont
- ✅ Interface de configuration intuitive
- ✅ Support multilingue (français/anglais)
- ✅ Mise à jour automatique configurable

## Prérequis

- Home Assistant 2024.9.0 ou plus récent
- HACS (optionnel mais recommandé)
- Connexion Internet pour accéder à l'API

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

    ```bash
    git clone https://github.com/lightd31/Chaban custom_components/chaban_bridge
    ```

2. Redémarrez Home Assistant.

## Configuration

1. Dans l'interface utilisateur de Home Assistant, allez dans `Configuration` > `Intégrations`.
2. Cliquez sur le bouton `+ Ajouter une intégration`
3. Recherchez "Chaban Bridge" et suivez les instructions à l'écran pour configurer l'intégration
4. Configurez l'intervalle de mise à jour (optionnel, par défaut : 1 heure)

### Options de configuration

- **Intervalle de mise à jour** : Fréquence de récupération des données (entre 5 minutes et 24 heures)

## Utilisation

Une fois configuré, le composant "Chaban Bridge" ajoutera un capteur qui fournira les informations suivantes :

### Entité principale

- **Nom** : Pont Chaban Delmas
- **ID unique** : chaban_bridge
- **État** : État actuel du pont (ouvert/fermé/maintenance)
- **Icône** : Dynamique selon l'état du pont

### Attributs détaillés

- `current_state` : État détaillé actuel du pont
- `is_closed` : Indique si le pont est fermé (booléen)
- `last_update` : Dernière mise à jour des données
- `closures` : Liste des 5 prochaines fermetures avec :
  - `reason` : Raison de la fermeture
  - `date` : Date de la fermeture
  - `start_date` : Date et heure de début de fermeture
  - `end_date` : Date et heure de fin de fermeture
  - `closure_type` : Type de fermeture (planifiée/urgence)

### Exemples d'automatisations

```yaml
# Notification de fermeture imminente
automation:
  - alias: "Alerte fermeture pont Chaban"
    trigger:
      - platform: state
        entity_id: sensor.pont_chaban_delmas
        to: "closed"
    action:
      - service: notify.mobile_app
        data:
          message: "Le pont Chaban-Delmas est maintenant fermé"
          
# Fermeture dans les 30 minutes
automation:
  - alias: "Alerte fermeture imminente"
    trigger:
      - platform: time_pattern
        minutes: "/5"
    condition:
      - condition: template
        value_template: >
          {% set closures = state_attr('sensor.pont_chaban_delmas', 'closures') %}
          {% if closures %}
            {% set next_closure = closures[0]['start_date'] %}
            {% set now = now() %}
            {% set closure_time = strptime(next_closure, '%Y-%m-%dT%H:%M:%S') %}
            {{ (closure_time - now).total_seconds() < 1800 }}
          {% else %}
            false
          {% endif %}
    action:
      - service: notify.mobile_app
        data:
          message: "Le pont Chaban-Delmas fermera dans moins de 30 minutes"
```

## Carte Lovelace Personnalisée

Une carte Lovelace dédiée a été développée pour afficher les informations de manière plus visuelle :

**[Lovelace Chaban Bridge Card](https://github.com/LightD31/lovelace-chaban-bridge)**

Cette carte permet d'afficher :

- L'état actuel du pont
- Les prochaines fermetures prévues  
- Une visualisation temporelle des fermetures

## Développement

### Tests

```bash
pip install -r requirements_test.txt
pytest tests/ -v
```

### Linting

```bash
pip install ruff
ruff check custom_components/
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

## Support

- [Issues GitHub](https://github.com/lightd31/Chaban/issues)
- [Discussions](https://github.com/lightd31/Chaban/discussions)

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](https://github.com/lightd31/Chaban/blob/main/LICENSE) pour plus de détails.