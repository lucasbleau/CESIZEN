# Déploiement & Exploitation – CESIZen

## 1. Pré-requis
- Docker / Docker Compose
- Accès au registre GHCR (image construite via tags)
- Fichier .env.prod configuré

## 2. Variables (exemple .env.prod)
DJANGO_SECRET_KEY=changer_cet_secret
DATABASE_URL=postgres://cesizen:motdepasse@db:5432/cesizen
ALLOWED_HOSTS=cesizen.fr,www.cesizen.fr
DEBUG=0
APP_VERSION=v1.2.0
LOG_LEVEL=INFO
SECURE_SSL_REDIRECT=1
SESSION_COOKIE_SECURE=1
CSRF_COOKIE_SECURE=1

## 3. Démarrage
```
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
```

## 4. Vérification
```
curl -fsS http://localhost:8000/health/
```

## 5. Mise à jour / Release
1. Tag git vX.Y.Z
2. Attendre build GHCR
3. Mettre à jour .env.prod (APP_VERSION)
4. docker compose pull && docker compose up -d

## 6. Rollback
```
docker pull ghcr.io/<repo>:vX.Y.(Z-1)
docker compose up -d
```

## 7. Sauvegarde DB
Script: ops/backup/backup.sh (dry-run possible)
Ex:
```
bash ops/backup/backup.sh --pg-url postgres://cesizen:pwd@localhost:5432/cesizen --dry-run
```

## 8. Santé & Logs
Health: /health/  
Logs:
```
docker compose logs -f web
```

## 9. Sécurité clés
- Rotation annuelle + après incident.
- Jamais de secret en clair dans commits.

## 10. Maintenance
Voir plan_maintenance.md (SLA, workflows, KPI).

Fin.

