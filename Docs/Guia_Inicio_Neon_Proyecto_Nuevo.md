# Guía de inicio con Neon PostgreSQL para nuevos proyectos

Esta guía explica paso a paso cómo integrar Neon PostgreSQL en un proyecto FastAPI desde cero.

---

## 1. Prerrequisitos

- Python 3.8+
- pip
- Cuenta y proyecto en Neon (https://neon.tech)

## 2. Crear base de datos en Neon

1. Inicia sesión en Neon Dashboard.
2. Crea un nuevo proyecto y namespace.
3. Copia la cadena de conexión (Connection String).
   - Ejemplo: `postgres://<user>:<pass>@<host>/<db>?sslmode=require`

## 3. Instalar dependencias

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary asyncpg python-dotenv loguru
```

## 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz:

```env
DATABASE_URL="postgres://<user>:<pass>@<host>/<db>?sslmode=require"
```

## 5. Ajustar `app/config.py`

```python
from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
raw = os.getenv('DATABASE_URL')
# Normalizar para asyncpg
db_url = raw.replace('postgres://', 'postgresql+asyncpg://', 1)
DATABASE_URL = db_url
```

## 6. Crear `app/db/base.py`

```python
from sqlalchemy.orm import declarative_base
Base = declarative_base()
```

## 7. Crear `app/db/database.py`

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

# Separar sslmode y pasar connect_args
url = DATABASE_URL.split('?')[0]
engine = create_async_engine(url, connect_args={'ssl': True}, pool_pre_ping=True)
SessionLocal = sessionmaker(class_=AsyncSession, bind=engine, autoflush=False, autocommit=False)

async def get_db():
    async with SessionLocal() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    await engine.dispose()
```

## 8. Usar en FastAPI

- Importar `get_db()` en rutas y modelos.
- En `app/main.py`, usar `init_db()` y `close_db()` en el lifespan.

## 9. Ejecutar la aplicación

```bash
uvicorn app.main:app --reload
```

---

Con esto tendrás un proyecto limpio usando Neon PostgreSQL con FastAPI y SQLAlchemy asíncrono.
