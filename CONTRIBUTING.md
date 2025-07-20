# Guide de Contribution

Merci de votre intérêt pour contribuer au projet Chaban Bridge ! 🎉

## Comment contribuer

### Signaler un bug

1. Vérifiez que le bug n'a pas déjà été signalé dans les [Issues](https://github.com/lightd31/Chaban/issues)
2. Créez une nouvelle issue avec le template "Bug Report"
3. Incluez autant de détails que possible :
   - Version de Home Assistant
   - Version de l'intégration
   - Logs pertinents
   - Étapes pour reproduire le problème

### Proposer une amélioration

1. Ouvrez une [Discussion](https://github.com/lightd31/Chaban/discussions) pour discuter de votre idée
2. Si l'idée est validée, créez une issue avec le template "Feature Request"

### Contribuer au code

1. **Fork** le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Configurez votre environnement de développement :
   ```bash
   pip install -r requirements_test.txt
   ```
4. Apportez vos modifications
5. Ajoutez des tests pour vos modifications
6. Vérifiez que tous les tests passent :
   ```bash
   pytest tests/ -v
   ```
7. Vérifiez le linting :
   ```bash
   ruff check custom_components/
   ```
8. Commitez vos changements (`git commit -m 'Add some AmazingFeature'`)
9. Poussez vers la branche (`git push origin feature/AmazingFeature`)
10. Ouvrez une **Pull Request**

## Standards de développement

### Style de code
- Suivez les conventions PEP 8
- Utilisez `ruff` pour le linting
- Documentez vos fonctions avec des docstrings
- Utilisez des type hints

### Tests
- Écrivez des tests pour toute nouvelle fonctionnalité
- Maintenez une couverture de test élevée
- Testez les cas d'erreur

### Commits
- Utilisez des messages de commit clairs et descriptifs
- Préférez plusieurs petits commits à un gros commit
- Référencez les issues dans vos commits (#123)

## Structure du projet

```
custom_components/chaban_bridge/
├── __init__.py          # Point d'entrée de l'intégration
├── config_flow.py       # Configuration via l'interface
├── const.py            # Constantes
├── manifest.json       # Métadonnées de l'intégration
├── sensor.py           # Entité capteur
└── translations/       # Traductions
    ├── en.json
    └── fr.json

tests/                  # Tests unitaires
├── conftest.py
├── test_config_flow.py
└── test_sensor.py
```

## Questions ?

N'hésitez pas à :
- Ouvrir une [Discussion](https://github.com/lightd31/Chaban/discussions)
- Contacter les mainteneurs

Merci pour votre contribution ! 🙏
