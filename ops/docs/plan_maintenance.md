# Plan de Maintenance – Projet CESIZen

## 1. Objectifs
Assurer la continuité du service, la correction rapide des anomalies, l’évolution maîtrisée et la traçabilité.

## 2. Types de Maintenance
| Type | Description |
|------|-------------|
| Corrective | Correction bugs / incidents |
| Évolutive | Nouvelles fonctionnalités / améliorations |
| Préventive | Mises à jour, refactorings |
| Adaptative | Changement d’environnement (DB, OS) |

## 3. Outil de Ticketing
- GitHub Issues.
- Labels: bug, feature, security, documentation, performance.
- Priorités: P1 (critique), P2 (majeur), P3 (mineur), P4 (amélioration).

## 4. SLA (Incidents)
| Priorité | Définition | Délai prise en compte | Délai correction cible |
|----------|------------|-----------------------|------------------------|
| P1 | Service indisponible / faille critique | ≤ 1h ouvrée | ≤ 3h ouvrées |
| P2 | Fonction clé dégradée | ≤ 2h ouvrées | ≤ 6h ouvrées |
| P3 | Bug impact limité | ≤ 1 jour | ≤ 5 jours |
| P4 | Amélioration | ≤ 2 jours | Planifié release |

## 5. Workflow Ticket
1. Création (template).
2. Qualification (priorité, type).
3. Attribution (responsable).
4. Implémentation.
5. Revue (PR + tests).
6. Merge + release note.
7. Clôture (validation).

## 6. Change Management
- PR obligatoire.
- Tests automatiques obligatoires.
- Convention commit (feat:, fix:, chore:, docs:, refactor:, security:).
- Release notes dérivées (script futur ou manuel).

## 7. Calendrier Release
| Fréquence | Contenu | Tag |
|-----------|---------|-----|
| Hebdo (si besoin) | Correctifs mineurs | PATCH |
| Mensuel | Évolutions mineures | MINOR |
| Trimestriel | Changement majeur planifié | MAJOR |

## 8. Indicateurs Suivi
| KPI | Objectif |
|-----|----------|
| Taux succès déploiements | ≥ 95% |
| Délai moyen résolution P1 | < 4h |
| % Tickets avec tests associés | 100% |
| Couverture tests | Maintien / amélioration |
| Incidents récurrents (même cause) | 0 après action corrective |

## 9. Backlog & Priorisation
- Revue mensuelle.
- Critères: valeur utilisateur, risque technique, dépendances.
- Architecture dette technique: suivi étiquette “tech-debt”.

## 10. Documentation
- Toute évolution impactant API → mise à jour doc + changelog.
- Procédures ajoutées dans /ops/docs.

## 11. Préventif
| Action | Fréquence |
|--------|-----------|
| Mise à jour dépendances | Mensuelle |
| Revue sécurité (librairies) | Mensuelle |
| Test restauration backup | Trimestrielle |
| Revue RGPD | Semestrielle |
| Audit configuration | Semestrielle |

## 12. Veille
Sources: Django releases, DRF, OWASP, Postgres, CVE feed. Consolidation mensuelle → ticket “veille”.

## 13. Fin de Vie / Dépréciation
- Fonction marquée “deprecated” -> tag dans release notes + plan retrait.
- Suppression > 2 cycles MINOR après annonce.

## 14. Post-mortem
Pour P1 / sécurité:
- Chronologie
- Impact
- Cause racine
- Actions immédiates
- Correctifs long terme
- Leçons / prévention

## 15. Améliorations Futures
- Automatisation génération changelog.
- Tableau bord métriques (Grafana).
- Support multi-fuseaux horaires (internationalisation future).
