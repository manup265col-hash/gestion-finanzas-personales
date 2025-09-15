# ================================
# Script de despliegue automático
# Django + GitHub + Heroku
# ================================

param (
    [string]$mensaje = "Actualización del proyecto"
)

Write-Host "🔧 Ejecutando migraciones locales..."
python manage.py makemigrations
python manage.py migrate

Write-Host "✅ Migraciones locales completadas."

Write-Host "📌 Guardando cambios en Git..."
git add .
git commit -m "$mensaje"
git push origin main

Write-Host "☁️ Subiendo cambios a Heroku..."
git push heroku main

Write-Host "🔄 Aplicando migraciones en Heroku..."
heroku run python manage.py migrate

Write-Host "🚀 Despliegue completado con éxito."
