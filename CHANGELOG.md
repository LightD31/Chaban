# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-07-20

### Added
- Interface de configuration avec validation des paramètres
- Support multilingue (français/anglais)
- Tests unitaires complets
- Workflow GitHub Actions pour les tests automatiques
- Documentation améliorée avec exemples d'automatisations
- Informations détaillées sur l'appareil
- Icônes dynamiques selon l'état du pont
- Gestion d'erreur robuste avec retry automatique
- Validation HACS

### Changed
- Migration vers `CoordinatorEntity` pour de meilleures performances
- Amélioration de la gestion des erreurs réseau
- Optimisation des appels API
- Code restructuré selon les meilleures pratiques Home Assistant 2024
- Manifest mis à jour avec les dépendances correctes

### Fixed
- Imports dupliqués dans `__init__.py`
- Méthode de déchargement d'entrée obsolète
- Gestion des timeouts API
- Configuration unique par instance

### Security
- Validation des intervalles de mise à jour
- Gestion sécurisée des erreurs API

## [0.1.0] - 2024-XX-XX

### Added
- Version initiale du composant
- Capteur basique pour l'état du pont
- Récupération des fermetures prévues
- Configuration via config flow
