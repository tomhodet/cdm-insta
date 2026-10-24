# CDM · Publication Instagram (n8n)

Fichier à importer : `publication-cdm.json`.

## Ce que fait le workflow

Chaque vendredi à 12h00 (heure de Paris), le workflow lit le calendrier
`calendrier/calendrier.json` du dépôt `tomhodet/cdm-insta`, cherche le post du jour
et le publie sur le compte Instagram de CDM Conciergerie (image simple ou carrousel).
Il vérifie d'abord que la légende ne figure pas déjà parmi les 10 derniers posts
(protection contre la double publication). Après publication, il attend 10 secondes
puis poste le premier commentaire (hashtags) si le calendrier en prévoit un.

Format d'une entrée du calendrier :

```json
{"date":"2026-11-06","type":"carrousel","image_url":"...","images":["...","..."],
 "legende":"...","premier_commentaire":"#...","alt_text":"..."}
```

## Réglages (nœud `Config`)

Route retenue : Facebook Login, avec un token de Page longue durée. Il n'y a pas de
workflow de renouvellement du token pour ce compte.

- **API_BASE** : `https://graph.facebook.com` par défaut. Mettre
  `https://graph.instagram.com` si on repasse par la connexion Instagram.
- **IG_ID** : `17841476967149235` (compte Instagram professionnel de CDM).
- **ALT_TEXT** : `true`. Le texte alternatif (coupé à 1000 caractères) est envoyé sur
  l'image simple et sur chaque élément du carrousel.
- **LOCATION_ID** : vide par défaut. S'il est renseigné, il est envoyé en `location_id`
  sur le conteneur image simple ou CAROUSEL (jamais sur les éléments).

## À faire après l'import

**Credential** : créer une credential « Header Auth » nommée `Instagram CDM`
(Name : `Authorization`, Value : `Bearer <token de Page CDM>`), puis la sélectionner
dans chaque nœud HTTP qui l'affiche en rouge (Derniers posts, Creer container,
Statut container, Publier, Creer element, Creer carrousel, Premier commentaire).

## Tester sans publier

1. Dans `Post du jour`, mettre une date du calendrier : `const DATE_FORCEE = '2026-11-06';`
2. Désactiver le nœud `Publier` (clic droit, Deactivate).
3. Lancer avec `Lancement manuel` et vérifier les sorties : post trouvé, containers
   créés, statut `FINISHED`. Le container non publié expire seul au bout de 24 h.
4. Remettre `DATE_FORCEE = ''` et réactiver `Publier` avant d'activer le workflow.

## Schéma

```
Chaque vendredi 12h ─┐
Lancement manuel ────┴─> Config -> Lire calendrier -> Post du jour -> Post prevu ?
  -> Derniers posts -> Deja publie ? -> A publier ? -> Carrousel ?
       non : Creer container ──────────────────────────────────────────┐
       oui : Eclater images -> Creer element -> Assembler carrousel     │
             -> Attendre 30s -> Creer carrousel ───────────────────────┤
  Attendre 60s <───────────────────────────────────────────────────────┘
  -> Statut container -> Container pret ?
       non : Erreur container
       oui : Publier -> Commentaire ? -> Attendre 10s -> Premier commentaire
```
