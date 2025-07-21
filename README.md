# Pont Chaban Delmas pour Home Assistant

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/LightD31/chaban-ha?style=for-the-badge)](https://github.com/LightD31/Chaban/releases)
[![GitHub](https://img.shields.io/github/license/LightD31/chaban-ha?style=for-the-badge)](https://github.com/LightD31/Chaban/blob/main/LICENSE)

Une intégration Home Assistant pour surveiller les fermetures et réouvertures du pont Chaban-Delmas à Bordeaux en temps réel.

## Qu'est-ce que le pont Chaban-Delmas ?

Le pont Chaban-Delmas est un pont vertical levant situé à Bordeaux, France. Il s'élève périodiquement pour permettre le passage de navires sur la Garonne, causant des interruptions temporaires de la circulation automobile et du tramway.

### Fonctionnalités

- ✅ État en temps réel du pont (ouvert/fermé/maintenance)
- ✅ Prochaines fermetures programmées (jusqu'à 5)
- ✅ Informations détaillées sur chaque fermeture (raison, dates, type)
- ✅ Icônes dynamiques selon l'état du pont
- ✅ Interface de configuration intuitive
- ✅ Support multilingue (français/anglais)
- ✅ Mise à jour automatique configurable
- ✅ Compatible HACS

## Prérequis

- Home Assistant 2024.9.0 ou plus récent
- HACS (optionnel mais recommandé)
- Connexion Internet pour accéder à l'API

## Installation

### Via HACS (Recommandé)

1. Ouvrez HACS dans Home Assistant
2. Allez dans "Intégrations"
3. Cliquez sur les trois points en haut à droite
4. Sélectionnez "Dépôts personnalisés"
5. Ajoutez `https://github.com/LightD31/Chaban` comme intégration
6. Recherchez "Chaban Bridge" et installez-le
7. Redémarrez Home Assistant

### Installation Manuelle

1. Téléchargez les fichiers depuis GitHub
2. Copiez le dossier `custom_components/chaban_bridge` dans votre répertoire `config/custom_components/`
3. Redémarrez Home Assistant

## Configuration

### Via l'Interface Utilisateur

1. Allez dans **Configuration** > **Intégrations**
2. Cliquez sur **+ Ajouter une intégration**
3. Recherchez "Chaban Bridge"
4. Suivez l'assistant de configuration :
   - **Intervalle de mise à jour** : Fréquence de récupération des données (entre 5 minutes et 24 heures)

## Utilisation

Une fois configuré, le capteur Chaban Bridge apparaîtra dans vos entités avec :

- **État** : État actuel du pont (ouvert/fermé/maintenance)
- **Attributs** :
  - `current_state` : État détaillé actuel du pont
  - `is_closed` : Indique si le pont est fermé (booléen)
  - `last_update` : Dernière mise à jour des données
  - `closures` : Liste des 5 prochaines fermetures avec :
    - `reason` : Raison de la fermeture
    - `date` : Date de la fermeture
    - `start_date` : Date et heure de début de fermeture
    - `end_date` : Date et heure de fin de fermeture
    - `closure_type` : Type de fermeture (planifiée/urgence)

### Carte Lovelace

```yaml
type: entities
entities:
  - sensor.pont_chaban_delmas
title: Pont Chaban-Delmas
```

### Exemple d'automatisation

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
```

## Carte Lovelace Personnalisée

Une carte Lovelace dédiée est disponible pour une visualisation améliorée :

**[Lovelace Chaban Bridge Card](https://github.com/LightD31/lovelace-chaban-bridge)**

Cette carte affiche l'état actuel du pont, les prochaines fermetures prévues et une visualisation temporelle des fermetures.

## Support

- 🐛 **Issues** : [GitHub Issues](https://github.com/LightD31/Chaban/issues)
- 💬 **Discussions** : [GitHub Discussions](https://github.com/LightD31/Chaban/discussions)

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou soumettre une pull request pour discuter d'améliorations.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Remerciements

- Données fournies par Bordeaux Métropole
- Inspiré par la communauté Home Assistant

---

⭐ Si cette intégration vous est utile, n'hésitez pas à donner une étoile au projet !
