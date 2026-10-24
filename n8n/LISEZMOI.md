# CDM · Publication Instagram (n8n)

Fichier à importer : `publication-cdm.json`.

## Ce que fait le workflow

Chaque jour à 17h30 (heure de Paris), le workflow lit le calendrier
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

Route retenue : connexion Instagram (comme le compte DelorIA). Le jeton dure 60 jours ;
`renouvellement-token-cdm.json` le renouvelle le 1er de chaque mois à 4h15.

- **API_BASE** : `https://graph.instagram.com`.
- **IG_ID** : `17841476967149235` (compte Instagram professionnel de CDM).
- **ALT_TEXT** : `true`. Le texte alternatif (coupé à 1000 caractères) est envoyé sur
  l'image simple et sur chaque élément du carrousel.
- **LOCATION_ID** : vide par défaut. S'il est renseigné, il est envoyé en `location_id`
  sur le conteneur image simple ou CAROUSEL (jamais sur les éléments).

## À faire après l'import

**Credentials** (déjà créées le 24/10/2026) : `Instagram CDM` (Header Auth,
`Authorization: Bearer <jeton>`) et `Instagram CDM refresh` (Query Auth, `access_token`).
Si un nœud HTTP les affiche en rouge après l'import, les resélectionner.
Dans `renouvellement-token-cdm.json`, choisir la connexion à l'API n8n dans les deux
nœuds « Mettre a jour credential ».

## Tester sans publier

1. Dans `Post du jour`, mettre une date du calendrier : `const DATE_FORCEE = '2026-11-03';`
2. Désactiver le nœud `Publier` (clic droit, Deactivate).
3. Lancer avec `Lancement manuel` et vérifier les sorties : post trouvé, containers
   créés, statut `FINISHED`. Le container non publié expire seul au bout de 24 h.
4. Remettre `DATE_FORCEE = ''` et réactiver `Publier` avant d'activer le workflow.

## Schéma

```
Chaque jour 17h30 ─┐
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
