param(
  [string]$AppName = "gestion-finanzas-personales",
  [string]$Region = "us",
  [string]$EmailUser = "",
  [string]$EmailPass = "",
  [string]$CloudinaryUrl = "",
  [switch]$Deploy
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-Step($msg) { Write-Host "`n==> $msg" -ForegroundColor Cyan }
function Write-Info($msg) { Write-Host "    $msg" -ForegroundColor Gray }
function Exec($cmd, [switch]$IgnoreError) {
  Write-Info $cmd
  try {
    & powershell -NoProfile -Command $cmd
  } catch {
    if (-not $IgnoreError) { throw }
  }
}

Write-Step "Checking Heroku CLI"
try { heroku --version | Out-Null } catch { throw "Heroku CLI not found. Install from https://devcenter.heroku.com/articles/heroku-cli" }

Write-Step "App existence: $AppName"
# Robust existence check using Start-Process (avoids PowerShell NativeCommandError)
$proc = Start-Process -FilePath "cmd.exe" -ArgumentList "/c","heroku apps:info -a $AppName 1>nul 2>nul" -NoNewWindow -PassThru -Wait
$exists = ($proc.ExitCode -eq 0)
if (-not $exists) {
  Exec "heroku create $AppName --region $Region"
  $proc2 = Start-Process -FilePath "cmd.exe" -ArgumentList "/c","heroku apps:info -a $AppName 1>nul 2>nul" -NoNewWindow -PassThru -Wait
  if ($proc2.ExitCode -ne 0) { throw "No se pudo crear/ubicar la app '$AppName'. Verifica nombre y sesión (heroku login)." }
} else {
  Write-Info "App already exists"
}

Write-Step "Set Python buildpack"
Exec "heroku buildpacks:set heroku/python -a $AppName"

Write-Step "Ensure Postgres addon"
# Try common free/small plans; ignore errors
Exec "heroku addons:create heroku-postgresql:mini -a $AppName" -IgnoreError
Exec "heroku addons:create heroku-postgresql:essential-0 -a $AppName" -IgnoreError
Exec "heroku addons:create heroku-postgresql:hobby-basic -a $AppName" -IgnoreError

Write-Step "Config vars"
# Generate a random secret (safe chars) if not set
$existingSecret = (& heroku config:get DJANGO_SECRET_KEY -a $AppName)
if (-not $existingSecret) {
  $lower = 97..122 | ForEach-Object { [char]$_ }
  $upper = 65..90  | ForEach-Object { [char]$_ }
  $digits = 48..57 | ForEach-Object { [char]$_ }
  $chars = @($lower + $upper + $digits)
  $rnd = New-Object System.Random
  $secret = -join (1..64 | ForEach-Object { $chars[$rnd.Next(0, $chars.Count)] })
  Exec "heroku config:set DJANGO_SECRET_KEY=$secret -a $AppName"
} else {
  Write-Info "DJANGO_SECRET_KEY already set"
}

Exec "heroku config:set DJANGO_DEBUG=False -a $AppName"
if ($EmailUser) { Exec "heroku config:set EMAIL_USER=`"$EmailUser`" -a $AppName" }
if ($EmailPass) { Exec "heroku config:set EMAIL_PASS=`"$EmailPass`" -a $AppName" }
if ($CloudinaryUrl) { Exec "heroku config:set CLOUDINARY_URL=`"$CloudinaryUrl`" -a $AppName" }
Exec "heroku config:unset DISABLE_COLLECTSTATIC -a $AppName" -IgnoreError

Write-Step "Git remote"
if (Test-Path -LiteralPath ".git") {
  Exec "heroku git:remote -a $AppName -r heroku"
} else {
  Write-Info "No es un repositorio Git. Inicializa con:"
  Write-Info "  git init; git add -A; git commit -m 'deploy'"
  Write-Info "  git branch -M main"
  Write-Info "Luego ejecuta: heroku git:remote -a $AppName -r heroku"
}

Write-Step "Ready to deploy"
Write-Info "This repo includes root Procfile and requirements.txt"
Write-Info "Deploy with: git push heroku main"

if ($Deploy) {
  Write-Step "Deploying: git push heroku main"
  Exec "git push heroku main"
}

Write-Step "Post-deploy commands"
Write-Info "Create superuser (one-time): heroku run python web/manage.py createsuperuser -a $AppName"
Write-Info "Open app: heroku open -a $AppName"
Write-Info "Logs: heroku logs -t -a $AppName"
