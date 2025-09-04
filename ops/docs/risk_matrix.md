# Matrice des Risques – CESIZen

| ID | Risque / Vulnérabilité | Menace | Impact | Probabilité | Criticité | Prévention | Détection | Réponse / Mitigation Résiduelle |
|----|------------------------|--------|--------|-------------|-----------|------------|-----------|---------------------------------|
| R1 | Injection SQL | Attaquant manipule requêtes | Fuite / corruption données | Faible | Moyen | ORM Django, validation | Logs erreurs | Patch, audit |
| R2 | XSS | Script injecté dans UI | Vol session / phishing | Moyen | Moyen | Autoescape, validation | Signalements, CSP futur | Nettoyage, patch template |
| R3 | Brute force login | Tentatives massives | Compromission compte | Haut | Moyen | Limiteur futur, complexité MDP | Pics échecs login | Blocage IP, MFA futur |
| R4 | Fuite secrets dépôt | Commit accidentel | Accès non autorisé | Critique | Faible | GitIgnore, secrets scanning | Outil GitHub | Rotation secrets |
| R5 | Dépendance vulnérable | Lib compromise | Exécution code | Haut | Moyen | Mises à jour mensuelles | Alertes CVE | Upgrade urgent |
| R6 | Exposition DB | Mauvaise config réseau | Fuite massive | Critique | Faible | Réseau privé, firewall | Scans externes | Fermer accès, rotation creds |
| R7 | DoS basique | Requêtes volumétriques | Indispo service | Moyen | Moyen | Reverse proxy, rate-limit futur | Monitoring latence | Filtrer IP, scale |
| R8 | Perte données | Suppression / panne disque | Perte historique | Haut | Faible | Backups + tests restauration | Alertes backup | Restauration |
| R9 | Escalade privilèges | Mauvaise vérification rôle | Accès admin | Haut | Faible | Contrôles code revus | Logs anomalies | Patch + post-mortem |
| R10 | Failles CI/CD | Build altéré | Backdoor image | Critique | Faible | Permissions min, review workflow | Audit actions | Révoquer jetons, rebuild |
| R11 | Logs sensibles | PII stockée | Non conformité RGPD | Moyen | Faible | Filtrage logs | Revue | Purge & correction |
| R12 | Incident sécurité non détecté | Manque monitoring | Aggravation impact | Haut | Moyen | Process health + journaux | Revue quotidienne | Process incident |
| R13 | Mauvaise purge comptes | Conservation indue | Non conformité | Moyen | Faible | Politique purge | Revue semestrielle | Script purge correctif |
| R14 | Ransomware DB | Chiffrement illégitime données | Indisponibilité prolongée | Critique | Faible | Backups off-site, mises à jour | Alertes comportement | Restaurer + analyse |
| R15 | Déni qualité tests | Release cassée | Régressions | Moyen | Moyen | CI systématique | Échecs pipeline | Hotfix + ajout tests |
| R16 | Mauvaise gestion sessions cookies non secure | Session détournée | Compromission compte | Haut | Faible | SECURE flags prod | Audit config | Activer flags, invalider sessions |
| R17 | Erreur migration destructrice | Script erroné | Perte données | Haut | Faible | Backup avant migration | Échec application | Restauration + correction |
| R18 | Accès non journalisé admin | Intrusion silencieuse | Altérations invisibles | Haut | Faible | Journalisation actions clés (future) | Revue comptes | Activer logs, contrôle comptes |

Criticité déterminée (ex.: Impact * Probabilité qualitative convertie). Mise à jour semestrielle.