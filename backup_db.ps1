param(
 [string]$ContainerName = "cesizen-db-1",
 [string]$Db= "cesizen_import"
)
$now = Get-Date -Format yyyyMMdd_HHmmss
$dest = Join-Path $PSScriptRoot "backups"
New-Item -ItemType Directory -Force -Path $dest | Out-Null
docker exec $ContainerName pg_dump -U cesizen -d $Db > (Join-Path $dest "dump_$($Db)_$now.sql")
