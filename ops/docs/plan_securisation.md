# Plan de Sécurisation – Projet CESIZen

## 1. Objectifs
Garantir confidentialité, intégrité, disponibilité et conformité RGPD des données.

## 2. Classification des Données
| Catégorie | Exemple | Sensibilité | Mesures |
|-----------|---------|------------|---------|
| Identification | email, username | Élevée | Hash, accès restreint |
| Authentification | hash mot de passe | Critique | PBKDF2 / salage |
| Historique exercices | durées respiration | Moyenne | Chiffrement transit |
| Métadonnées techniques | logs timestamp | Faible | Rotation / anonymisation partielle |
| Futur (émotions) | réponses track | Élevée | Minimisation + anonymisation analytique |

## 3. Principes
- Moindre privilège
- Défense en profondeur
- Journalisation systématique
- Séparation configuration / code

## 4. Mesures Techniques
| Domaine | Mesure | Statut |
|---------|--------|--------|
| Transport | HTTPS (TLS 1.2+) | À appliquer côté proxy |
| Hash MDP | PBKDF2 (Django) | En place |
| Chiffrement repos (DB) | Support disque chiffré (infrastructure) | À valider hébergeur |
| Cookies | httponly, samesite, secure en prod | Partiel (secure à activer) |
| Headers sécurité | HSTS, X-Content-Type-Options, Referrer-Policy | Proxy |
| Séparation secrets | Variables env / GitHub Secrets | En place |
| Durcissement image | USER non-root, dépendances minimales | Ajouté |
| Dépendances | Mises à jour / pip audit | À planifier |
| Logs | Aucune donnée sensible | À surveiller |
| Accès SSH | Clés + limitation IP | À configurer |
| Sauvegardes | Script + rétention + test restauration | Plan défini |

## 5. Menaces & Contrôles (Exemple)
| Menace | Vecteur | Contrôle Préventif | Détection | Réponse |
|--------|---------|--------------------|-----------|---------|
| SQL Injection | Paramètres | ORM Django | Logs erreurs | Patch |
| XSS | Entrées non échappées | Templates autoescape | CSP futur | Correction template |
| Brute force | Auth | Limitation (future) | Pics logs | Blocage IP |
| Exfiltration logs | Logs sensibles | Revue logs | Audit accès | Purge / rotation |
| Fuite secrets | Repo Git | GitLeaks / secrets scanning | Alerte GitHub | Rotation secrets |
| Compromission pipeline | Token actions | Permissions minimales | Revue workflows | Révocation PAT |
| DoS simple | Requêtes massives | Reverse proxy rate-limit (futur) | Pics latence | Tuning / blocage IP |

## 6. Matrice des Risques
Voir risk_matrix.md (fichier séparé).

## 7. Gestion des Vulnérabilités
- Revue dépendances mensuelle.
- Veille sécurité: Django, DRF, Postgres.
- Correctif critique: ≤ 24h.
- Standard: prochain cycle release.

## 8. Gestion des Secrets
- Jamais commit.
- Rotation annuelle ou incident.
- Accès restreint (principle of least privilege).

## 9. Journalisation
| Type | Contenu | Conservation | Outil |
|------|---------|-------------|-------|
| Accès | Méthode, chemin, code | 30 j | Stdout |
| Erreurs | Traceback filtrée | 30 j | Stdout |
| Sécurité | Auth ratée, upgrade admin | 90 j (futur) | Centralisation future |

## 10. Supervision & Alertes
- Health check /health.
- Erreurs 5xx > seuil → alerte (futur).
- Backups échec → alerte manuelle (log + email futur).

## 11. RGPD (Synthèse)
- Minimisation: seules données strictes (email, usage exercices).
- Droits: export/suppression sur ticket (délai ≤ 30 jours).
- Base légale: exécution du service + consentement (futur si notifications).
- Conservation: comptes inactifs > 24 mois → purge (future tâche).
- Aucune donnée hors UE.

## 12. Processus Incident Sécurité
Phases:
1. Détection (logs, alertes).
2. Triage (priorité).
3. Containment (isoler conteneur).
4. Éradication (patch / rotation secrets).
5. Restauration (redeploy propre).
6. Post-mortem (rapport + actions préventives).

Délais cibles:
- Critique (exfiltration confirmée): containment ≤ 1h, communication initiale ≤ 4h.
- Majeur: containment ≤ 4h.
- Mineur: correctif ≤ prochain patch cycle.

## 13. Conformité Continue
- Revue semestrielle du plan.
- Mise à jour après toute évolution majeure architecture.

## 14. Améliorations Futures
- WAF / Rate limiting.
- CSP stricte.
- Multi-factor administrateurs.
- OIDC / SSO (phase 2).

