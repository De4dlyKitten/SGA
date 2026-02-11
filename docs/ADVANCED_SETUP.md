# SGA-Lite - Guía Avanzada de Configuración

## 📚 Contenido

1. [Configuración de PostgreSQL](#configuración-de-postgresql)
2. [Despliegue con Gunicorn + Nginx](#despliegue-con-gunicorn--nginx)
3. [Configuración de Dominio y SSL](#configuración-de-dominio-y-ssl)
4. [Optimizaciones de Producción](#optimizaciones-de-producción)
5. [Respaldos y Mantenimiento](#respaldos-y-mantenimiento)

---

## Configuración de PostgreSQL

### Instalación en Ubuntu/Debian

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### Crear Base de Datos y Usuario

```bash
# Entrar a PostgreSQL
sudo -u postgres psql

# Crear base de datos
CREATE DATABASE sga_lite_db;

# Crear usuario
CREATE USER sga_user WITH PASSWORD 'tu_password_seguro';

# Dar permisos
GRANT ALL PRIVILEGES ON DATABASE sga_lite_db TO sga_user;

# Salir
\q
```

### Configurar .env para PostgreSQL

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=sga_lite_db
DB_USER=sga_user
DB_PASSWORD=tu_password_seguro
DB_HOST=localhost
DB_PORT=5432
```

### Permitir Conexiones Remotas (Opcional)

Editar `/etc/postgresql/14/main/postgresql.conf`:
```
listen_addresses = '*'
```

Editar `/etc/postgresql/14/main/pg_hba.conf`:
```
host    all             all             0.0.0.0/0               md5
```

Reiniciar:
```bash
sudo systemctl restart postgresql
```

---

## Despliegue con Gunicorn + Nginx

### 1. Instalar Gunicorn

```bash
source venv/bin/activate
pip install gunicorn
```

### 2. Crear archivo de servicio systemd

Crear `/etc/systemd/system/sga-lite.service`:

```ini
[Unit]
Description=SGA-Lite Gunicorn daemon
After=network.target

[Service]
User=tu_usuario
Group=www-data
WorkingDirectory=/ruta/a/sga-lite
Environment="PATH=/ruta/a/sga-lite/venv/bin"
ExecStart=/ruta/a/sga-lite/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/ruta/a/sga-lite/sga-lite.sock \
          sga_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 3. Iniciar servicio

```bash
sudo systemctl start sga-lite
sudo systemctl enable sga-lite
sudo systemctl status sga-lite
```

### 4. Configurar Nginx

Crear `/etc/nginx/sites-available/sga-lite`:

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /ruta/a/sga-lite/staticfiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/ruta/a/sga-lite/sga-lite.sock;
    }
}
```

Activar configuración:
```bash
sudo ln -s /etc/nginx/sites-available/sga-lite /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Configuración de Dominio y SSL

### 1. Apuntar Dominio al Servidor

En tu registrador de dominios, crear:
- **A Record**: `@` → IP de tu servidor
- **A Record**: `www` → IP de tu servidor

### 2. Instalar Certbot (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
```

### 3. Obtener Certificado SSL

```bash
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

Certbot configurará automáticamente Nginx para HTTPS.

### 4. Renovación Automática

```bash
# Verificar renovación
sudo certbot renew --dry-run

# La renovación automática ya está configurada
```

---

## Optimizaciones de Producción

### 1. Configuración de Django

En `settings.py` o `.env`:

```python
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### 2. Configurar STATIC_ROOT

```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

Ejecutar:
```bash
python manage.py collectstatic --noinput
```

### 3. Optimizar Base de Datos

```sql
-- Crear índices adicionales si es necesario
CREATE INDEX idx_attendance_date ON attendance_attendancelog(date);
CREATE INDEX idx_attendance_user_date ON attendance_attendancelog(user_id, date);

-- Analizar tablas
ANALYZE;
```

### 4. Configurar Cache (Redis - Opcional)

Instalar Redis:
```bash
sudo apt install redis-server
pip install django-redis
```

En `settings.py`:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

---

## Respaldos y Mantenimiento

### 1. Backup de Base de Datos

**Crear script de backup** (`/home/tu_usuario/backup_sga.sh`):

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/tu_usuario/backups"
DB_NAME="sga_lite_db"
DB_USER="sga_user"

mkdir -p $BACKUP_DIR

# Backup PostgreSQL
PGPASSWORD="tu_password" pg_dump -U $DB_USER -h localhost $DB_NAME > $BACKUP_DIR/sga_backup_$DATE.sql

# Comprimir
gzip $BACKUP_DIR/sga_backup_$DATE.sql

# Eliminar backups más antiguos de 30 días
find $BACKUP_DIR -name "sga_backup_*.sql.gz" -mtime +30 -delete

echo "Backup completado: sga_backup_$DATE.sql.gz"
```

**Automatizar con cron**:
```bash
crontab -e

# Agregar línea (backup diario a las 2 AM)
0 2 * * * /home/tu_usuario/backup_sga.sh
```

### 2. Restaurar Backup

```bash
gunzip sga_backup_20250211.sql.gz
PGPASSWORD="tu_password" psql -U sga_user -h localhost sga_lite_db < sga_backup_20250211.sql
```

### 3. Monitoreo de Logs

```bash
# Ver logs de Gunicorn
sudo journalctl -u sga-lite -f

# Ver logs de Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Ver logs de Django (si configurado)
tail -f /ruta/a/sga-lite/logs/django.log
```

### 4. Actualizar el Sistema

```bash
cd /ruta/a/sga-lite
git pull  # Si usas Git
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart sga-lite
```

---

## Seguridad Adicional

### 1. Firewall (UFW)

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. Fail2Ban (Protección contra fuerza bruta)

```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 3. Actualizar SECRET_KEY

```python
# Generar nueva clave
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Actualizar en `.env`

---

## Solución de Problemas Comunes

### Error 502 Bad Gateway

```bash
# Verificar que Gunicorn esté corriendo
sudo systemctl status sga-lite

# Verificar permisos del socket
ls -la /ruta/a/sga-lite/sga-lite.sock
```

### Error de Conexión a Base de Datos

```bash
# Verificar que PostgreSQL esté corriendo
sudo systemctl status postgresql

# Probar conexión manual
psql -U sga_user -h localhost -d sga_lite_db
```

### Archivos Estáticos No Se Cargan

```bash
# Re-colectar archivos estáticos
python manage.py collectstatic --noinput

# Verificar permisos
sudo chown -R www-data:www-data /ruta/a/sga-lite/staticfiles
```

---

## Comandos Útiles de Mantenimiento

```bash
# Ver usuarios conectados
python manage.py shell
>>> from django.contrib.sessions.models import Session
>>> Session.objects.all().count()

# Limpiar sesiones expiradas
python manage.py clearsessions

# Ver estadísticas de base de datos
python manage.py dbshell
>>> SELECT COUNT(*) FROM attendance_attendancelog;

# Crear dump de datos (fixtures)
python manage.py dumpdata attendance > attendance_data.json
```

---

## Contacto y Soporte

Para problemas específicos de despliegue o configuración avanzada, consultar:
- Documentación oficial de Django: https://docs.djangoproject.com
- Guías de Nginx: https://nginx.org/en/docs/
- PostgreSQL Documentation: https://www.postgresql.org/docs/
