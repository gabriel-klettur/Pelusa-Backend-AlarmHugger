# Implementación de Neon PostgreSQL en Pelusa-Backend-AlarmHugger

Este documento describe cómo migramos y configuramos Neon PostgreSQL en este proyecto.

---

## 1. Dependencias

- `psycopg2-binary` y `asyncpg` para conexión Postgres asíncrona.
- `python-dotenv` para cargar variables de entorno.
- `sqlalchemy` para ORM.
- `loguru` para logging.

Actualizadas en `requirements.txt`:
```text
psycopg2-binary
asyncpg
python-dotenv
loguru
```  

## 2. Variables de entorno

En `.env`:
```env
DATABASE_URL="postgres://<user>:<pass>@<host>/<db>?sslmode=require"
ALLOWED_IPS=...
BLOCKED_IPS=...
```  

## 3. Configuración en `app/config.py`

- Carga con `load_dotenv()`.
- Normaliza `DATABASE_URL`: reemplaza `postgres://` o `postgresql://` por `postgresql+asyncpg://`.

```python
raw = os.getenv('DATABASE_URL')
if raw.startswith('postgres://'):
    DATABASE_URL = raw.replace('postgres://','postgresql+asyncpg://',1)
else:
    DATABASE_URL = raw
```

## 4. Base de datos en `app/db`

### `base.py`
```python
from sqlalchemy.orm import declarative_base
Base = declarative_base()
```

### `database.py`
- Extrae la parte antes de `?` para la URL.
- Configura `connect_args={'ssl': True}` si `sslmode=require`.
- Crea `create_async_engine(db_url, connect_args, pool_pre_ping=True)`.
- Define `SessionLocal = sessionmaker(class_=AsyncSession, bind=engine)`.
- Generadores: `get_db()`, `init_db()`, `close_db()`.

## 5. Modelos en `app/alarms/models.py`

- Usa `Base` de `app.db.base`.
- Tabla única `tbl_alarms` con columnas:
  - `id`, `Ticker`, `Interval`, `Quantity`, `Price_Alert`, `Time_Alert`, `Order`, `Strategy`, `created_at`.

## 6. Rutas

### Webhook (`app/alarms/routes.py`)
- Inyecta `db: AsyncSession = Depends(get_db)`.
- Procesa payload Pydantic `AlarmCreate` y guarda con repositorio.

### Health Check (`app/server/routes.py`)
- Inyecta DB y ejecuta `SELECT 1`.
- Retorna JSON con estado y hora.

## 7. Aplicación principal (`app/main.py`)

- Definición de `lifespan`: llama `init_db()` y `close_db()`.
- Configura middlewares y CORS.
- `include_router(alarms_router, prefix="/alarms")`.
- `include_router(server_router, prefix="/server")`.

## 8. README.md

- Actualizada para Neon:
  - Reemplazo de Turso/SQLite por Neon PostgreSQL.
  - Instrucciones de `.env` y deployment.

## 9. Scripts de prueba

- `test_endpoints.py` en raíz:
  - `test_health()` y `test_webhook()` con `requests`.

## 10. Pasos finales

1. Ejecutar `uvicorn app.main:app --reload`.
2. Probar endpoints con `python test_endpoints.py`.
3. Actualizar CI/CD y documentación adicional si es necesario.
