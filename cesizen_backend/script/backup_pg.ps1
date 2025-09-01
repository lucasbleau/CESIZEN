# Usage: .\scripts\backup_pg.ps1
# Creates backups\cesizen_db_YYYYMMDD_HHMMSS.sql

$now = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = Join-Path $PSScriptRoot "..\backups"
if (-not (Test-Path $backupDir)) { New-Item -ItemType Directory -Path $backupDir | Out-Null }

# get container id for db service
$cid = (docker compose ps -q db).Trim()
if (-not $cid) { Write-Error "DB container not found. Ensure docker compose up -d" ; exit 1 }

$envFile = Join-Path (Split-Path $PSScriptRoot -Parent) ".env"
# try to read credentials from .env (fallbacks)
$envContent = Get-Content $envFile -ErrorAction SilentlyContinue
$dbName = ($envContent | Select-String "^DB_NAME=" | ForEach-Object { $_.ToString().Split('=')[1] }) -ne $null ? ($envContent | Select-String "^DB_NAME=" | ForEach-Object { $_.ToString().Split('=')[1] }) : "cesizen_db"
$dbUser = ($envContent | Select-String "^DB_USER=" | ForEach-Object { $_.ToString().Split('=')[1] }) -ne $null ? ($envContent | Select-String "^DB_USER=" | ForEach-Object { $_.ToString().Split('=')[1] }) : "cesizen"

$dest = Join-Path $backupDir "cesizen_db_$now.sql"

Write-Output "Creating backup $dest from container $cid ..."
docker exec -i $cid pg_dump -U $dbUser -d $dbName > $dest

if ($LASTEXITCODE -eq 0) { Write-Output "Backup created: $dest" } else { Write-Error "Backup failed" }