# Tracker d'esprits Fortnite (overlay)

Petit outil Windows en Python pour suivre les esprits recuperes.

Le mode actuel suit les variantes (Normal, Or, Gelifie, etc.) pour un total de 109 entrees.

## Fonctionnalites

- Fenetre toujours au-dessus des autres applications (pratique pendant le jeu)
- Cases a cocher pour marquer les esprits recuperes
- Barre de progression automatique
- Filtre de recherche
- Filtre "manquants seulement"
- Miniatures des esprits dans la liste (via `esprits_images.json`)
- Sauvegarde locale automatique dans `etat_esprits.json`

## Fichiers

- `overlay_esprits.py` : application principale
- `esprits.txt` : liste des esprits (1 nom par ligne)
- `esprits_images.json` : noms + images des esprits
- `etat_esprits.json` : etat sauvegarde (genere automatiquement)
- `lancer_overlay.bat` : lanceur rapide

## Utilisation

1. Edite `esprits.txt` si besoin (ou garde la liste deja pre-remplie).
2. Double-clique sur `lancer_overlay.bat`.
3. Place la fenetre ou tu veux sur ton ecran.
4. Coche au fur et a mesure ce que tu as recupere.
5. Si tu modifies `esprits.txt` ou `esprits_images.json`, clique "Recharger la liste".

## Prerequis

- Windows
- Python 3.10+
- Pillow (pour afficher les miniatures): `pip install pillow`

## Astuce overlay

La fenetre est semi-transparente et "toujours au-dessus". Si tu veux la rendre plus ou moins visible, change cette ligne dans `overlay_esprits.py` :

```python
self.root.attributes("-alpha", 0.92)
```

Exemple : `0.75` = plus transparent, `1.0` = opaque.
