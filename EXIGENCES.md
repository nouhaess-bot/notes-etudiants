\# Exigences de sécurité de l'application des notes



| # | Exigence : « Le système doit… » | Vérification | Étape du SDLC | Test |

|---|---|---|---|---|

| 1 | utiliser des requêtes SQL paramétrées pour empêcher les injections SQL. | Tester une recherche avec une entrée malveillante. | Développement | S1 |

| 2 | identifier l'utilisateur avant d'autoriser la modification d'une note. | Une demande sans jeton doit retourner HTTP 401. | Conception / Tests | S2 |

| 3 | interdire aux étudiants de modifier les notes. | Un jeton étudiant doit retourner HTTP 403. | Conception / Tests | S3 |

| 4 | autoriser un enseignant à modifier uniquement les notes de son module. | Un enseignant d'un autre module doit recevoir HTTP 403. | Conception / Tests | S4 |

| 5 | accepter uniquement une note numérique comprise entre 0 et 20. | Une note invalide doit retourner HTTP 400. | Développement / Tests | S5 |

| 6 | ne pas exposer les détails techniques des erreurs internes. | La réponse d'erreur ne doit pas révéler les détails de la base de données. | Tests | S7 |

| 7 | permettre à un enseignant autorisé de modifier une note. | La modification doit retourner HTTP 200 et enregistrer la nouvelle note. | Tests | S6 |

