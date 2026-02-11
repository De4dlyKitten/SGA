# SGA-Lite - Guía de Testing y Validación

## 🎯 Criterios de Aceptación

Este documento describe cómo validar que el sistema cumple con todos los requerimientos especificados en el SOW.

---

## Test Suite 1: Autenticación y Roles

### Test 1.1: Login de Administrador
```
DADO que existe un usuario admin con contraseña admin123
CUANDO el admin ingresa sus credenciales correctas
ENTONCES es redirigido al Dashboard de Administrador
Y ve estadísticas en tiempo real
```

**Pasos:**
1. Ir a http://localhost:8000
2. Login con: admin / admin123
3. ✅ Verificar redirección a `/attendance/admin-dashboard/`
4. ✅ Verificar que se ven tarjetas de estadísticas

### Test 1.2: Login de Empleado
```
DADO que existe un empleado employee1 con contraseña password123
CUANDO el empleado ingresa sus credenciales correctas
ENTONCES es redirigido al Dashboard de Empleado
Y ve el reloj y botón de fichaje
```

**Pasos:**
1. Logout del admin
2. Login con: employee1 / password123
3. ✅ Verificar redirección a `/attendance/employee/`
4. ✅ Verificar que se ve el reloj en tiempo real

### Test 1.3: Credenciales Incorrectas
```
CUANDO se ingresan credenciales incorrectas
ENTONCES se muestra un mensaje de error
Y NO se permite el acceso
```

**Pasos:**
1. Login con: wrong / wrong123
2. ✅ Verificar mensaje de error
3. ✅ Verificar que permanece en página de login

---

## Test Suite 2: Gestión de Grupos

### Test 2.1: Crear Grupo de Fin de Semana
```
DADO que soy administrador
CUANDO creo un grupo "Weekend" con Sábado y Domingo
ENTONCES el grupo se crea correctamente
Y está disponible para asignación
```

**Pasos:**
1. Login como admin
2. Ir a "Groups" → "Create Group"
3. Nombre: "Weekend Shift"
4. Seleccionar: Saturday, Sunday
5. Click "Create Group"
6. ✅ Verificar mensaje de éxito
7. ✅ Verificar que aparece en lista de grupos

### Test 2.2: Editar Grupo Existente
```
CUANDO edito un grupo existente
ENTONCES los cambios se guardan correctamente
```

**Pasos:**
1. En lista de grupos, click "Edit" en "Weekend Shift"
2. Agregar Friday a los días
3. Click "Save Changes"
4. ✅ Verificar que ahora muestra "Friday, Saturday, Sunday"

### Test 2.3: Eliminar Grupo
```
CUANDO elimino un grupo
ENTONCES se elimina de la base de datos
Y las asignaciones de usuarios se eliminan
```

**Pasos:**
1. Crear grupo temporal "Test Group"
2. Click "Delete" en "Test Group"
3. Confirmar eliminación
4. ✅ Verificar que ya no aparece en la lista

---

## Test Suite 3: Asignación de Usuarios a Grupos

### Test 3.1: Asignar Usuario a Grupo
```
DADO que existe el usuario "employee1"
Y existe el grupo "Weekend Shift" (Sáb-Dom)
CUANDO asigno "employee1" al grupo "Weekend Shift"
ENTONCES la asignación se guarda correctamente
```

**Pasos:**
1. Ir a "Users" → "Assign Groups" de employee1
2. Seleccionar "Weekend Shift"
3. Click "Save Assignments"
4. ✅ Verificar que en la lista de usuarios, employee1 muestra "Weekend Shift"

### Test 3.2: Asignar Usuario a Múltiples Grupos
```
CUANDO asigno un usuario a múltiples grupos
ENTONCES puede fichar en días de cualquiera de sus grupos
```

**Pasos:**
1. Crear grupo "Weekday Shift" (Lun-Vie)
2. Asignar employee1 a AMBOS: "Weekday Shift" y "Weekend Shift"
3. ✅ Verificar que employee1 muestra ambos grupos

---

## Test Suite 4: Fichaje (Core Business Logic) ⭐

### Test 4.1: Fichaje en Día NO Permitido (CRÍTICO)
```
DADO que "employee1" está asignado SOLO al grupo "Weekend Shift" (Sáb-Dom)
CUANDO intenta fichar un MIÉRCOLES
ENTONCES el sistema NO muestra el botón de fichar
Y muestra mensaje "Not Scheduled Today"
```

**Pasos:**
1. Asegurar que employee1 SOLO tiene "Weekend Shift"
2. Cambiar la fecha del sistema a un Miércoles (o esperar a miércoles)
3. Login como employee1
4. ✅ **VERIFICAR: NO aparece botón "CLOCK IN"**
5. ✅ **VERIFICAR: Aparece mensaje "Not Scheduled Today"**

### Test 4.2: Fichaje en Día Permitido (CRÍTICO)
```
DADO que "employee1" está asignado al grupo "Weekend Shift" (Sáb-Dom)
CUANDO intenta fichar un SÁBADO
ENTONCES el sistema SÍ muestra el botón "CLOCK IN"
Y permite marcar entrada
```

**Pasos:**
1. Cambiar la fecha del sistema a un Sábado
2. Login como employee1
3. ✅ **VERIFICAR: Aparece botón "CLOCK IN"**
4. Click en "CLOCK IN"
5. ✅ Verificar mensaje de éxito con hora
6. ✅ Verificar que botón cambia a "CLOCK OUT"

### Test 4.3: Marcar Salida
```
DADO que ya marqué entrada
CUANDO hago click en "CLOCK OUT"
ENTONCES se registra la hora de salida
Y se calcula el total de horas
```

**Pasos:**
1. Estando fichado (botón "CLOCK OUT" visible)
2. Click en "CLOCK OUT"
3. ✅ Verificar mensaje con total de horas
4. ✅ Verificar mensaje "Workday Complete"

### Test 4.4: No Permitir Doble Entrada
```
CUANDO intento fichar entrada dos veces el mismo día
ENTONCES el sistema muestra advertencia
Y NO crea registro duplicado
```

**Pasos:**
1. Marcar entrada
2. Hacer logout
3. Login nuevamente
4. ✅ Verificar que muestra "You have already clocked in today"

---

## Test Suite 5: Dashboard de Administrador

### Test 5.1: Ver Empleados Activos
```
CUANDO un empleado ficha entrada
ENTONCES aparece en la lista "Currently Active" del admin
```

**Pasos:**
1. Employee1 marca entrada (como se hizo arriba)
2. Login como admin
3. ✅ Verificar que employee1 aparece en "Currently Active"
4. ✅ Verificar que muestra hora de entrada
5. ✅ Verificar que muestra duración en tiempo real

### Test 5.2: Ver Empleados Completados
```
CUANDO un empleado marca entrada Y salida
ENTONCES aparece en la lista "Completed Today"
CON el total de horas trabajadas
```

**Pasos:**
1. Employee1 marca salida
2. Refrescar dashboard de admin
3. ✅ Verificar que employee1 aparece en "Completed Today"
4. ✅ Verificar que muestra total de horas (ej: "8.50 hrs")

---

## Test Suite 6: Reportes y Exportación

### Test 6.1: Filtrar Reportes por Fecha
```
CUANDO filtro reportes por rango de fechas
ENTONCES solo veo registros en ese rango
```

**Pasos:**
1. Ir a "Reports"
2. Seleccionar Start Date: hoy
3. Seleccionar End Date: hoy
4. Click "Apply Filters"
5. ✅ Verificar que solo muestra registros de hoy

### Test 6.2: Filtrar por Usuario
```
CUANDO filtro reportes por usuario específico
ENTONCES solo veo registros de ese usuario
```

**Pasos:**
1. En Reports, seleccionar employee1 en dropdown
2. Click "Apply Filters"
3. ✅ Verificar que solo muestra registros de employee1

### Test 6.3: Exportar a Excel (CRÍTICO)
```
DADO que existen registros de asistencia
CUANDO hago click en "Export to Excel"
ENTONCES se descarga un archivo .xlsx
CON todos los datos correctos
```

**Pasos:**
1. Asegurar que existe al menos un registro completo
2. En Reports, click "Export to Excel"
3. ✅ Verificar que se descarga archivo .xlsx
4. ✅ Abrir archivo y verificar:
   - Columnas: User, Date, Check In, Check Out, Total Hours
   - Datos correctos
   - Formato profesional (headers en negrita, etc.)

---

## Test Suite 7: Validaciones de Negocio

### Test 7.1: No Permitir Salida sin Entrada
```
CUANDO intento marcar salida sin haber marcado entrada
ENTONCES el sistema muestra error
```

**Pasos:**
1. Employee1 no ha fichado hoy
2. Intentar hacer POST a /attendance/clock-out/ (usando Postman o form)
3. ✅ Verificar mensaje: "You must clock in before clocking out"

### Test 7.2: Validar Hora de Salida > Entrada
```
CUANDO marco salida ANTES de la entrada (manipulación)
ENTONCES el sistema rechaza el registro
```

Este test requiere manipulación de base de datos o código:
```python
# En Django shell
from attendance.models import AttendanceLog
from datetime import time, date
log = AttendanceLog.objects.create(
    user_id=2,
    date=date.today(),
    check_in=time(10, 0),
    check_out=time(9, 0)  # Antes de entrada
)
# ✅ Debería lanzar ValidationError
```

---

## Test Suite 8: Test del Caso de Aceptación Principal

**Este es EL TEST más importante del SOW:**

```
ESCENARIO: Validar funcionamiento completo del sistema

DADO:
  - Admin crea grupo "Fines de Semana" con Sábado y Domingo
  - Admin asigna ese grupo al "Usuario A" (employee1)

CUANDO:
  1. Usuario A intenta entrar un MIÉRCOLES
     ENTONCES: Sistema NO muestra botón de fichar
  
  2. Usuario A intenta entrar un SÁBADO
     ENTONCES: Sistema SÍ permite fichar Entrada y Salida
  
  3. Admin descarga Excel
     ENTONCES: Ve el registro de esas horas

RESULTADO ESPERADO: ✅ TODOS los pasos funcionan correctamente
```

**Pasos Detallados:**

```bash
# PARTE 1: Setup (como Admin)
1. Login como admin
2. Ir a "Groups" → "Create Group"
3. Nombre: "Fines de Semana"
4. Seleccionar SOLO: Saturday, Sunday
5. Save
6. Ir a "Users" → employee1 → "Assign Groups"
7. Quitar TODOS los grupos previos
8. Seleccionar SOLO "Fines de Semana"
9. Save

# PARTE 2: Test Miércoles (como Employee)
10. Logout
11. Cambiar fecha del sistema a un Miércoles
12. Login como employee1
13. ✅ VERIFICAR: NO hay botón "CLOCK IN"
14. ✅ VERIFICAR: Mensaje "Not scheduled on Wednesday"

# PARTE 3: Test Sábado (como Employee)
15. Cambiar fecha del sistema a un Sábado
16. Refresh página
17. ✅ VERIFICAR: Aparece botón "CLOCK IN"
18. Click "CLOCK IN"
19. ✅ VERIFICAR: Entrada registrada
20. Click "CLOCK OUT"
21. ✅ VERIFICAR: Salida registrada + Total Horas

# PARTE 4: Descarga Excel (como Admin)
22. Logout
23. Login como admin
24. Ir a "Reports"
25. Filtrar por el Sábado
26. Click "Export to Excel"
27. ✅ VERIFICAR: Descarga archivo
28. ✅ VERIFICAR: Archivo contiene:
    - User: employee1
    - Date: [sábado]
    - Check In: [hora]
    - Check Out: [hora]
    - Total Hours: [calculado]
```

**Si TODOS estos pasos pasan → El proyecto está COMPLETO ✅**

---

## Checklist Final de Aceptación

Marcar cada item cuando esté validado:

### Funcionalidades Core
- [ ] Login funciona para Admin y Employee
- [ ] Redirección correcta según rol
- [ ] Crear grupos de asistencia
- [ ] Editar grupos de asistencia
- [ ] Eliminar grupos de asistencia
- [ ] Asignar usuarios a grupos
- [ ] Desasignar usuarios de grupos

### Lógica de Fichaje
- [ ] Empleado NO puede fichar en día no permitido
- [ ] Empleado SÍ puede fichar en día permitido
- [ ] Marcar entrada funciona
- [ ] Marcar salida funciona
- [ ] Cálculo de horas es correcto
- [ ] No permite doble entrada
- [ ] No permite salida sin entrada

### Dashboard Admin
- [ ] Muestra empleados activos en tiempo real
- [ ] Muestra empleados completados del día
- [ ] Estadísticas son correctas

### Reportes
- [ ] Filtro por fecha funciona
- [ ] Filtro por usuario funciona
- [ ] Exportación a Excel funciona
- [ ] Archivo Excel tiene formato correcto
- [ ] Datos en Excel son correctos

### Caso de Aceptación Principal
- [ ] Test completo del escenario Weekend pasa

---

## Comandos Útiles para Testing

```bash
# Resetear base de datos para testing limpio
python manage.py flush
python manage.py seed_data

# Ver registros en consola
python manage.py shell
>>> from attendance.models import AttendanceLog
>>> AttendanceLog.objects.all()

# Crear usuario de prueba rápido
python manage.py shell
>>> from users.models import User
>>> User.objects.create_user(username='test', password='test123', role='EMPLOYEE')

# Simular día específico (en código)
from datetime import date
from unittest.mock import patch
with patch('django.utils.timezone.localdate', return_value=date(2025, 2, 15)):  # Sábado
    # Tu código aquí
```

---

## Conclusión

Si TODOS los tests de esta guía pasan, el sistema cumple al 100% con el SOW y está listo para producción.

**Tiempo estimado de testing completo: 30-45 minutos**
