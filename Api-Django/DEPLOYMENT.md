# Guía de Despliegue - API Django

## Problemas Corregidos

1. **ALLOWED_HOSTS vacío**: Ahora se requiere definir explícitamente los hosts permitidos mediante la variable de entorno `ALLOWED_HOSTS`
2. **SECRET_KEY sin validación**: Ahora se valida que SECRET_KEY esté configurada en variables de entorno
3. **Base de datos SQLite en producción**: Se agregó soporte para PostgreSQL y outras bases de datos
4. **CORS no configurado**: Se agregó django-cors-headers para permitir peticiones desde otros dominios

## Variables de Entorno Requeridas

Para desplegar en producción, establece las siguientes variables de entorno:

```
SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## Variables de Entorno Opcionales (Base de Datos)

### Opción 1: PostgreSQL (Recomendado para producción)

```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

O configure individualmente:

```
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=dbname
DATABASE_USER=user
DATABASE_PASSWORD=password
```

### Opción 2: SQLite (Desarrollo local)

Por defecto usará SQLite si no se especifica una base de datos PostgreSQL.

## Pasos de Despliegue

### 1. Preparar el entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus valores
nano .env
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar migraciones

```bash
python manage.py migrate
```

### 4. Recopilar archivos estáticos

```bash
python manage.py collectstatic --noinput
```

### 5. Iniciar el servidor (desarrollo)

```bash
python manage.py runserver
```

### 6. Iniciar con Gunicorn (producción)

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

## Despliegue en Heroku

1. Crea una aplicación en Heroku
2. Agrega la base de datos PostgreSQL:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

3. Establece las variables de entorno:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app.herokuapp.com
   ```

4. Realiza un push a Heroku:
   ```bash
   git push heroku main
   ```

## Troubleshooting

### Error 500 - SECRET_KEY no configurada
- Asegúrate de que la variable `SECRET_KEY` esté establecida en el entorno de despliegue

### Error 500 - ALLOWED_HOSTS inválido
- Verifica que `ALLOWED_HOSTS` incluya el dominio correcto de tu aplicación
- Recuerda separar múltiples hosts con comas

### Error en conexión a base de datos
- Si usas SQLite: verifica que el archivo db.sqlite3 sea accesible y escribible
- Si usas PostgreSQL: verifica que DATABASE_URL sea correcta o que DATABASE_HOST, DATABASE_NAME, etc. estén configurados

### CORS Error
- Configura `CORS_ALLOWED_ORIGINS` con los dominios desde los que se hará peticiones
- Incluye el protocolo (http:// o https://)
