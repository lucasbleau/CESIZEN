# Registre RGPD – CESIZen

| Traitement | Finalité | Données | Base légale | Durée conservation | Mesures |
|------------|----------|---------|-------------|--------------------|---------|
| Gestion comptes | Authentifier utilisateurs | Email, username, hash MDP | Exécution contrat (service) | Compte + 24 mois inactivité | Hash, accès restreint |
| Historique exercices respiration | Suivi usage / progression utilisateur | Durées, exercice choisi | Intérêt légitime (amélioration) | 12 mois glissants (future purge) | Limitation accès |
| Logs techniques | Diagnostic incidents | Timestamp, chemin, code statut | Intérêt légitime | 30 jours | Rotation, anonymisation IP partielle (future) |
| Support / incidents | Traitement demandes | Email, contenu ticket | Exécution contrat | 24 mois | Accès contrôlé |
| Sauvegardes | Continuité service | Copie DB | Intérêt légitime | 30 jours cycle rétention | Stockage sécurisé |

Droits personnes:
- Accès / rectification / suppression sur demande (délai ≤ 30 jours).
- Portabilité: export JSON sur demande (future fonction).
- Limitation / opposition: possible suppression historique.

Sous-traitants: (Hébergeur) – vérifier localisation UE.  
Transferts hors UE: Aucun.  
Violation de données: notification CNIL si risque élevé, délai initial objectif < 72h.

