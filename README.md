# cdm-insta

Publication automatique du compte Instagram @conciergerie_clesdesmerveilles (CDM Conciergerie, Pontorson).

- `calendrier/calendrier.json` : la file des posts (date, type, images, légende, premier commentaire, texte alternatif). Un post chaque mardi et vendredi, plus les posts bonus des fêtes.
- `calendrier/AAAA-MM/` : les images publiées, servies par raw.githubusercontent.com.
- `n8n/publication-cdm.json` : workflow de publication : chaque jour à 17h30, il publie le post daté du jour s'il existe.
- `n8n/renouvellement-token-cdm.json` : renouvellement du jeton Instagram, le 1er du mois.
- `construire.py` : reconstruit le calendrier à partir du stock de posts.

Pour annuler un post : supprimer son entrée dans `calendrier.json` avant 17h30 le jour prévu.
