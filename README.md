# Trycore EVM — Project Management Dashboard

Aplicación fullstack para la gestión de proyectos y actividades mediante Earned Value Management (EVM). Permite gestionar presupuestos, avances y costos, calcular indicadores individuales y consolidados y visualizar el desempeño mediante un dashboard interactivo.

## Tecnologías

- **Frontend:** React, Vite, JavaScript/JSX.
- **Backend:** Python, FastAPI, Pydantic.
- **Base de datos:** PostgreSQL, SQLAlchemy, psycopg.
- **Motor EVM:** Python Decimal.
- **Testing:** pytest, pytest-cov, Vitest, Testing Library.
- **Calidad:** Ruff, Oxlint.
- **Control de versiones:** Gitflow y GitHub.

## Requisitos

- Python 3.12.
- Node.js y npm.
- PostgreSQL 17.
- Windows y PowerShell para ejecutar los comandos siguientes.

## Instalación y ejecución

Los comandos parten de la raíz del repositorio.

### 1. PostgreSQL

Crear una base de datos denominada `trycore_evm` y ejecutar el script de inicialización:

```powershell
psql -U postgres -d trycore_evm -f database/init_db.sql
```

Si `psql` no está disponible en PATH, utilizar su ruta de instalación.

La configuración detallada se encuentra en [docs/database.md](docs/database.md).

### 2. Backend

```powershell
py -3.12 -m venv backend/.venv
cd backend
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Configurar `DATABASE_URL` en `backend/.env` con las credenciales locales de PostgreSQL y ejecutar:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Servicios disponibles:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/api-docs
- Health check: http://127.0.0.1:8000/health

### 3. Frontend

En otra terminal, desde la raíz del repositorio:

```powershell
cd frontend
npm.cmd ci
Copy-Item .env.example .env
npm.cmd run dev
```

Abrir http://localhost:5173.

El frontend se conecta al backend mediante el proxy de desarrollo de Vite. Ambos servidores deben estar ejecutándose.

No versionar archivos `.env` con credenciales.

## Funcionalidades

- CRUD de proyectos y actividades.
- Cálculo de BAC, PV, EV, AC, CV, SV, CPI, SPI, EAC y VAC.
- Indicadores individuales y consolidados.
- Interpretaciones visuales de CPI y SPI.
- Tabla de actividades y gráfica PV vs. EV vs. AC.
- Validación de entradas y manejo de indicadores indefinidos.
- API REST documentada mediante Swagger/OpenAPI.

Los indicadores EVM se calculan en el backend, sin duplicar las fórmulas en el frontend ni almacenar resultados derivados en PostgreSQL.

## Pruebas

Para ejecutar las pruebas completas del backend, crear una base independiente `trycore_evm_test` y configurar `backend/.env.test` a partir de `.env.test.example`.

Desde `backend/`:

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
```

Desde `frontend/`:

```powershell
npm.cmd test -- --run
npm.cmd run lint
npm.cmd run build
```

## Documentación

- [Arquitectura](docs/architecture.md)
- [Base de datos](docs/database.md)
- [API REST](docs/api.md)
- [Frontend](docs/frontend.md)
- [Registro de asistencia de IA](AI_PROCESS.md)

## Consideraciones

La aplicación está preparada para ejecución local. No incluye autenticación ni despliegue productivo.

El desarrollo se organizó mediante ramas Gitflow (`main`, `develop`, `feature/*` y `release/*`) y Pull Requests para integrar las funcionalidades.