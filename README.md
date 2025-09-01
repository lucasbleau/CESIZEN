# CESIZEN – Application de Respiration Guidée

CESIZEN est une application web qui propose des exercices de respiration, le suivi de l’historique et une interface d’administration.

## Dépôt GitHub
<https://github.com/lucasbleau/CESIZEN.git>

## Installation locale

### 1. Prérequis
- **Python 3.10+**
- **pip**  
- **Git**
- (Recommandé) environnement virtuel **venv**

### 2. Stack Docker (Backend Node + Postgres + Nginx)
```
docker compose up -d
```
Services:
- db : PostgreSQL (base active `cesizen_import`)
- app : API Node (port host 8000)
- nginx : reverse proxy (80 / 8443)

### 3. Base de données
Import initial MySQL migré dans le schéma `cesizen_db` de la base `cesizen_import`.
Nouvelles tables/migrations dans le schéma `public`.
Search path: `public, cesizen_db`.

### 4. Migrations
```
docker compose exec app npm run migrate
```
Fichiers dans `migrations/` :
- 001_init.sql (tables users, breathing_exercises, user_sessions)
- 002_add_unique_breathing_title.sql (contrainte UNIQUE)

Historique enregistré dans `schema_migrations`.

### 5. Seed
```
docker compose exec app npm run seed
```
Insère (idempotent) les exercices de respiration de base.

### 6. Backup manuel
```
$now=$(Get-Date -Format "yyyyMMdd_HHmmss")
$cid=(docker compose ps -q db).Trim()
mkdir backups -ErrorAction SilentlyContinue | Out-Null
docker exec -i $cid pg_dump -U cesizen -d cesizen_import > ".\backups\cesizen_import_$now.sql"
```

### 7. Restauration (exemple)
```
docker compose exec -T db psql -U cesizen -d cesizen_import < backups\FICHIER.sql
```

### 8. Rebuild complet (reset data)
```
docker compose down
docker volume rm cesizen_pgdata
docker compose up -d
docker compose exec app npm run migrate
docker compose exec app npm run seed
```

### 9. Commandes utiles
```
docker compose exec db psql -U cesizen -d cesizen_import -c "\dt"
docker compose exec db psql -U cesizen -d cesizen_import -c "SELECT count(*) FROM breathing_exercises;"
```
