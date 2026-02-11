# SGA-Lite - Sistema de Gestión de Asistencia

Sistema web ligero para el control de asistencia de empleados basado en grupos de días permitidos.

## 📋 Características

- ✅ **Autenticación**: Login seguro con roles (Admin/Empleado)
- 👥 **Gestión de Usuarios**: Crear y administrar empleados
- 📅 **Grupos de Asistencia**: Definir qué días puede fichar cada empleado
- ⏰ **Fichaje**: Interfaz minimalista para marcar entrada/salida
- 📊 **Reportes**: Dashboard en vivo y exportación a Excel
- 🌐 **Timezone**: Configurado para America/Santo_Domingo
- 🎨 **UI Moderna**: TailwindCSS + Alpine.js

## 🛠️ Stack Tecnológico

- **Backend**: Django 5.0.1
- **Frontend**: Django Templates + TailwindCSS + Alpine.js
- **Base de Datos**: PostgreSQL (SQLite para desarrollo)
- **Exportación**: openpyxl (Excel)

## 📦 Instalación

### Prerrequisitos

- Python 3.10 o superior
- PostgreSQL (opcional, SQLite por defecto)
- pip y virtualenv

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
```bash
cd sga-lite
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar entorno virtual**

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Configurar variables de entorno**

Copiar el archivo `.env.example` a `.env`:
```bash
cp .env.example .env
```

**Para desarrollo con SQLite (recomendado para empezar):**
```env
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
TIMEZONE=America/Santo_Domingo
```

**Para producción con PostgreSQL:**
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=sga_lite_db
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
TIMEZONE=America/Santo_Domingo
```

6. **Ejecutar migraciones**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Cargar datos iniciales (seed)**
```bash
python manage.py seed_data
```

Este comando creará:
- Usuario Admin: `admin / admin123`
- Usuario Empleado: `employee1 / password123`
- 3 grupos de asistencia de ejemplo

8. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

9. **Acceder a la aplicación**
- Aplicación web: http://localhost:8000
- Panel Admin Django: http://localhost:8000/admin

## 👤 Credenciales por Defecto

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin | admin123 | Administrador |
| employee1 | password123 | Empleado |

**⚠️ IMPORTANTE**: Cambiar estas contraseñas en producción.

## 📖 Guía de Uso

### Para Administradores

1. **Crear Grupos de Asistencia**
   - Ir a "Groups" en el menú
   - Click en "Create Group"
   - Definir nombre y días permitidos (ej: "Turno Mañana" → Lun-Vie)

2. **Asignar Usuarios a Grupos**
   - Ir a "Users" en el menú
   - Click en "Assign Groups" del usuario deseado
   - Seleccionar uno o varios grupos

3. **Ver Dashboard en Vivo**
   - Dashboard muestra empleados activos (fichados)
   - Estadísticas en tiempo real

4. **Generar Reportes**
   - Ir a "Reports"
   - Filtrar por fecha y/o usuario
   - Exportar a Excel

### Para Empleados

1. **Fichar Entrada**
   - Login con credenciales
   - Ver botón "CLOCK IN" (solo si es día permitido)
   - Click para registrar entrada

2. **Fichar Salida**
   - El botón cambia a "CLOCK OUT"
   - Click para registrar salida
   - Ver total de horas trabajadas

3. **Ver Historial**
   - Historial de últimos 7 días en dashboard

## 🔧 Estructura del Proyecto

```
sga-lite/
├── sga_project/          # Configuración principal Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                # App de usuarios
│   ├── models.py
│   ├── views.py
│   └── management/
│       └── commands/
│           └── seed_data.py
├── attendance/           # App de asistencia
│   ├── models.py        # AttendanceGroup, UserGroup, AttendanceLog
│   ├── views.py         # Lógica de negocio
│   ├── urls.py
│   └── admin.py
├── templates/            # Templates HTML
│   ├── base/
│   ├── users/
│   └── attendance/
├── static/               # Archivos estáticos
├── manage.py
├── requirements.txt
└── README.md
```

## 📊 Modelo de Datos

### Users (Custom User Model)
- username, email, password
- role: ADMIN / EMPLOYEE
- is_active

### AttendanceGroup
- name: Nombre del grupo
- allowed_days: JSON [0-6] (0=Lunes, 6=Domingo)

### UserGroup (Many-to-Many)
- user_id
- group_id

### AttendanceLog
- user_id
- date
- check_in (Time)
- check_out (Time)
- Constraint: Único por user+date

## 🧪 Criterios de Aceptación (Testing)

Para verificar que el sistema funciona correctamente:

```python
# Test Case 1: Crear grupo de fin de semana
1. Admin crea grupo "Weekend" con Sábado y Domingo
2. Admin asigna "Usuario A" al grupo "Weekend"
3. Usuario A intenta fichar un Miércoles → Sistema NO muestra botón
4. Usuario A intenta fichar un Sábado → Sistema SÍ permite fichar
5. Usuario A marca Entrada y Salida
6. Admin descarga Excel con el registro ✓
```

## 🚀 Despliegue en Producción

### Opción 1: VPS (Contabo/Hetzner/DigitalOcean)

1. **Preparar servidor**
```bash
sudo apt update
sudo apt install python3-pip python3-venv postgresql nginx
```

2. **Clonar proyecto**
```bash
git clone <tu-repo>
cd sga-lite
```

3. **Configurar PostgreSQL**
```bash
sudo -u postgres createdb sga_lite_db
sudo -u postgres createuser sga_user
sudo -u postgres psql
ALTER USER sga_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE sga_lite_db TO sga_user;
```

4. **Configurar .env para producción**
```env
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=sga_lite_db
DB_USER=sga_user
DB_PASSWORD=tu-password
SECRET_KEY=tu-clave-super-secreta
```

5. **Instalar y migrar**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py collectstatic
```

6. **Configurar Gunicorn**
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 sga_project.wsgi
```

7. **Configurar Nginx** (ver docs de Nginx para proxy reverso)

### Opción 2: Oracle Cloud Free Tier

1. Crear instancia Ubuntu
2. Seguir pasos de VPS
3. Abrir puerto 8000 en firewall
4. Configurar dominio (opcional)

## 🔒 Seguridad

- ✅ CSRF Protection habilitado
- ✅ Password hashing con Django
- ✅ SQL Injection protection (ORM)
- ⚠️ Cambiar SECRET_KEY en producción
- ⚠️ Usar HTTPS en producción
- ⚠️ Configurar ALLOWED_HOSTS correctamente

## 📝 Comandos Útiles

```bash
# Crear superusuario adicional
python manage.py createsuperuser

# Crear usuario empleado desde shell
python manage.py shell
>>> from users.models import User
>>> User.objects.create_user(username='juan', password='pass123', role='EMPLOYEE')

# Resetear base de datos (CUIDADO: Borra todo)
python manage.py flush
python manage.py seed_data

# Colectar archivos estáticos para producción
python manage.py collectstatic
```

## 🐛 Troubleshooting

**Error: No module named 'decouple'**
```bash
pip install python-decouple
```

**Error: (1049, "Unknown database")**
- Verificar que la base de datos PostgreSQL existe
- O cambiar a SQLite en .env

**Error: ALLOWED_HOSTS**
- Agregar tu IP/dominio a ALLOWED_HOSTS en .env

## 📄 Licencia

Proyecto desarrollado para uso interno. Todos los derechos reservados.

## 👨‍💻 Soporte

Para dudas o problemas:
1. Revisar este README
2. Consultar logs: `python manage.py runserver` muestra errores
3. Verificar configuración en .env

---

**Desarrollado con ❤️ usando Django + TailwindCSS**
