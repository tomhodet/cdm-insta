# cdm-insta

Publication automatique du compte Instagram @conciergerie_clesdesmerveilles (CDM Conciergerie, Pontorson).

- `calendrier/calendrier.json` : la file des posts (date, type, images, légende, premier commentaire, texte alternatif). Un post par vendredi, à 12 h.
- `calendrier/AAAA-MM/` : les images publiées, servies par raw.githubusercontent.com.
- `n8n/publication-cdm.json` : workflow de publication (vendredi 12 h).
- `n8n/renouvellement-token-cdm.json` : renouvellement du jeton Instagram, le 1er du mois.
- `construire.py` : reconstruit le calendrier à partir du stock de posts.

Pour annuler un post : supprimer son entrée dans `calendrier.json` avant le vendredi midi.
